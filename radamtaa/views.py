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

from radamtaa.models import Mtaa, Comment, Profile, Posts, Location
from .forms import MtaaForm, SignUpForm, ProfileUpdateForm, Profile

class LandingView(TemplateView):
    template_name = 'landing.html'

@login_required
def userhome(request, **kwargs):
    neighbourhoods = Mtaa.get_mtaa().order_by('-pub_date')
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

#     form= MtaaForm
#     def form_valid(self, form):
#         form.instance.name = self.request.user
#         return super().form_valid(form)

def mtaaview(request):
    current_user= request.user
    if request.method == 'POST':
        form = MtaaForm(request.POST, request.FILES)
        if form.is_valid():
            mtaa = form.save(commit=False)
            mtaa.user = current_user
            mtaa.profile = form
            mtaa.save()
            messages.success(request, 'You Have succesfully added your Mtaa. You may now Join It')
            return HttpResponseRedirect('index')
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


class FindMtaaView(DetailView):
    model = Mtaa
    template_name = 'joinedmtaa.html'
    slug_field = "slug"

    form = MtaaForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def mtaa(self, request, *args, **kwargs):
        form = MtaaForm(request.POST)
        if form.is_valid():
            mtaa = self.get_object()
            form.instance.user = request.user
            form.instance.mtaa = mtaa
            form.save()

            return redirect(reverse('mtaa', kwargs={"form":form, 'slug':mtaa.slug}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        return context
    
    def get_context_data(self, **kwargs):
        post_comments_count = Comment.objects.all().filter(comment=self.object.id).count()
        post_comments = Comment.objects.all().filter(comment=self.object.id)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'post_comments': post_comments,
            'post_comments_count': post_comments_count,
        })
        return context
    
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
