from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm 

from .models import Event, Location
from .forms import CreateEventForm, CreateEventWithLocationForm, CreateLocationForm, UpdateEventForm, UpdateLocationForm

def index(request):
    # Get recent events from model as a queryset ordered by number of voters
    recent_events_ids = [e.id for e in Event.objects.all() if e.was_published_recently()]
    filtered = Event.objects.filter(id__in=recent_events_ids)
    queryset = filtered.annotate(voter_count = Count('voters')).order_by('-voter_count')

    # Handle users who click 'Join'
    if request.method == "POST" and 'join' in request.POST and request.user.is_authenticated:
        event = Event.objects.get(pk=request.POST['event_id'])
        event.voters.add(request.user)
        messages.success(request, "Joined event!")
        return redirect('polls:event_detail', pk=request.POST['event_id'])
    # Handle users who click 'Exit'
    elif request.method == "POST" and 'exit' in request.POST and request.user.is_authenticated:
        event = Event.objects.get(pk=request.POST['event_id'])
        event.voters.remove(request.user)
        messages.success(request, "Exited event!")
        return redirect('polls:event_detail', pk=request.POST['event_id'])

    # Render page as usual
    return render(request, 'polls/index.html', context={'events' : queryset})


def event_detail(request, pk):
    # Get event model
    event = get_object_or_404(Event, pk=pk)
    
    # Handle actions on event detail view
    if request.method == "POST" and 'join' in request.POST and request.user.is_authenticated:
        event.voters.add(request.user)
        messages.success(request, "Joined event!")
        return redirect('polls:event_detail', pk=pk)
    elif request.method == "POST" and 'exit' in request.POST and request.user.is_authenticated:
        event.voters.remove(request.user)
        messages.success(request, "Exited event!")
        return redirect('polls:event_detail', pk=pk)
    elif request.user.is_authenticated == False:
        return redirect('login')
    return render(request, 'polls/event_detail.html', context={'event': event})
    

def create_location(request):
    # Initialize Model forms under the create view
    location_form = CreateLocationForm()
    event_form = CreateEventForm()
    
    # Handle users who create events
    if request.user.is_authenticated:
        if request.method == "POST":
            location_form = CreateLocationForm(request.POST)
            event_form = CreateEventWithLocationForm(request.POST)

            # Handle multi-model form logic by avoiding commit and commiting after assignment
            if location_form.is_valid() and event_form.is_valid():
                a = location_form.save()
                b = event_form.save(commit=False)
                b.location = a 
                b.creator = request.user
                b.save()
                b.voters.add(request.user)
                messages.success(request, "Event successfully created!")
                return redirect('polls:index')
            else: 
                messages.info(request, "Location with that name already exists. Try another one?")
                return redirect('polls:create_location')
        # Handle default view for authenticated users
        else: 
            context = {
                'location_form': location_form,
                'event_form': event_form
            }
            return render(request, 'polls/create_location.html', context=context)
    else:
        return redirect('login')

def create_event(request):
    # Initialize Model forms under the create view
    event_form = CreateEventForm()
    
    # Handle users who create events
    if request.user.is_authenticated:
        if request.method == "POST":
            event_form = CreateEventForm(request.POST)
            if event_form.is_valid():
                a = event_form.save(commit=False)
                a.creator = request.user
                a.save()
                a.voters.add(request.user)
                messages.success(request, "Event successfully created!")
                return redirect('polls:index')
            else: 
                messages.info(request, "Something went wrong. Please contact your website administrator.")
                return redirect('polls:index')
        # Handle default view for authenticated users
        else: 
            return render(request, 'polls/create_event.html', context={'event_form': event_form})
    else:
        return redirect('login')

def update_event(request, pk):
    # Retrieve models and initialize form with model instances
    event = get_object_or_404(Event, pk=pk)
    location = get_object_or_404(Location, pk=event.location.id)
    event_form = UpdateEventForm(instance=event)
    location_form = UpdateLocationForm(instance=location)

    if request.user.is_authenticated:
        print(request.POST)
        if request.method == "POST" and 'edit' in request.POST:
            location_form = UpdateLocationForm(request.POST, instance=location)
            event_form = UpdateEventForm(request.POST, instance=event)

            if location_form.is_valid() and event_form.is_valid():
                location_form.save()
                event_form.save()
                messages.success(request, "Event edited successfully!")
                return redirect('polls:event_detail', pk=pk)
        # Redirect to delete view
        elif request.method == "POST" and 'delete' in request.POST:
            return redirect('polls:delete', pk=pk)
        else: 
            context = {
                'event': event,
                'location_form': location_form,
                'event_form': event_form,
            }
            return render(request, 'polls/update_event.html', context=context)
    else:
        return redirect('login')

def delete_event(request, pk):
    # Retrieve object to be deleted
    event = get_object_or_404(Event, pk=pk)

    if request.user.is_authenticated:
        if request.method == "POST" and 'confirm' in request.POST:
            event.delete()
            messages.success(request, "Event deleted successfully!")
            return redirect('polls:index')
        elif request.method == "POST" and 'decline' in request.POST:
            return redirect('polls:update', pk=pk)
        else:
            return render(request, 'polls/delete_event.html', context={'event': event})
    else:
        return redirect('login')


def register(request):
    # Handle user creation
    # TODO refactor to use model form
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Welcome to Smakan!")
            return redirect('polls:index')
        else:
            messages.warning(request, "The account already exists.")
            return render(request, 'polls/register.html', {})
    elif request.user.is_authenticated == True:
        return redirect('polls:index')
    else:
        form = UserCreationForm()
        return render(request, 'polls/register.html', {})


def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('polls:index')
    elif request.user.is_authenticated == True:
        return redirect('polls:index')
    else:
        return render(request, 'polls/login.html', {})


def sign_out(request):
    if request.user.is_authenticated == True:
        logout(request)
    return render(request, 'polls/logout.html', {})