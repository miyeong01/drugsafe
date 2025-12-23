from rest_framework import serializers
from .models import Drug, Review, Comment

class DrugListSerializer(serializers.ModelSerializer):
    form_name = serializers.CharField(source='form.name', read_only=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Drug
        fields = '__all__'

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        
        if user and user.is_authenticated:
            result = obj.favorites.filter(user=user).exists()
            return result
        return False

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    drug_name = serializers.ReadOnlyField(source='drug.name')
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'drug', 'drug_name', 'form', 'created_at', 'updated_at',)
        extra_kwargs = {
            'score' : {'required': True},
            'title' : {
                'required' : False,
                'allow_blank' : True,
                'allow_null' : True,
            },
            'content' : {
                'required' : False,
                'allow_blank' : True,
                'allow_null' : True,
            },
        }

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    drug_id = serializers.ReadOnlyField(source='review.drug.id')
    drug_name = serializers.ReadOnlyField(source='review.drug.name')
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'review', 'drug_id', 'drug_name', 'form', 'created_at', 'updated_at',)

class ReviewDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Review
        fields = ('user', 'username', 'drug', 'form', 'score', 'created_at', 'updated_at', 'title', 'content', 'comments')
        read_only_fields = ('user', 'drug', 'form', 'created_at', 'updated_at',)