from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('profile/', views.profile, name="profile"),
    path('register/', views.register, name="register"),
    path('ok/', views.ok, name="ok"),
    path('betConfirm/<int:event_id>/<int:team_id>/', views.betConfirm, name="betConfirm"),
    path('betPage/<int:event_id>/', views.betPage, name='betPage'),
    path('login/', LoginView.as_view(template_name="homepage.html"), {'next_page': settings.LOGIN_REDIRECT_URL}, name="login"),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name="logout"),
    path('betSuccess', views.Bet_success, name="betSuccess"),
    path('gameList/<str:game>/', views.gameList, name="gameList"),
    path('search/<str:keyword>/', views.search, name='search'),
    path('ajax/team/', views.ajax_load_teams, name='ajax_team')
]
