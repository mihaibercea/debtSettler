from django.shortcuts import render, reverse, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth import views
from accounts.models import CustomUser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from home.models import Club, Session, Invite, SessionMember, Sum, Payment, JoinRequest, LiveSession
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from accounts.models import CustomUser

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import InviteForm, ZeroSumForm, SessionForm, PluslDebit, DebitForm, LiveSessionForm, PluslBuyIn, PlusStack
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormMixin
import json
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils import timezone

#import pdb; pdb.set_trace()

def send_email(request):
    send_mail(
        'Subject',
        'Body',
        'mihai.bercea@gmail.com',
        ['mihai.bercea@gmail.com'],
        fail_silently=False,
    )
    return render(request, 'email_sent.html')

def index(request):

# Generate counts of some of the main objects
    num_clubs = Club.objects.all().count()    

   
    # The 'all()' is implied by default.
    num_members = CustomUser.objects.count()

    context = {
        'num_clubs': num_clubs,
        'num_members': num_members,        
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context)

class ClubListView(generic.ListView):

    model = Club
    context_object_name = 'club_list'
    queryset = Club.objects.all() 
    #template_name = 'home/club_list.html'  # Specify your own template name/location

@login_required
def myclublist_view(request):
    myclub_list = request.user.clubs.all()
    return render(request, 'home/myclub_list.html', context={'myclub_list': myclub_list})
    
    #queryset = CustomUser.objects.all() 

@login_required
def myinvites_list(request):    
    user = request.user 
    return render(request, 'home/myinvites.html', context={'user': user})

@login_required
def club_join_requests(request, pk):    
    u = request.user
    club = get_object_or_404(Club, pk=pk)
    if u not in club.members.all():     

        return HttpResponseBadRequest('Invalid request')
    
    else: 
        return render(request, 'home/club_join_requests.html', context={'club': club})

@login_required
def mysums(request, interval):
   
    if not interval:
        interval = 'alltime'

    user = request.user
    to_give = 0
    to_receive = 0

    current_date = timezone.now()

    # Calculate the start date for the last 30 days
    last_30_days_start = current_date - timedelta(days=30)

    current_year_start = current_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)  

    for p in user.payments.all():

        if p.paid==False:
            if p.to_member == user:
                to_receive+=p.value
            else:
                to_give+=p.value
        
    if interval=='alltime':
        ls = user.livesessions.all()
    elif interval == 'year':
        ls = user.livesessions.filter(date__gte=current_year_start) 
    elif interval == 'month':
        ls = user.livesessions.filter(date__range=[last_30_days_start, current_date])

    ls_data = []
    ls_labels = []

    for s in ls:
        if ls_data:
            current = ls_data[-1]
        else:
            current=0
        ls_data.append(current+(s.stack-s.buy_in))
        ls_labels.append(str(s.date)) 

    return render(request, 'home/mysums.html', context={'user': user, 'to_give':to_give, 'to_receive':to_receive, 'ls':ls, 'ls_data':ls_data, 'ls_labels':ls_labels, 'interval':interval})

@login_required
def create_live_session(request):

    user = request.user

    if request.method == 'POST':
        form = LiveSessionForm(request.POST)
        
        if form.is_valid():
        
            casino = form.cleaned_data['casino']
            stakes =  form.cleaned_data['stakes'] 
            game =  form.cleaned_data['game'] 
            
            valid_session = LiveSession(casino=casino,  stakes=stakes, game=game, date = timezone.now())            

            valid_session.save()
            user.livesessions.add(valid_session)
            user.save()
            session_id = valid_session.id   

            return redirect('home:live-session-detail', pk=session_id)

            #return render(request, 'home/club_detail.html', context={'club': club, 'sesisons_list':sesisons_list, 'is_member':is_member})
                
    else:
        form = LiveSessionForm()
        #form.name.initial=str(timezone.now())
    return render(request, 'home/livesession_create.html', {'form':form})

