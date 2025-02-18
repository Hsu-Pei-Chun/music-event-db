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
            event = Event.objects.prefetch_related("show_info__location").filter(title__icontains=title).first()
            if not event:
                return Response({"success": False, "message": "找不到活動"}, status=404)
            serializer = EventSerializer(event)
            return Response({"success": True, "data": serializer.data})
        
        events = Event.objects.all().prefetch_related("show_info__location")
        serializer = EventSerializer(events, many=True)
        return Response({"success": True, "data": serializer.data})

    def put(self, request, *args, **kwargs):
        """資料修改 API，允許部分更新"""
        uid = request.data.get("UID")  # 用 UID 來查找資料
        event = get_object_or_404(Event.objects.prefetch_related("show_info__location"), UID=uid)
        serializer = EventSerializer(event, data=request.data, partial=True)  # `partial=True` 允許部分更新
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "資料更新成功", "data": serializer.data})
        return Response({"success": False, "error": serializer.errors}, status=400)

    def delete(self, request, *args, **kwargs):
        """資料刪除 API，透過 UID 刪除"""
        uid = request.data.get("UID")  # 用 UID 來確保刪除的是正確的資料
        event = get_object_or_404(Event.objects.prefetch_related("show_info__location"), UID=uid)
        event.delete()
        return Response({"success": True, "message": "資料刪除成功"})
