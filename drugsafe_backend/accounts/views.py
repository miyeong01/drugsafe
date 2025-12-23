from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import PasswordChangeSerializer

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            # 현재 비밀번호 확인
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["현재 비밀번호가 틀립니다."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # 새 비밀번호 설정
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)