@login_required
def livesession_detail(request, pk):
    
        user = request.user
        live_session = get_object_or_404(LiveSession, pk=pk)

        stakes = live_session.stakes
        casino = live_session.casino
        game = live_session.game
        stack = live_session.stack
        buy_in = live_session.buy_in
        result = live_session.stack - live_session.buy_in

        plus_buy_in_form = PluslBuyIn()
        plus_stack_form = PlusStack()

        return render(request, 'home/livesession_detail.html', context={'stakes': stakes, 'casino':casino, 'game':game, 'stack':stack, 'buy_in':buy_in,  'id':live_session.id, 'result':result, 'plus_buy_in':plus_buy_in_form, 'plus_stack':plus_stack_form})


@login_required
@csrf_exempt
def accept_invite(request, pk):
    # is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # if is_ajax:
    #     if request.method == 'POST':
    #         data = json.load(request)
    #         todo = data.get('payload')
    #         Todo.objects.create(task=todo['task'], completed=todo['completed'])
    #         return JsonResponse({'status': 'Todo added!'})
    #     return JsonResponse({'status': 'Invalid request'}, status=400)
    # else:
    #     return HttpResponseBadRequest('Invalid request')   
    
    if request.method == 'GET':
        pk = request.GET['invite_id']
        invite = get_object_or_404(Invite, pk=pk)
        invite.accepted = True
        invite.parent_club.members.add(invite.to_user)
        invite.to_user.clubs.add(invite.parent_club)
        invite.save()
        return HttpResponse('Success')
    else:
        return HttpResponse('Not a GET method')

@login_required
def accept_join_request(request, pk):

    if request.method == 'POST':
        rpk = request.POST['req_id']
        req = get_object_or_404(JoinRequest, pk=rpk)        
        req.parent_club.members.add(req.from_user)
        req.from_user.clubs.add(req.parent_club)
        req.accepted = True
        req.save()
        return HttpResponse('Success')
    else:
        return HttpResponse('Not a POST method')

class ClubDetailView(LoginRequiredMixin, generic.DetailView):
    model = Club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u = self.request.user
        club = self.get_object()        

        if u not in club.members.all():
            is_member = False
            context['is_member'] = is_member
                        
        else:
            is_member = True
            helper_text = "Hello, " + str(u.username) + ". Welcome to " + club.name            
            sessions_list = club.sessions.all()
            context['is_member'] = is_member
            context['sessions_list'] = sessions_list
            context['helper_text'] = helper_text

        return context

    # def club_detail_view(request, primary_key):

    #     u = request.user

    #     club = get_object_or_404(Club, pk=primary_key)

    #     helper_text = "Hello " + str(u.username) + ". Welcome to club: " + club.name

    #     if u not in club.members.all():
            
    #         return render(request, 'home/club_list.html', context={'club_list': Club.objects.all() })    
        
    #     else:

    #         sesisons_list = club.sessions.all()

    #         return render(request, 'home/club_detail.html', context={'club': club, 'sesisons_list':sesisons_list, 'helper_text': helper_text})        
                

# class ClubInviteView(LoginRequiredMixin, generic.DetailView):

#     model = Club
#     template_name = "home/club_invite.html"

def test_view(request):

    # text = 'No text yet.'
    # session = Session.objects.get(id="5702d03c-6aa4-4eaa-b70c-f1f3bbf57958")

    # # if request.method == 'POST':
    # #     form = TestForm(request.POST)
        
    # #     if form.is_valid():

    # #         text = form.cleaned_data['text']          
                
    # #         return render(request, 'test.html', context={'form':form, 'text': text, 'session':session})
    # #         #return HttpResponseRedirect(reverse('home:index'))
    # # else:
        
    # form = ZeroSumForm()

    # return render(request, 'test.html', context={'form':form, 'text': text, 'session':session})
        send_mail(
        'Subject',
        'Body',
        'mihai.bercea@gmail.com',
        ['mihai.bercea@gmail.com'],
        fail_silently=False,
        )
        return render(request, 'test.html')

