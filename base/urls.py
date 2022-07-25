from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('signup/', Signup, name='signup'),
    path('login/', Login, name='login'),
    path('logout/', Logout_fun, name='logout'),
    path('profile/', Profile_fun, name='profile'),
    path('updateprofile/', Updateprofile, name='updateprofile'),
    path('post', Postlist, name="post"),
    path('createpost', Postcreate, name='createpost'),
    path('viewprofile/<str:user_name>/', Viewprofile, name='viewprofile'),
    path('makepayments/<str:user_name>/<str:post_id>/',
         Makepayments, name='makepayments'),
    path('deletepost/<str:post_id>/', Deletepost, name='deletepost'),
    path('faq/', Faq, name='faq'),
    path('about/', About, name='about'),
    path('contact/', Contact, name='contact'),
    path('algorithm/', Algorithm, name='algorithm'),
    
     path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),
    
]
