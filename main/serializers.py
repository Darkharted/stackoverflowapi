import re
from django.db.models import fields
from django.http import request
from rest_framework import serializers
from .models import (Problem, Picture, Reply, Comment)
# from abc import ABC

# class A(ABC,serializers.ModelSerializer):
#     author = .......

class PictureSerizalizer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = ('image',)
    


class ProblemSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Problem
        fields = ('id', 'title', 'description', 'author')

    def create(self, validated_data):
        request = self.context.get('request')
        pictures_files = request.FILES
        problem = Problem.objects.create(
            author=request.user,
            **validated_data, 
        )
        for picture in pictures_files.getlist('pictures'):
            Picture.objects.create(
                image=picture,
                problem=problem
            )
        return problem

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)

        images_data = request.FILES
        instance.pictures.all().delete()
        for image in images_data.getlist('pictures'):
            Picture.objects.create(
                image=image, 
                problem=instance
                )
        return instance
    # request.user
    # Problem.objects.create(
    #     author=request.user
    # )

    # request.FILES -> [1,2,3,4,5]
    # for i in [1,2,3,4,5]:
    #     Picture.objects.create(
    #         image=i,
    #         problem=problem
    #     )
    
    def to_reperepresentation(self, instance):
        reperepresentation = super().to_representation(instance)
        reperepresentation['pictures'] = PictureSerizalizer(
            instance.pictures.all(), many=True
        ).data
        action = self.context.get('action')
        if action=='retrieve':
            reperepresentation['replies'] = ReplySerializer(
                instance.replies.all(), many=True
                ).data
        elif action == 'list':
            reperepresentation['replies'] = instance.replies.count()
        return reperepresentation



class ReplySerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')

    class Meta:

        model = Reply
        fields =  "__all__"
    
    def create(self, validated_data):
        request = self.context.get('request')
        reply = Reply.objects.create(
            author=request.user,
            **validated_data
        )
        return reply

    def to_reperepresentation(self, instance):
        reperepresentation = super().to_representation
        action = self.context.get('action')
        if action == 'list':
            reperepresentation['comments'] = instance.comments.count()
        elif action  == 'retrieve':
            reperepresentation['comments'] = CommentSerializer(
                instance.comments.all(), many = True
            ).data
        return reperepresentation

    

class CommentSerializer(serializers.ModelSerializer):
    
    author = serializers.ReadOnlyField(source='author.email')


    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment =  Comment.objects.create(
            author=request.user,
            **validated_data
        )
        return comment