@login_required
def add_member_debit(request, spk, mpk):
    u = request.user
    session = get_object_or_404(Session, pk=spk)    
    member = get_object_or_404(SessionMember, pk=mpk)

    #if u != sum.member:       
    if u not in session.parent_club.members.all():     

        return HttpResponseBadRequest('Invalid request')
    
    else:   

        if request.method == 'POST':
            form = DebitForm(request.POST)
            if form.is_valid():

                new_debit = form.cleaned_data['debit']
                member.debit = new_debit
                member.save()

                #return render(request, 'session_detail.html', context={'form':form, 'session':session})
                return redirect('home:session-detail', pk=session.id)
        else:        
            return HttpResponse('Not a POST method')
@login_required
def remove_session_member(request, spk, mpk):

    u = request.user
    session = get_object_or_404(Session, pk=spk)    
    member = get_object_or_404(SessionMember, pk=mpk)

    if request.method != 'GET':
        return HttpResponseBadRequest('Invalid request')

    else:      
        if u not in session.parent_club.members.all():     

            return HttpResponseBadRequest('Invalid request')
        
        else:  

            if request.method == 'GET':
                for s in session.sums.all():
                    if s.member == member.main_account:
                        s.delete()
                        member.main_account.save()                        
                        break
                member.delete()
                session.save()

                #return render(request, 'session_detail.html', context={'form':form, 'session':session})
                return redirect('home:session-detail', pk=session.id)
            else:        
                return HttpResponse('Not a DELETE method')
            

@login_required
def plus_debit(request, spk, mpk):

    u = request.user 
    session = get_object_or_404(Session, pk=spk)    
    member = get_object_or_404(SessionMember, pk=mpk)  
    #if u != sum.member:       
    if u not in session.parent_club.members.all():    

        return HttpResponseBadRequest('Invalid request')
    
    else:

        if request.method == 'POST':
            form = PluslDebit(request.POST)
            if form.is_valid():                 
                member.debit = member.debit + form.cleaned_data['plus_debit']
                member.save()

                #return render(request, 'session_detail.html', context={'form':form, 'session':session})

                return redirect('home:session-detail', pk=session.id)
        else:        
            return HttpResponse('Not a POST method')

@login_required
def plus_buy_in(request, lspk):
    u = request.user 
    live_session = get_object_or_404(LiveSession, pk=lspk) 

    if request.method == 'POST':
        form = PluslBuyIn(request.POST)
        if form.is_valid():                 
            live_session.buy_in = live_session.buy_in + form.cleaned_data['plus_buy_in']
            live_session.save()

            #return render(request, 'session_detail.html', context={'form':form, 'session':session})

            return redirect('home:live-session-detail', pk=live_session.id)
    else:        
        return HttpResponse('Not a POST method')
    
    return HttpResponse('Something went wrong')

@login_required
def plus_stack(request, lspk):
    u = request.user 
    live_session = get_object_or_404(LiveSession, pk=lspk) 

    if request.method == 'POST':
        form = PlusStack(request.POST)
        if form.is_valid():                 
            live_session.stack = live_session.stack + form.cleaned_data['plus_stack']
            live_session.save()

            #return render(request, 'session_detail.html', context={'form':form, 'session':session})

            return redirect('home:live-session-detail', pk=live_session.id)     
    else:        
        return HttpResponse('Not a POST method')
    
    return HttpResponse('Something went wrong')

@login_required
def pay_sum(request, pk):

    u = request.user
    sum = get_object_or_404(Sum, pk=pk)

    #if u != sum.member:       
    if u not in sum.parent_session.parent_club.members.all():    

        return HttpResponseBadRequest('Invalid request')
    
    else:

        sum.paid = True
        sum.save()
        return render(request, 'home/session_detail.html')
    
@login_required
def unpay_sum(request, pk):

    u = request.user
    sum = get_object_or_404(Sum, pk=pk)

    #if u != sum.member:       
    if u not in sum.parent_session.parent_club.members.all():    

        return HttpResponseBadRequest('Invalid request')
    
    else:

        sum.paid = False
        sum.save()
        return render(request, 'home/session_detail.html')
    
