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
from .forms import InviteForm



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
        

class ClubInviteView(LoginRequiredMixin, generic.DetailView):

    model = Club

    def club_invite_view(request, primary_key):
        club = get_object_or_404(Club, pk=primary_key)
        form = InviteForm(request.POST)
        helper_text = 'Invite a user:'        

        if request.method == 'POST':
            form = InviteForm(request.POST)
            
            if form.is_valid():

                user_invite = form.cleaned_data['user']
                

                for u in CustomUser.object.all():
                    if user_invite == u.username:

                        valid_invite = Invite(parent_club=club, from_user=request.user, to_user=u, time_created = timezone.now)
                        valid_invite.save()                                        
                        club.invites_sent.add(valid_invite)
                        club.save() 
                        return render(request, 'home/club_detail.html', context={'club': club})
                    
                return render(request, 'home/club_invite.html', context={'form':form, 'helper_text':'User not found. Please input a valid username', 'club': club})
        
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
    fields = ['name', 'members', 'sessions'] 

class ClubDelete(LoginRequiredMixin, DeleteView):
    model = Club
    success_url = reverse_lazy('home:clubs')  