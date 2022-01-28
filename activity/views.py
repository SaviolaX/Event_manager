from django.shortcuts import render

from .models import EventCreationActivity


def display_activity(request):
    """Display all created events activities"""
    activities = EventCreationActivity.objects.all().order_by('-created')

    context = {'activities': activities}
    return render(request, 'activity/create_event_activity.html', context)
