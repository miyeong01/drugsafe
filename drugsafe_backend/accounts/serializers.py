# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # 'first_name' 필드의 값을 'name'이라는 키로 프론트에 보내줍니다.
    name = serializers.CharField(source='first_name', read_only=True)

    class Meta:
        model = User
        # 프론트엔드에서 사용할 필드들을 정의합니다.
        fields = ('pk', 'username', 'email', 'name', 'first_name', 'last_name')

class CustomRegisterSerializer(RegisterSerializer):
    # 프론트에서 보낸 'name'을 받을 필드 선언
    name = serializers.CharField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('name', '')
        return data
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.validated_data.get('name', '')
        user.save()
        return user