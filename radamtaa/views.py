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
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm

from radamtaa.models import Mtaa
from .forms import MtaaForm, SignUpForm, ProfileUpdateForm, Profile

class LandingView(TemplateView):
    template_name = 'landing.html'

@login_required
def userhome(request):
    neighbourhoods = Mtaa.get_mtaa()
    return render(request, 'index.html', {"mitaa":neighbourhoods})

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

class MyProfile(DetailView):
    model = Profile
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user.profile


# class MtaaView(CreateView):
#     model = Mtaa
#     form_class= MtaaForm
#     template_name = 'mtaa.html'
#     success_url = reverse_lazy('index')

#     def get_object(self):
#         return self.request.user.mtaa

def mtaaview(request):
    current_user= request.user
    if request.method == 'POST':
        form = MtaaForm(request.POST, request.FILES)
        if form.is_valid():
            mtaa = form.save(commit=False)
            mtaa.user = current_user
            mtaa.save()
            messages.success(request, 'You Have succesfully added your Mtaa. You may now Join It')
        return redirect('index')
    else:
        form = MtaaForm()
    return render(request, 'mtaa.html', {"form": form})

class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    fields = ['userpic', 'houselocation','user', 'email', 'phonenumber', 'bio', 'gender']
    template_name = 'profileedit.html'
    # form_class = ProfileUpdateForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Your Account Settings were updated successfully!')
        return reverse('profile')

    # def get_queryset(self, *args, **kwargs):
        
    #     return Profile.objects.filter(id=self.kwargs['pk'])
