from django.db.models.base import Model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView,UpdateView, CreateView, DeleteView, TemplateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ProfileUpdateForm, Profile

class LandingView(TemplateView):
    template_name = 'landing.html'

@login_required
def userhome(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form':form})

@login_required
def profile(request):

    return render(request, 'profile.html')


@login_required
def EditProfile(request):
    profileform = ProfileUpdateForm(instance=request.user.profile)
    pform = None
    if request.method == 'POST':
        profileform=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if profileform.is_valid():
            pform=profileform.save(commit=False)
            pform.user = request.user
            pform.profile = profileform
            pform.save()


            return redirect('profile')

        else:
            profileform = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user': request.user,
        'profileform': profileform, 
        'pform':pform,
    }
    return render(request, 'profileedit.html', context)
