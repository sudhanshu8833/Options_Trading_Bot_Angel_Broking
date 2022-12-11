from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.index, name='index'),
    path('position/', views.position, name='position'),
    path('start_strategy/', views.start_strategy, name='start_strategy'),
    path('order/', views.closed_positions, name='start_strategy'),

    path('test/', views.test, name='testing_celery'),
]