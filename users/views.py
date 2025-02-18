from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

class RegisterView(APIView):
    """ 使用者註冊 API """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "請提供使用者名稱和密碼"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "使用者名稱已被註冊"}, status=status.HTTP_400_BAD_REQUEST)

        # 創建新使用者並加密密碼
        user = User.objects.create_user(username=username, password=password)

        # 產生 Token
        token = Token.objects.create(user=user)
        return Response({"message": "註冊成功", "token": token.key}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """ 使用者登入 API """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "登入成功", "token": token.key}, status=status.HTTP_200_OK)

        return Response({"error": "帳號或密碼錯誤"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """ 使用者登出 API """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()  # 刪除 Token
        return Response({"message": "登出成功"}, status=status.HTTP_200_OK)
