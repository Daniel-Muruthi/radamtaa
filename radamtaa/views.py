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
from .forms import SignUpForm

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