@login_required
def pay_payment(request, pk):

    u = request.user
    payment = get_object_or_404(Payment, pk=pk)

    #if u != sum.member:       
    if u not in [payment.to_member, payment.from_member]:    

        return HttpResponseBadRequest('You cannot change payment status for someone else')
    
    else:

        payment.paid = True
        payment.save()
        return render(request, 'home/session_detail.html')
    
@login_required
def unpay_payment(request, pk):

    u = request.user
    payment= get_object_or_404(Payment, pk=pk)

    #if u != sum.member:       
    if u not in [payment.to_member, payment.from_member]:      

        return HttpResponseBadRequest('You cannot change payment status for someone else')
    
    else:

        payment.paid = False
        payment.save()
        return render(request, 'home/session_detail.html')

@login_required
def make_payments(request, pk):

    u = request.user    
    session = get_object_or_404(Session, pk=pk)

    #if u != sum.member:       
    if u not in session.parent_club.members.all():    

        return HttpResponseBadRequest('Invalid request')
    
    else:
        
        plus_sums = []
        minus_sums = []

        for sum in session.sums.all():
            val = sum.current_sum
            if sum.current_sum > 0:
                plus_sums.append([sum, val])
            elif sum.current_sum < 0:
                minus_sums.append([sum, val])     
        
        sorted(plus_sums, key=lambda x: x[1])
        sorted(minus_sums, key=lambda x: x[1])

        while len(plus_sums)>0 and len(minus_sums)>0:            
            if abs(abs(minus_sums[0][1]) - plus_sums[0][1]) <= 0.01:
                payment = Payment(
                    from_member = minus_sums[0][0].member,
                    to_member = plus_sums[0][0].member,
                    parent_session = session,
                    value = plus_sums[0][1]
                )
                payment.save()
                session.payments.add(payment)
                session.save()
                minus_sums[0][0].member.payments.add(payment)
                minus_sums[0][0].member.save()
                plus_sums[0][0].member.payments.add(payment)
                plus_sums[0][0].member.save()
                minus_sums.pop(0)
                plus_sums.pop(0)

            elif abs(minus_sums[0][1]) > plus_sums[0][1]:

                payment = Payment(
                    from_member = minus_sums[0][0].member,
                    to_member = plus_sums[0][0].member,
                    parent_session = session,
                    value = plus_sums[0][1]
                )
                payment.save()         
                session.payments.add(payment)
                session.save()
                minus_sums[0][0].member.payments.add(payment)
                minus_sums[0][0].member.save()
                plus_sums[0][0].member.payments.add(payment)
                plus_sums[0][0].member.save()       
                minus_sums[0][1]+=plus_sums[0][1]
                plus_sums.pop(0)

            else:

                payment = Payment(
                    from_member = minus_sums[0][0].member,
                    to_member = plus_sums[0][0].member,
                    parent_session = session,
                    value = abs(minus_sums[0][1])
                )
                payment.save()
                session.payments.add(payment)
                session.save()
                minus_sums[0][0].member.payments.add(payment)
                minus_sums[0][0].member.save()
                plus_sums[0][0].member.payments.add(payment)
                plus_sums[0][0].member.save()
                plus_sums[0][1]+=minus_sums[0][1]
                minus_sums.pop(0)        

        return redirect('home:session-detail', pk=session.pk)

@login_required
def create_session(request, pk):

    club = get_object_or_404(Club, pk=pk)

    u = request.user

    if u not in club.members.all():
        is_member = False
        sesisons_list = club.sessions.all()

        return render(request, 'home/club_detail.html', context={'club': club, 'sesisons_list':sesisons_list, 'is_member':is_member})

    else:

        is_member = True

        if request.method == 'POST':
            form = SessionForm(request.POST)
            
            if form.is_valid():
            
                type = form.cleaned_data['type']
                name =  form.cleaned_data['name']  
                
                valid_session = Session(time_created = timezone.now(), name = name,  type = type, parent_club = club)            

                valid_session.save()
                club.sessions.add(valid_session)
                club.save()

                sesisons_list = club.sessions.all()

                return redirect('home:club-detail', pk=club.pk)

                #return render(request, 'home/club_detail.html', context={'club': club, 'sesisons_list':sesisons_list, 'is_member':is_member})
                    
        else:
            form = SessionForm()
            #form.name.initial=str(timezone.now())
        return render(request, 'home/session_create.html', context={'club': club, 'form':form, 'is_member': is_member})

