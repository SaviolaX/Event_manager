from django.urls import path

from . import views

app_name = 'activity'

urlpatterns = [
    path('', views.display_activity, name='events_creations'),
]
