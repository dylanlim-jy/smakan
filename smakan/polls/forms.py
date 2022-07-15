from django import forms
from .models import Event, Location

class CreateEventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
        self.fields['note'].widget.attrs = {
            'class': 'u-full-width', 
            'placeholder': 'This info will be displayed to other people.'
            }
        self.fields['location'].widget.attrs = {
            'class': 'u-full-width', 
            'placeholder': 'Choose from previously created'
            }
    class Meta:
        model = Event
        fields = ('location', 'note')
        labels = {
            'note': 'Extra Info',
            'location': 'Choose from a previous location'
        }

class CreateEventWithLocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateEventWithLocationForm, self).__init__(*args, **kwargs)
        self.fields['note'].widget.attrs = {
            'class': 'u-full-width', 
            'placeholder': 'This info will be displayed to other people.'
            }
    class Meta:
        model = Event
        fields = ('note',)
        labels = {
            'note': 'Extra Info',
        }

class CreateLocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateLocationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'u-full-width', 
            'placeholder': 'Where are we going?'
            }
        self.fields['url'].widget.attrs = {
            'class': 'u-full-width', 
            'placeholder': 'What\'s the Google maps / waze URL?'
            }
    class Meta:
        model = Location
        fields = '__all__'
        labels = {
            'name': 'Dinner Place Name',
            'url': 'URL',
        }

class UpdateEventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateEventForm, self).__init__(*args, **kwargs)
        self.fields['note'].widget.attrs = {
            'class': 'u-full-width', 
            'placeholder': 'This info will be displayed to other people.'
            }
    class Meta:
        model = Event
        fields = ('note',)
        labels = {
            'note': 'Extra Info',
        }

class UpdateLocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateLocationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'u-full-width', 
            'placeholder': 'Where are we going?'
            }
        self.fields['url'].widget.attrs = {
            'class': 'u-full-width', 
            'placeholder': 'What\'s the Google maps / waze URL?'
            }
    class Meta:
        model = Location
        fields = '__all__'
        labels = {
            'name': 'Dinner Place Name',
            'url': 'URL',
        }