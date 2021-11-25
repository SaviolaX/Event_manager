from django import forms

from .models import Event


class CreateEventForm(forms.ModelForm):
    title = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Write title here'}))
    event_date = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Example: 21.01.2121'}))
    start = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Example: 20:00'}))
    finish = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Example: 22:00'}))

    class Meta:
        model = Event
        fields = ('privat_event', 'title', 'description',
                  'event_date', 'start', 'finish')
