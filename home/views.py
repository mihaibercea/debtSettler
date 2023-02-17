from django.shortcuts import render, reverse, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth import views
from accounts.models import CustomUser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from home.models import Club, Session, Invite
from django.http import HttpResponse, HttpResponseRedirect
from accounts.models import CustomUser

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import InviteForm, TestForm



def index(request):

# Generate counts of some of the main objects
    num_clubs = Club.objects.all().count()    

   
#     The 'all()' is implied by default.
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

class ClubDetailView(LoginRequiredMixin, generic.DetailView):
    model = Club   

    def club_detail_view(request, primary_key):
        club = get_object_or_404(Club, pk=primary_key)        
        return render(request, 'home/club_detail.html', context={'club': club})   
            

# class ClubInviteView(LoginRequiredMixin, generic.DetailView):

#     model = Club
#     template_name = "home/club_invite.html"

def test_view(request):
    helper_text = 'Testing...'
    text = 'No text yet.'

    if request.method == 'POST':
        form = TestForm(request.POST)
        
        if form.is_valid():

            text = form.cleaned_data['text']
            helper_text = 'Test has passed.' 
                
            #return render(request, 'home/test.html', context={'form':form, 'helper_text':helper_text, 'text': text})
            return render(request, 'home/index.html')
    else:
        form = TestForm()
    return render(request, 'home/test.html', context={'form':form, 'helper_text':helper_text, 'text': text}) 

@login_required
def club_invite_view(request, pk):
    club = get_object_or_404(Club, pk=pk)        
    helper_text = 'Invite a user:'        

    if request.method == 'POST':
        form = InviteForm(request.POST)
        
        if form.is_valid():

            user_invited = form.cleaned_data['user']                

            for u in CustomUser.objects.all():
                if user_invited == str(u.username):

                    valid_invite = Invite(parent_club=club, from_user=request.user, to_user=u, time_created = timezone.now)

                    helper_text = 'Invite a user:'

                    valid_invite.save()                                        
                    club.invites_sent.add(valid_invite)
                    club.save() 
                    return render(request, 'home/club_invite.html',  context={'form':form, 'helper_text':'Invite sent. Invite another user?', 'club': club})
                
            return render(request, 'home/club_invite.html', context={'form':form, 'helper_text':'User not found. Please input a valid username', 'club': club})
    else:
        form = InviteForm()
    return render(request, 'home/club_invite.html', context={'club': club, 'form':form, 'helper_text':helper_text})       

class SessionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Session

    def session_detail_view(request, primary_key):
        session = get_object_or_404(Session, pk=primary_key)
        return render(request, 'home/session_detail.html', context={'session': session})
    

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