from django.contrib.auth.models import User
from rest_framework import serializers
from idea_app import models
from django.shortcuts import get_object_or_404
from datetime import datetime




class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required = True, help_text='email or password')
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('phone','pk')

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = User
        fields = ('id','username','email','password','first_name','last_name','profile')
        # extra_kwargs = {'password': {'write_only': True,}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        models.UserProfile.objects.create(user=user, **profile_data)
        return user

class IdeaSerializer(serializers.ModelSerializer):
    creator = UserProfileSerializer()
    buyer = UserProfileSerializer()
    class Meta:
        model = models.Idea
        fields = '__all__'
        read_only_fields = ('date_added','likes','dislikes', 'buyer','creator')
    def update(self, instance, validated_data):
        if instance.buyer is not None or instance.date_sold is not None:
            raise serializers.ValidationError("You can not update sold object")
        if validated_data['is_auction'] is not None and validated_data['auction_end'] is None:
            raise serializers.ValidationError("You need end date for the auction")
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.price = validated_data.get('price', instance.price)
        instance.file = validated_data.get('file', instance.file)
        instance.is_public = validated_data.get('is_public', instance.is_public)
        instance.is_auction = validated_data.get('is_auction', instance.is_auction)
        instance.auction_end = validated_data.get('auction_end', instance.auction_end)
        return instance
