from django.urls import path
from  . import views
from knox import views as knox_views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('user-profile/<slug:slug>', views.user_profile_detail, name="user_profile_name"),
    path('stats', views.stats_view, name="stats"),
    path('students', views.user_profiles, name="students_page"),
    path('payments', views.payments, name="payments_page"),
    path('payments/<slug:slug>', views.payments, name="payments_one_page"),
    path('payment-details/<slug:slug>', views.payment_detail, name="payment_detail_page"),
    path('login', views.login, name="login"),
    path('logout', knox_views.LogoutView.as_view(), name="logout"),
    path('logout-all', knox_views.LogoutAllView.as_view(),name="logout_all"),
    path('change-password', views.change_password, name="change-password"),
    path('password-reset', views.password_reset, name="password-reset"),
    path('password-reset/<slug:slug>', views.password_reset_done, name="password-reset-done"),
]