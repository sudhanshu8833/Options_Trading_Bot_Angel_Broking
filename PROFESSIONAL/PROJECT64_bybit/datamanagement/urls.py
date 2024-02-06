from django.urls import path

from . import views

urlpatterns = [
    path('handleLogin/', views.handleLogin, name='handleLogin'),
    path('handleLogout/', views.handleLogout, name='handleLogout'),
    path('', views.login_page, name='login_page'),
    path('rest_update/', views.rest_update, name='rest_update'),
    path('start_strategy/', views.start_strategy, name='start_strategy'),
    path('TESTING/', views.TESTING, name='TESTING'),
]