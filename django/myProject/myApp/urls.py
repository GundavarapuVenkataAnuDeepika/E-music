# urls.py
from django.urls import path
from .views import home, login,register,dashboard,settings_page,profile,signout,helpcenter,notifications,subscription,spotify_dashboard,about,contact,submit_contact_form,success,spotify_login,spotify_callback,search,HomeView

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('settings_page/',settings_page,name='settings_page'),
    path('profile/',profile,name='profile'),
    path('signout/',signout,name='signout'),
    path('helpcenter/',helpcenter,name='helpcenter'),
    path('subscription/',subscription,name='subscription'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('contact/submit/', submit_contact_form, name='submit_contact_form'),
    path('success/',success,name='success'),
    path('spotify/login/', spotify_login, name='spotify_login'),
    path('spotify/callback/', spotify_callback, name='spotify_callback'),
    path('spotifydashboard/', spotify_dashboard, name='spotify_dashboard'),
    path('homeview/',HomeView.as_view(),name='dashboardcopy'),
    path("search/",search,name='search'),
    path('notifications/', notifications, name='notifications'),
    
    
    
]