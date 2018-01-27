"""
accounts url
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^forgot-password/$', views.ForgotPasswordView.as_view(),
        name="forgot-password"),
    url(r'^me/$', views.UserProfileView.as_view(), name='profile'),
    url(r'^reset-password/$', views.PasswordResetView.as_view(), name="reset-password") 
]