@login_required
def delete_session(request, pk):

    if request.method != 'DELETE':
        return HttpResponseBadRequest('Invalid request')

    else:

        session = get_object_or_404(Session, pk=pk)
        u = request.user
        club = session.parent_club    
        
        if u not in club.members.all():
            is_member = False
            sesisons_list = club.sessions.all()

            return render(request, 'home/club_detail.html', context={'club': club, 'sesisons_list':sesisons_list, 'is_member':is_member})

        else:
            is_member = True
            club = session.parent_club
            for payment in session.payments.all():
                payment.delete()                    
            session.delete()
            sesisons_list = club.sessions.all()
            return render(request, 'home/club_detail.html', context={'club': club, 'sesisons_list':sesisons_list, 'is_member':is_member})    


@login_required
def session_add_user(request, pk):

    session = get_object_or_404(Session, pk=pk)

    u = request.user

    if u not in session.parent_club.members.all():
        return HttpResponseBadRequest('Invalid request')
    
    else:    

        members_already_in_session = []
        
        for member in session.members.all():
            members_already_in_session.append((member.id))

        if request.method == 'POST':

            member_id = request.POST.get('member_id')            

            current_id = str(session.id) + str(member_id)

            if current_id not in members_already_in_session:
                
                new_member_username =  request.POST.get('new_member_username')

                acc = CustomUser.objects.get(id=str(member_id))
                
                session_member = SessionMember(
                    id = current_id,
                    name = str(new_member_username),            
                    debit=0,
                    settled_sum=0,
                    parent_session = session,
                    main_account = acc
                )

                new_sum = Sum(                    
                    member = acc,
                    current_sum = 0,
                    parent_session = session                    
                )

                new_sum.save()

                acc.sums.add(new_sum)
                acc.save()
                session_member.save()

        #name = str(new_member_username), debit=0, settled_sum=0,parent_session = session

                session.members.add(session_member)
                session.save()

                #return render(request, 'home/session_detail.html', context={'session': session})
                # messages.success(request, "Member added." )
                # return redirect('home:session-detail', pk=session.pk)
                response_data = {
                'message': 'User added successfully',
                 }

                return JsonResponse(response_data)
        # Any other data you want to send back to the client   
    
            else:
                response_data = {
                'message': 'User already in session',
                 }

                return JsonResponse(response_data)
                # messages.success(request, "Member already in session." )
                # return redirect('home:index')
                #return redirect('home:session-detail', pk=session.pk)
            
        else:
            return HttpResponseBadRequest('Invalid request')

@login_required
def settle_session(request, pk):  
    session = get_object_or_404(Session, pk=pk)

    u = request.user

    if u not in session.parent_club.members.all():
        return HttpResponseBadRequest('Invalid request')
    
    else:
        
        if session.status == "o":

            if session.type == 's':               
                
                total_spent = 0
                num_members = 0

                for member in session.members.all():
                    total_spent += member.debit
                    num_members += 1

                if num_members > 0:
                    mean_spent = total_spent / num_members 

                    for member in session.members.all():
                        member.settled_sum = member.debit - mean_spent
                        acc = member.main_account
                        for s in acc.sums.all():
                            if s.parent_session == session:
                                s.current_sum = member.debit - mean_spent
                                s.save()
                                session.sums.add(s)
                        
                        member.save()

                    session.status='c'
                    session.save()

                return redirect('home:session-detail', pk=session.id)            
                
            elif session.type == 'z':           

                for member in session.members.all():
                    member.settled_sum = member.debit                        
                    acc = member.main_account
                    for s in acc.sums.all():
                        if s.parent_session == session:
                            s.current_sum = member.debit
                            s.save()
                            session.sums.add(s)                 
                    
                    member.save()

                session_bias = 0

                for sum in session.sums.all():
                    val = sum.current_sum
                    session_bias+=val
                
                session.bias = session_bias   

                session.status='c'
                session.save()
                return redirect('home:session-detail', pk=session.id)

        elif session.status =='c':

            session.status='o'
            for sum in session.sums.all():
                sum.paid = False
                sum.save()
            for payment in session.payments.all():
                payment.delete()                
            session.save()
            return redirect('home:session-detail', pk=session.id)

        else:
            return HttpResponseBadRequest('Invalid request')

