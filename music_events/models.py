from django.db import models

class Event(models.Model):
    UID = models.CharField(max_length=255, primary_key=True)  # 活動唯一識別碼
    version = models.CharField(max_length=10)  # 數據版本
    title = models.CharField(max_length=255)  # 活動名稱
    category = models.CharField(max_length=10)  # 活動分類（原本是 IntegerField，JSON 為字串）
    showUnit = models.CharField(max_length=255, blank=True, null=True)  # 演出單位
    discountInfo = models.TextField(blank=True, null=True)  # 折扣資訊
    descriptionFilterHtml = models.TextField(blank=True, null=True)  # 活動描述
    imageUrl = models.URLField(blank=True, null=True)  # 活動圖片
    masterUnit = models.JSONField(blank=True, null=True)  # 主辦單位（存 JSON）
    subUnit = models.JSONField(blank=True, null=True)  # 協辦單位
    supportUnit = models.JSONField(blank=True, null=True)  # 支援單位
    otherUnit = models.JSONField(blank=True, null=True)  # 其他單位
    webSales = models.URLField(blank=True, null=True)  # 購票網址
    sourceWebPromote = models.URLField(blank=True, null=True)  # 宣傳網站
    sourceWebName = models.CharField(max_length=255, blank=True, null=True)  # 來源網站
    startDate = models.DateField()  # 活動開始日期
    endDate = models.DateField()  # 活動結束日期
    hitRate = models.IntegerField(default=0)  # 點擊率
    comment = models.TextField(blank=True, null=True)  # 活動評論
    editModifyDate = models.CharField(max_length=255, blank=True, null=True)  # 最後修改日期

    def __str__(self):
        return self.title


class Location(models.Model):
    locationID = models.AutoField(primary_key=True)  # 自動遞增 ID
    location = models.CharField(max_length=255)  # 具體地址
    locationName = models.CharField(max_length=255)  # 場地名稱
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)  # 緯度
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)  # 經度

    def __str__(self):
        return self.locationName


class ShowInfo(models.Model):
    showID = models.AutoField(primary_key=True)  # 場次唯一識別碼，自動遞增
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="show_info")  # 關聯到 events 表
    show_time = models.DateTimeField()  # 演出時間（從 JSON 轉換格式）
    endTime = models.DateTimeField(blank=True, null=True)  # 演出結束時間（允許 null）
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="show_info")  # 關聯到 locations 表
    onSales = models.CharField(max_length=1, choices=[("Y", "Yes"), ("N", "No")], default="N")  # 是否開放售票
    price = models.CharField(max_length=255, blank=True, null=True)  # 票價資訊

    def __str__(self):
        return f"{self.event.title} - {self.show_time}"
