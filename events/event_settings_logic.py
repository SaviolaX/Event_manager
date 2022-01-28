from django.shortcuts import render, redirect

from .models import Event
from accounts.models import Profile
from . forms import CreateEventForm
from activity.models import EventCreationActivity


def create_event_and_assign_to_current_user(request):
    """Create event"""
    profile = Profile.objects.get(user=request.user)
    form = CreateEventForm()

    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = profile
            event.save()

            EventCreationActivity.objects.create(
                user=profile,
                event=event)

            return redirect('events:all_events')
    else:
        form = CreateEventForm()

    context = {'profile': profile, 'form': form}
    return render(request, 'events/create_event.html', context)


def edit_current_event(request, id):
    """Edit event"""
    event = Event.objects.get(id=id)
    form = CreateEventForm(instance=event)

    if request.method == 'POST':
        form = CreateEventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('events:event_page', event.id)

    context = {'form': form}
    return render(request, 'events/edit_event.html', context)


def delete_current_event(request, id):
    """Delete event"""
    event = Event.objects.get(id=id)
    event.delete()
    return redirect('accounts:my_events')
