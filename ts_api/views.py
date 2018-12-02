from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse
from django.db.models import Q
from rest_framework import mixins, generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.contrib.auth.models import User
from decimal import *
from datetime import datetime
from . import serializers
from idea_app import models
import json
import pytz
# Create your views here.


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        "login": request.build_absolute_uri()+"rest-auth/login",
        "logout": request.build_absolute_uri()+"rest-auth/logout",
        "register user" : reverse('ts_api:register', request=request, format=format),
        "get current user" :reverse('ts_api:get_current_user', request=request, format=format),

        "get single user (admin only)" : reverse('ts_api:get_user', request=request, format=format),
        "all users (admin only)" : reverse('ts_api:user_list', request=request, format=format),

        "all ideas": reverse('ts_api:all_ideas', request=request, format=format),
        "get idea": reverse('ts_api:get_idea', request=request, format=format),
        "my ideas": reverse('ts_api:my_ideas', request=request, format=format),
        "user ideas": reverse('ts_api:user_ideas', request=request, format=format),
        "add idea (by authorized user)": reverse('ts_api:add_idea', request=request, format=format),
        "edit idea (of the authorized user)": reverse('ts_api:edit_idea', request=request, format=format),
        "search": reverse('ts_api:search', request=request, format=format),

        "get all categories": reverse('ts_api:all_categories', request=request, format=format),
        "get category": reverse('ts_api:get_category', request=request, format=format),

        "add rating (by authorize user, only if not yet rated)": reverse('ts_api:add_rating', request=request, format=format),
        "get current user's rating for an idea": reverse('ts_api:get_user_rating', request=request, format=format),
        "remove current rating for an idea": reverse('ts_api:remove_rating', request=request, format=format),

    })


class AddRating(generics.CreateAPIView):
    queryset = models.IdeaRating.objects.all()
    serializer_class = serializers.RatingSerializer
    permission_classes = (permissions.IsAuthenticated,)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def get_user_rating(request, idea_id):
    user = request.user
    if user is None:
        return JsonResponse({'error':'User not Found'}, status=status.HTTP_404_NOT_FOUND)
    profile = models.UserProfile.objects.get(user=user)
    if profile is None:
        return JsonResponse({'error':'User not Found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        rating = models.IdeaRating.objects.get(user = profile, idea_id = idea_id)
    except:
        return JsonResponse({'error':'User has not rated this Idea'}, status=status.HTTP_404_NOT_FOUND)

    rating = serializers.RatingSerializer(rating)
    return Response(rating.data)

@api_view(['GET','DELETE'])
@permission_classes((permissions.IsAuthenticated, ))
def delete_rating(request,idea_id):
    try:
        rating = models.IdeaRating.objects.get(idea_id = idea_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.RatingSerializer(rating)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        user = request.user
        try:
            profile = models.UserProfile.objects.get(user=user)
        except:
            return JsonResponse({'detail':'User not Found'},status = status.HTTP_404_NOT_FOUND)
        try:
            if rating.user != profile:
                return JsonResponse({'detail':'User is not the author of the rating'}, status = status.HTTP_400_BAD_REQUEST)
            rating.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            response = JsonResponse({'detail':'User not Found'},status = status.HTTP_400_BAD_REQUEST)
            return response



class RemoveRating(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.RatingSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.IdeaRating.objects.all()
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        user = self.request.user
        try:
            profile = models.UserProfile.objects.get(user=user)
            if instance.user != profile:
                return JsonResponse({'error':'User is not the author of the rating'}, status = status.HTTP_400_BAD_REQUEST)
            super().perform_destroy(instance)
        except:
            response = JsonResponse({'error':'User not Found'},status = status.HTTP_400_BAD_REQUEST)
            print(response)
            return response


class GetIdea(generics.RetrieveAPIView):
    serializer_class = serializers.IdeaSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'
    queryset = models.Idea.objects.all()

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
    permission_classes = (permissions.IsAuthenticated,)

class MyIdeas(generics.ListAPIView):
    serializer_class = serializers.IdeaSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        try:
            user = self.request.user
            profile = models.UserProfile.objects.get(user=user)
            queryset = models.Idea.objects.filter(creator = profile).order_by('-date_added')
            return queryset
        except:
            raise Http404("User not found")

class UserIdeas(generics.ListAPIView):
    serializer_class = serializers.IdeaSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        try:
            user = User.objects.get(id=self.pk)
            profile = models.UserProfile.objects.get(user=user)
            queryset = models.Idea.objects.filter(creator = profile).order_by('-date_added')
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
    permission_classes = (permissions.IsAuthenticated,)


class CategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all().order_by('priority')

class GetCategory(generics.RetrieveAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all().order_by('priority')
    lookup_field = 'pk'

class RegisterUser(generics.CreateAPIView):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

class GetUser(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    lookup_field = 'pk'

class GetCurrentUser(generics.RetrieveAPIView):
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.UserProfile.objects.all()
    def get_object(self):
        user = self.request.user
        return get_object_or_404(models.UserProfile, user=user)

class SearchIdeas(generics.ListAPIView):
    serializer_class = serializers.IdeaSerializer

    def get_queryset(self):
        queryset = models.Idea.objects.all()
        format = "%Y-%m-%d"
        utc=pytz.UTC
        price_lowest = None
        price_highest = None
        date_start = None
        date_end = None
        min_rating = None
        search_text = self.request.query_params.get('search_text', None)
        try:
            price_lowest = Decimal(self.request.query_params.get('price_lowest', None))
        except:
            price_lowest = None
        try:
            price_highest = Decimal(self.request.query_params.get('price_highest', None))
        except:
            price_highest = None
        try:
            min_rating = int(self.request.query_params.get('min_rating', None))
        except:
            min_rating = None
        try:
            date_start = utc.localize(datetime.strptime(self.request.query_params.get('date_start', None), format))
        except Exception as ex:
            date_start = None
        try:
            date_end = utc.localize(datetime.strptime(self.request.query_params.get('date_end', None), format))
        except:
            date_end = None
        if search_text:
            queryset = queryset.filter(Q(title__icontains=search_text)|Q(description__icontains=search_text))
        if price_lowest:
            queryset = queryset.filter(price__gte=price_lowest)
        if price_highest:
            queryset = queryset.filter(price__lte=price_highest)
        if date_start:
            queryset = queryset.filter(date_added__gte=date_start)
        if date_end:
            queryset = queryset.filter(date_added__lte=date_end)
        if min_rating:
            objects_ids = [obj.id for obj in list(queryset) if obj.likes-obj.dislikes >= min_rating]
            queryset = queryset.filter(id__in=objects_ids)
        return queryset
