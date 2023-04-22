from django.shortcuts import render, reverse, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth import views
from accounts.models import CustomUser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from home.models import Club, Session, Invite, SessionMember
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from accounts.models import CustomUser

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import InviteForm, TestForm, SessionForm
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormMixin
import json



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
            helper_text = "Hello " + str(u.username) + ". Welcome to club: " + club.name            
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

    text = 'No text yet.'
    session = Session.objects.get(id="5702d03c-6aa4-4eaa-b70c-f1f3bbf57958")

    # if request.method == 'POST':
    #     form = TestForm(request.POST)
        
    #     if form.is_valid():

    #         text = form.cleaned_data['text']          
                
    #         return render(request, 'test.html', context={'form':form, 'text': text, 'session':session})
    #         #return HttpResponseRedirect(reverse('home:index'))
    # else:
        
    form = TestForm()

    return render(request, 'test.html', context={'form':form, 'text': text, 'session':session})

def add_member_debit(request, spk, mpk):
    session = get_object_or_404(Session, pk=spk)    
    member = get_object_or_404(SessionMember, pk=mpk)


    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():

            new_debit = form.cleaned_data['debit']
            member.debit = new_debit
            member.save()

            #return render(request, 'session_detail.html', context={'form':form, 'session':session})
            return redirect('home:session-detail', pk=session.id)
    else:        
        return HttpResponse('Not a POST method')

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
        return render(request, 'home/session_create.html', context={'club': club, 'form':form, 'is_member': is_member})

@login_required
def session_add_user(request, pk):

    session = get_object_or_404(Session, pk=pk)

    u = request.user

    if u not in session.parent_club.members.all():
        return HttpResponseBadRequest('Invalid request')
    
    else:    

        members_already_in_session = []
        
        for member in session.members.all():
            members_already_in_session.append(str(member.id))

        if request.method == 'POST':

            member_id = request.POST.get('member_id')

            current_id = str(session.id) + str(member_id)

            if current_id not in members_already_in_session:
                
                new_member_username =  request.POST.get('new_member_username')
                
                session_member = SessionMember(
                    id = current_id,
                    name = str(new_member_username),            
                    debit=0,
                    settled_sum=0,
                    parent_session = session,
                    main_account = CustomUser.objects.get(id=member_id)
                )

                session_member.save()
        #name = str(new_member_username), debit=0, settled_sum=0,parent_session = session

                session.members.add(session_member)
                session.save()

                #return render(request, 'home/session_detail.html', context={'session': session})
                return redirect('home:session-detail', pk=session.pk)
            else:
                return redirect('home:session-detail', pk=session.pk)
        else:
            return HttpResponseBadRequest('Invalid request')

@login_required
def settle_session(request, pk):  
    session = get_object_or_404(Session, pk=pk)

    u = request.user

    if u not in session.parent_club.members.all():
        return HttpResponseBadRequest('Invalid request')
    
    else:

        if session.type == 's':

            if session.status == 'o':
            
                total_spent = 0
                num_members = 0

                for member in session.members.all():
                    total_spent += member.debit
                    num_members += 1

                if num_members > 0:
                    mean_spent = total_spent / num_members
                
                    for member in session.members.all():
                        member.settled_sum = mean_spent - member.debit
                        member.save()

                    session.status='c'
                    session.save()

                return redirect('home:session-detail', pk=session.id)

            elif session.status =='c':
                    session.status='o'
                    session.save()
                    return redirect('home:session-detail', pk=session.id)
            
        elif session.type == 'z':
            if session.status == 'o':

                for member in session.members.all():
                        member.settled_sum = member.debit
                        member.save()

                session.status='c'
                session.save()
                return redirect('home:session-detail', pk=session.id)
            

        else:
            return HttpResponseBadRequest('Invalid request')

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
    form_class = TestForm

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
        context['form_debit'] = TestForm(initial={'parent_session': self.object})
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