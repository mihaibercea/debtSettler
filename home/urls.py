from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [    
    path('', views.index, name='index'),
    path('home', views.index, name='index2'),
    path('myclubs/', views.myclublist_view, name='myclubs'),   
    path('myinvites/', views.myinvites_list, name='myinvites'),   
    path('clubs/', views.ClubListView.as_view(), name='clubs'),
    path('club/<str:pk>', views.ClubDetailView.as_view(), name='club-detail'),
    path('session/<str:pk>', views.SessionDetailView.as_view(), name='session-detail'),
    path('clubs/create/', views.ClubCreate.as_view(), name='club-create'),
    path('club/<int:pk>/update', views.ClubUpdate.as_view(), name='club-update'),
    path('club/<int:pk>/delete', views.ClubDelete.as_view(), name='club-delete'),
    path('club/<int:pk>/invite', views.club_invite, name='club-invite'),
    path('club/<int:pk>/create-session', views.create_session, name='club-create-session'),    
    path('test', views.test_view, name='test'),
    path('accept_invite/<str:pk>', views.accept_invite, name='accept-invite'),
    path('session/<str:pk>/adduser', views.session_add_user, name='session-add-user'),
    path('session/<str:pk>/settle', views.settle_session, name='settle-session'),
    path('session/<str:spk>/<str:mpk>/debit', views.add_member_debit, name='add-member-debit'),  
]