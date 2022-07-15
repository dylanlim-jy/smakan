from django.urls import path, include
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('event/<int:pk>', views.event_detail, name='event_detail'),
    path('create_event', views.create_event, name='create_event'),
    path('create_location', views.create_location, name='create_location'),
    path('update/<int:pk>', views.update_event, name='update'),
    path('delete/<int:pk>', views.delete_event, name='delete'),
    path('register', views.register, name='register'),
    path('logout', views.sign_out, name='logout'),
    path('login', views.sign_in, name='login'),
]
