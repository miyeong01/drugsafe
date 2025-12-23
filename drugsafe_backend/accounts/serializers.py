# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.password_validation import validate_password

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
    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "새 비밀번호가 일치하지 않습니다."})
        return attrs