from rest_framework import serializers
from django.db.models import Avg 
from .models import Drug, Review, Comment

class DrugListSerializer(serializers.ModelSerializer):
    form_name = serializers.CharField(source='form.name', read_only=True)
    is_favorite = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Drug
        fields = '__all__'

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        if user and user.is_authenticated:
            # favorite 모델의 related_name='favorites' 확인
            return obj.favorites.filter(user=user).exists()
        return False
    
    def get_rating(self, obj):
        try:
            # Review의 related_name='drugs'와 필드명 'score' 사용
            average = obj.drugs.aggregate(Avg('score'))['score__avg']
            return round(float(average), 1) if average else 0.0
        except Exception as e:
            # 서버가 죽지 않도록 에러 로깅만 하고 0.0 반환
            print(f"Rating Error: {e}")
            return 0.0

    def get_review_count(self, obj):
        # Review의 related_name='drugs' 사용
        return obj.drugs.count()

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