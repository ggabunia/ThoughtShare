from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView,CreateView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from . import models
from . import forms
# Create your views here.

def duplicate_mail(email):
    users = list(User.objects.filter(email = email))
    if len(users) > 0:
        return True
    return False


def index(request):
    return render(request, 'idea_app/index.html')

class IdeasList(ListView):
    model = models.Idea
    ordering = ['-date_added']
    template_name = 'idea_app/idea_list.html'

class SearchIdeas(TemplateView):
    def get(self,request, **kwargs):
        return render(request, 'idea_app/search.html', context = {})
    def post(self, request, **kwargs):
        ideas = models.Idea.objects.all()
        post = request.POST
        if post.get('title') is not None:
            ideas = ideas.filter(title__icontains = post.get('title'))

        return render(request, 'idea_app/search.html', context = {'ideas': ideas,})


class RegisterForm(TemplateView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        form = forms.UserForm()
        return render(request, 'idea_app/register.html', context={'form': form})
    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        form = forms.UserForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data
            try:
                if duplicate_mail(data['email']):
                    form.add_error(field = 'email', error = "Email already in user")
                try:
                    validate_password(data['password'])
                except ValidationError as ve:
                    form.add_error(field = 'password', error = ve.messages)
                if len(form.errors) > 0:
                    return render(request, 'idea_app/register.html', context={'form': form})
                user = User.objects.create_user(username=data['username'],
                                             email=data['email'],
                                             password=data['password'],
                                             first_name = data['first_name'],
                                             last_name = data['last_name'])

            except IntegrityError as e:

                if 'unique constraint' in str(e).lower():
                    form.add_error(field = 'username', error="Username already in use")
                else:
                    form.add_error(field = none, error = "Unspecified error, try again later")
                return render(request, 'idea_app/register.html', context={'form': form})
            except Exception as e:
                form.add_error(field = None, error = "Unspecified Integrity error, try again later" )
                return render(request, 'idea_app/register.html', context={'form': form})
            try:
                profile = models.UserProfile(user = user,  phone = data['phone'])
                profile.save()

            except Exception as ex:
                print(ex)




            if profile is None or profile.pk is None:
                user.delete()
                form.add_error(field = None, error = "Error registering, try again later." )
                return render(request, 'idea_app/register.html', context={'form': form})

            login(request=request,user=user)
            return HttpResponseRedirect(reverse('thought_share:index'))
        else:
            return render(request, 'idea_app/register.html', context={'form': form})



class LoginForm(TemplateView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'idea_app/login.html')
    def post(self, request, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request=request, user=user)

                return HttpResponseRedirect(reverse('thought_share:index'))
            else:
                return render(request, 'idea_app/login.html',  context = {'error': "User Not Active",})
        else:
            return render(request, 'idea_app/login.html',  context = {'error': "User Not Found",})


@login_required
def user_logout(request):
    logout(request)
    for sesskey in request.session.keys():
        try:
            del request.session[sesskey]
        except:
            continue
    return HttpResponseRedirect(reverse('thought_share:index'))
