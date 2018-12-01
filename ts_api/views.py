from django.shortcuts import render
from django.http import Http404
from rest_framework import mixins, generics, permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from django.contrib.auth.models import User
from . import serializers
from idea_app import models
# Create your views here.


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        "login": request.build_absolute_uri()+"rest-auth/login",
        "logout": request.build_absolute_uri()+"rest-auth/logout",
        "all ideas": reverse('ts_api:all_ideas', request=request, format=format),
        "user's ideas": reverse('ts_api:user_ideas', request=request, format=format),
        "all users" : reverse('ts_api:user_list', request=request, format=format),
        "get single user" : reverse('ts_api:get_user', request=request, format=format),
        "register user" : reverse('ts_api:register', request=request, format=format),
        "add idea": reverse('ts_api:add_idea', request=request, format=format),
        "get all categories": reverse('ts_api:all_categories', request=request, format=format),
        "get category": reverse('ts_api:get_category', request=request, format=format),
        "edit idea": reverse('ts_api:edit_idea', request=request, format=format),
        "authorize": request.build_absolute_uri()+"rest-auth/login",
    })




class AllIdeas(generics.ListAPIView):
    serializer_class = serializers.IdeaSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        try:
            queryset = models.Idea.objects.all().order_by('-date_added')
            return queryset
        except:
            raise Http404("Ideas not Found")

class AddIdea(generics.CreateAPIView):
    queryset = models.Idea.objects.all()
    serializer_class = serializers.IdeaSerializer

class UserIdeas(generics.ListAPIView):
    serializer_class = serializers.IdeaSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        try:
            pk = self.kwargs['pk']
            user = User.objects.get(pk=pk)
            profile = models.UserProfile.objects.get(user=user)
            queryset = models.Idea.objects.filter(i_creator = profile).order_by('-i_date_added')
            return queryset
        except:
            raise Http404("User not found")

class UpdateIdea(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.IdeaSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        profile = models.UserProfile.objects.get(user =  self.request.user)
        queryset = models.Idea.objects.filter(creator = profile, buyer__isnull=True, date_sold__isnull=True)
        return queryset


class UserList(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

class CategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all().order_by('priority')

class GetCategory(generics.RetrieveAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all().order_by('priority')
    lookup_field = 'pk'

class RegisterUser(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

class GetUser(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'
