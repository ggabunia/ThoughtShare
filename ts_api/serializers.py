from django.contrib.auth.models import User
from rest_framework import serializers
from idea_app import models
from django.shortcuts import get_object_or_404
from datetime import datetime




class RatingSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only = True )
    date_added = serializers.DateTimeField(read_only = True )
    is_positive = serializers.BooleanField()
    idea_id = serializers.IntegerField()
    def get_current_user(self):
        user = self.context['request'].user
        if user:
            return user
        else:
            raise serializers.ValidationError("User not found")
    def create(self, validated_data):
        user = self.get_current_user()
        profile = models.UserProfile.objects.get(user=user)
        if profile is None:
            raise serializers.ValidationError("User not found")
        idea_id = int(validated_data['idea_id'])
        is_positive = int(validated_data['is_positive'])
        prev_rating = models.IdeaRating.objects.filter(user=profile, idea_id = idea_id)
        if len(prev_rating)>0:
            raise serializers.ValidationError("User has already rated this idea")
        try:
            rating = models.IdeaRating.objects.create(user=profile, idea_id = idea_id, is_positive = is_positive)
        except:
            raise serializers.ValidationError("Idea not found")
        return rating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'





class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = User
        fields = ('id','username','email','password','first_name','last_name')
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.UserProfile
        fields = ('phone','pk', 'user')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        profile = models.UserProfile.objects.create(user=user, **validated_data)
        return profile

class IdeaSerializer(serializers.ModelSerializer):
    creator = UserProfileSerializer(read_only = True)
    buyer = UserProfileSerializer(read_only = True)
    update_file = serializers.BooleanField(default = False, write_only = True)
    class Meta:
        model = models.Idea
        fields = '__all__'
        read_only_fields = ('date_added','likes','dislikes', 'date_sold')

    def get_current_user_profile(self):
        user = self.context['request'].user
        if user:
            try:
                return models.UserProfile.objects.get(user = user)
            except:
                raise serializers.ValidationError("User not found")
        else:
            raise serializers.ValidationError("User not found")
    def create(self, validated_data):
        instance = models.Idea.objects.create(
            title = validated_data['title'],
            description = validated_data['description'],
            content = validated_data['content'],
            price = validated_data['price'],
            file = validated_data['file'],
            is_public = validated_data['is_public'],
            is_auction = validated_data['is_auction'],
            auction_end = validated_data['auction_end'],
            category = validated_data['category'],
            creator = self.get_current_user_profile(),
            )
        return instance
    def update(self, instance, validated_data):
        if instance.buyer is not None or instance.date_sold is not None:
            raise serializers.ValidationError("You can not update sold object")
        if validated_data['is_auction'] and validated_data['auction_end'] is None:
            raise serializers.ValidationError("You need end date for the auction")
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.price = validated_data.get('price', instance.price)

        instance.is_public = validated_data.get('is_public', instance.is_public)
        instance.is_auction = validated_data.get('is_auction', instance.is_auction)
        instance.auction_end = validated_data.get('auction_end', instance.auction_end)
        if validated_data['update_file']:
            instance.file = validated_data.get('file', instance.file)
        if not instance.is_auction:
            instance.auction_end = None
        instance.save()
        return instance
