from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.urls import reverse
from django import forms
from .forms import RegisterForm, LoginForm, VotingForm, CreatePollForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


# Create your views here.

def register_view(request):

    try:

        form = RegisterForm()
        if request.method == "POST":
           form = RegisterForm(request.POST)
           if form.is_valid():
              instance = form.save()
              username = form.cleaned_data.get('username')
              email= form.cleaned_data.get('email')
              phone = form.cleaned_data.get('phone')
              profile, created = Profile.objects.get_or_create(user=instance)
              profile.name = username
              profile.email = email
              profile.phone = phone
              profile.save()
              return redirect('login')

        context ={'form': form}
        return render(request,"register.html", context)
    except Exception as e:
        return HttpResponse(e)

def login_view(request):
    try:
        form = LoginForm()
        if request.method =="POST":
            form = LoginForm(request.POST)
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Authentication Failed!")

        context = {'form': form}
        return render(request,"login.html", context)
    except Exception as e:
        return HttpResponse(e)


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_view(request):
    polls = Poll.objects.all()
    context = {'polls': polls}

    return render(request,"home.html", context)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def vote_view(request, poll_id):
    try:
        poll = get_object_or_404(Poll,pk=poll_id)

        if request.method == "POST":
            option_selected = request.POST.get('poll')
            if option_selected == "option_1":
                poll.option_1_votes += 1
            elif option_selected == "option_2":
                poll.option_2_votes += 1
            elif option_selected == "option_3":
                poll.option_3_votes += 1
            elif option_selected == "option_4":
                poll.option_4_votes += 1
            else:
                messages.error(request, "Please select an option.")
                return redirect(reverse('vote', kwargs={"poll_id": poll.id}))

            poll.save()
            return redirect(reverse('results', kwargs={"poll_id": poll.id}))

        context = {'poll': poll}
        return render(request,"vote.html", context)
    except Exception as e:
        return HttpResponse(e)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createpoll_view(request):
    try:
        form = CreatePollForm()
        user = request.user

        if request.method == "POST":
            form = CreatePollForm(request.POST)
            if form.is_valid():
               profile, created = Profile.objects.get_or_create(user=user)
               if not created:
                  form.instance.user = profile
                  form.save()
                  messages.success(request,"Poll created successfully.")
                  return redirect("create")
               else:
                   messages.error(request, "Error!!!User not in db.")
        else:
            profile, created = Profile.objects.get_or_create(user=user)
            polls = profile.poll_set.all()
            if len(polls) < 5:
                context = {'form': form}
                return render(request, "create.html", context)
            else:
                print("questions exceeded 5")
                messages.error(request, 'Only 5 polls allowed per user')
                return redirect("home")
    except Exception as e:
        return HttpResponse(e)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def results_view(request, poll_id):
    poll = get_object_or_404(Poll,pk=poll_id)
    context = {'poll': poll}
    return render(request, "results.html", context)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile_view(request):
    try:
         profile, created = Profile.objects.get_or_create(user=request.user)
         polls = profile.poll_set.all()
         print(polls)
         context = {'profile': profile , 'polls': polls}
         return render(request,"profile.html",context)
    except Exception as e:
        return HttpResponse(e)




