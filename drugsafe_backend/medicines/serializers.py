from rest_framework import serializers
from .models import Drug, Review, Comment, Score

class DrugListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'drug', 'form', 'created_at', 'updated_at',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'form', 'created_at', 'updated_at',)

class ReviewDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Review
        fields = ('user', 'drug', 'form', 'created_at', 'updated_at', 'title', 'content', 'comments')
        read_only_fields = ('user', 'drug', 'form', 'created_at', 'updated_at',)

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
        read_only_fields = ('user', 'form', 'drug',)