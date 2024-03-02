from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('confirm/', views.Confirm.as_view(), name='confirm'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile_view'),
    path('profile/<int:pk>/settings', views.ProfileSettings.as_view(), name='profile_settings'),
    path('updateProfile/<int:pk>', views.UpdateProfile, name="update_profile"),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name="accounts/resetPassword.html"),
         name="password_reset"),
    path('reset-password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/resetPasswordSent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/setNewPassword.html"),
         name="password_reset_confirm"),
    path('reset-password-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/resetPasswordDone.html"),
         name="password_reset_complete"),

]
