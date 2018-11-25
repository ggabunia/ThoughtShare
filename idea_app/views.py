from django.shortcuts import render, get_object_or_404
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
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('thought_share:index'))
        form = forms.UserForm()
        return render(request, 'idea_app/authorization.html', context={'form': form})
    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('thought_share:index'))
        form = forms.UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                if duplicate_mail(data['form_email']):
                    form.add_error(field = 'form_email', error = "Email already in use")
                try:
                    validate_password(data['form_password'])
                except ValidationError as ve:
                    form.add_error(field = 'form_password', error = ve.messages)
                if len(form.errors) > 0:
                    return render(request, 'idea_app/authorization.html', context={'form': form})
                user = User.objects.create_user(username=data['form_username'],
                                             email=data['form_email'],
                                             password=data['form_password'],
                                             first_name = data['form_first_name'],
                                             last_name = data['form_last_name'])
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error(field = 'form_username', error="Username already in use")
                    print("here")
                else:
                    form.add_error(field = none, error = "Unspecified error, try again later")
                return render(request, 'idea_app/authorization.html', context={'form': form})
            except Exception as e:
                form.add_error(field = None, error = "Unspecified Integrity error, try again later" )
                return render(request, 'idea_app/authorization.html', context={'form': form})
            try:
                profile = models.UserProfile(user = user,  phone = data['form_phoneNumber'])
                profile.save()

            except Exception as ex:
                profile = None
                print(ex)
            if profile is None or profile.pk is None:
                user.delete()
                form.add_error(field = None, error = "Error registering, try again later." )
                return render(request, 'idea_app/authorization.html', context={'form': form})
            login(request=request,user=user)
            return HttpResponseRedirect(reverse('thought_share:index'))
        else:
            return render(request, 'idea_app/authorization.html', context={'form': form})

class LoginForm(TemplateView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('thought_share:index'))
        form = forms.UserForm()
        return render(request, 'idea_app/authorization.html', context={'form':form})
    def post(self, request, **kwargs):
        username = request.POST.get('form-username')
        password = request.POST.get('form-password')
        form = forms.UserForm()
        user = authenticate(username = username, password = password)
        if user:
            print(user)
            if user.is_active:
                login(request=request, user=user)

                return HttpResponseRedirect(reverse('thought_share:index'))
            else:
                print("not active")
                return render(request, 'idea_app/authorization.html',  context = {'login_error': "User Not Active", 'form':form})
        else:
            print("not found?")
            return render(request, 'idea_app/authorization.html',  context = {'login_error': "User Not Found",'form':form})

class AddIdeaForm(LoginRequiredMixin,TemplateView):
    def get(self, request, **kwargs):
        form = forms.IdeaForm()
        return render(request, 'idea_app/add_idea.html',context={'form':form})
    def post(self,request, **kwargs):
        form = forms.IdeaForm(request.POST,request.FILES)
        profile = models.UserProfile.objects.get(user=request.user)
        idea = form.save(commit=False)
        idea.i_creator = profile
        idea.save()
        return HttpResponseRedirect(reverse('thought_share:my_ideas'))


class EditIdeaForm(LoginRequiredMixin,TemplateView):
    def get(self, request, **kwargs):
        pk = kwargs['pk']
        profile = None
        try:
            profile = get_object_or_404(models.UserProfile, user = request.user)
        except:
            HttpResponseRedirect(reverse('thought_share:index'))
        if profile is None:
            pass
        try:
            idea = models.Idea.objects.get(pk=pk)
        except:
            return HttpResponse("Idea Does Not exist")
        if idea.i_creator != profile:
            return HttpResponse("Not the creator")
        if idea.i_date_sold is not None:
            return HttpResponse("Idea already sold")
        form = forms.IdeaForm(instance=idea)
        return render(request, 'idea_app/edit_idea.html',context={'form':form, 'pk':pk})
    def post(self,request, **kwargs):
        try:
            pkStr = request.POST.get('pk')
            pk = int(pkStr)
        except:
            return HttpResponse("error getting pk")
        try:
            profile = get_object_or_404(models.UserProfile, user = request.user)
        except:
            HttpResponseRedirect(reverse('thought_share:index'))
        if profile is None:
            pass
        try:
            idea = models.Idea.objects.get(pk=pk)
        except:
            return HttpResponse("Idea Does Not exist")
        if idea.i_creator != profile:
            return HttpResponse("Not the creator")
        if idea.i_date_sold is not None:
            return HttpResponse("Idea already sold")
        form = forms.IdeaForm(request.POST, instance=idea)
        form.save()
        return HttpResponseRedirect(reverse('thought_share:my_ideas'))

def my_ideas(request):
    return HttpResponse("my ideas page")


@login_required
def user_logout(request):
    logout(request)
    for sesskey in request.session.keys():
        try:
            del request.session[sesskey]
        except:
            continue
    return HttpResponseRedirect(reverse('thought_share:index'))
