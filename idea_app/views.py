from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView,CreateView
from . import models
# Create your views here.


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
