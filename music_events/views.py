from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Event
from .serializers import EventSerializer

class OperationView(APIView):

    permission_classes = [AllowAny]

    def get_permissions(self):
        """設定不同操作的權限"""
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAuthenticated()]
        return [AllowAny()]  # 其他操作需要登入

    def get(self, request, *args, **kwargs):
        """資料查詢 API，透過 title 查詢"""
        title = request.query_params.get("title")
        if title:
            event = Event.objects.filter(title__icontains=title).first()
            serializer = EventSerializer(event)
            return Response({"success": True, "data": serializer.data})
        
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response({"success": True, "data": serializer.data})

    def put(self, request, *args, **kwargs):
        """資料修改 API，允許部分更新"""
        title = request.data.get("title")
        event = Event.objects.filter(title__icontains=title).first()  # 透過 title 找到活動
        serializer = EventSerializer(event, data=request.data, partial=True)  # `partial=True` 允許部分更新
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "資料更新成功", "data": serializer.data})
        return Response({"success": False, "error": serializer.errors}, status=400)

    def delete(self, request, *args, **kwargs):
        """資料刪除 API，透過 title 刪除"""
        title = request.data.get("title")
        event = Event.objects.filter(title__icontains=title).first()
        event.delete()
        return Response({"success": True, "message": "資料刪除成功"})
