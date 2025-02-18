from rest_framework import serializers
from .models import Event, ShowInfo, Location

class ShowInfoSerializer(serializers.ModelSerializer):
    """場次資訊序列化"""
    time = serializers.DateTimeField(source="show_time", format="%Y/%m/%d %H:%M:%S")
    endTime = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S")
    location = serializers.CharField(source="location.location")
    locationName = serializers.CharField(source="location.locationName")
    latitude = serializers.CharField(source="location.latitude")
    longitude = serializers.CharField(source="location.longitude")

    class Meta:
        model = ShowInfo
        fields = ["time", "endTime", "location", "locationName", "onSales", "price", "latitude", "longitude"]

class EventSerializer(serializers.ModelSerializer):
    """活動資訊序列化"""
    showInfo = ShowInfoSerializer(source="show_info", many=True)  # 加入 showInfo

    class Meta:
        model = Event
        fields = [
            "version",
            "UID",
            "title",
            "category",
            "showInfo",
            "showUnit",
            "discountInfo",
            "descriptionFilterHtml",
            "imageUrl",
            "masterUnit",
            "subUnit",
            "supportUnit",
            "otherUnit",
            "webSales",
            "sourceWebPromote",
            "comment",
            "editModifyDate",
            "sourceWebName",
            "startDate",
            "endDate",
            "hitRate",
        ]