@login_required
def club_request_join(request, pk):
    club = get_object_or_404(Club, pk=pk)
    u = request.user

    if u in club.members.all():
        return HttpResponseBadRequest('User is already a member of the club')
    
    else:
        join_req =  JoinRequest(
            parent_club = club,    
            from_user = u
        )
        join_req.save()
        club.join_requests.add(join_req)
        club.save()
        u.join_requests.add(join_req)
        u.save()

        return render(request, 'myinvites.html')

@login_required
def club_invite(request, pk):
    club = get_object_or_404(Club, pk=pk)

    u = request.user

    if u not in club.members.all():
        return HttpResponseBadRequest('Invalid request')
    
    else: 
        helper_text = 'Invite a user:'        

        if request.method == 'POST':
            form = InviteForm(request.POST)
            
            if form.is_valid():

                user_invited = form.cleaned_data['user']                

                for u in CustomUser.objects.all():
                    if user_invited == str(u.username):

                        already_exists = False

                        for inv in club.invites_sent.all():
                            if inv.to_user == u:
                                helper_text = 'The user already has an invite to this club. Invite another user?'
                                return render(request, 'home/club_invite.html',  context={'form':form, 'helper_text':helper_text, 'club': club})

                        valid_invite = Invite(parent_club=club, from_user=request.user, to_user=u, time_created = timezone.now())

                        helper_text = 'Invite a user:'

                        valid_invite.save()                        
                        club.invites_sent.add(valid_invite)
                        u.invites_received.add(valid_invite)
                        club.save() 
                        return render(request, 'home/club_invite.html',  context={'form':form, 'helper_text':'Invite sent. Invite another user?', 'club': club})
                    
                return render(request, 'home/club_invite.html', context={'form':form, 'helper_text':'User not found. Please input a valid username', 'club': club})
        else:
            form = InviteForm()
        return render(request, 'home/club_invite.html', context={'club': club, 'form':form, 'helper_text':helper_text})


class SessionDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Session
    form_class = ZeroSumForm

    def get_success_url(self):
        return reverse_lazy('home:session-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(SessionDetailView, self).get_context_data(**kwargs)
        session = get_object_or_404(Session, pk=self.kwargs['pk'])

        u = self.request.user
        if u not in session.parent_club.members.all():

            is_member = False
        else:
            is_member = True
        
        context['is_member'] = is_member
        context['session'] = session
        context['form_debit'] = DebitForm(initial={'parent_session': self.object})
        context['plus_debit'] = PluslDebit(initial={'parent_session': self.object})
        return context

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    # def form_valid(self, form):
    #     session_member = form.save(commit=False)
    #     session_member.save()
    #     return super().form_valid(form)

    def session_detail_view(request):                   

        return render(request, 'session_detail.html')
        
    #test

class ClubCreate(LoginRequiredMixin, CreateView):
    model = Club        
    fields = ['name']
    initial = {'sessions': 'None', 'time_created': timezone.now()}

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save(commit=False)
        self.object.save()                
        form.instance.members.add(self.request.user)
        self.request.user.clubs.add(self.object)

        return super(ClubCreate, self).form_valid(form)
    
    #login_url = '/login/'
    #redirect_field_name = 'redirect_to'

    #success_url = reverse_lazy('my_clubs') 
        

class ClubUpdate(LoginRequiredMixin, UpdateView):
    model = Club
    fields = ['name', 'members'] 

class ClubDelete(LoginRequiredMixin, DeleteView):
    model = Club
    success_url = reverse_lazy('home:clubs')  