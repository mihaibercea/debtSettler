from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [    
    path('', views.index, name='index'),
    path('myclubs/', views.myclublist_view, name='myclubs'),
    path('clubs/', views.ClubListView.as_view(), name='clubs'),
    path('club/<str:pk>', views.ClubDetailView.as_view(), name='club-detail'),
    path('session/<str:pk>', views.SessionDetailView.as_view(), name='session-detail'),
    path('clubs/create/', views.ClubCreate.as_view(), name='club-create'),
    path('club/<int:pk>/update/', views.ClubUpdate.as_view(), name='club-update'),
    path('club/<int:pk>/delete/', views.ClubDelete.as_view(), name='club-delete'),
    path('club/<int:pk>/invite/', views.club_invite_view, name='club-invite'),
    path('test', views.test_view, name='test')
]