import json
from django.core.management.base import BaseCommand
from music_events.models import Event, Location, ShowInfo
from django.utils.dateparse import parse_datetime, parse_date
import os
from django.conf import settings
from datetime import datetime

def parse_custom_datetime(datetime_str):
    """解析多種格式的日期時間字符串
    
    支持的格式:
    - YYYY/MM/DD HH:mm:ss
    - YYYY-MM-DD HH:mm:ss
    - YYYY/MM/DD
    - YYYY-MM-DD
    
    Args:
        datetime_str: 要解析的日期時間字符串
        
    Returns:
        datetime: 解析後的 datetime 對象，解析失敗則返回 None
    """
    if not datetime_str:
        return None
        
    date_formats = [
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
        "%Y-%m-%d"
    ]
    
    for date_format in date_formats:
        try:
            return datetime.strptime(datetime_str, date_format)
        except ValueError:
            continue
            
    return None


class Command(BaseCommand):
    help = "Import music events from JSON file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "music_events", "data", "music_events.json")  # JSON 檔案路徑

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        event_created = 0
        event_updated = 0
        showinfo_created = 0
        showinfo_updated = 0 
        location_cache = {}  # 避免重複查詢相同場地

        for item in data:
            print(f"Processing Event UID: {item['UID']}, startDate: {item.get('startDate')}")
            # 檢查活動是否已存在，避免重複插入
            event, created = Event.objects.update_or_create(
                UID=item["UID"],
                defaults={
                    "version": item["version"],
                    "title": item["title"],
                    "category": item["category"],
                    "showUnit": item["showUnit"] or None,
                    "discountInfo": item["discountInfo"] or None,
                    "descriptionFilterHtml": item["descriptionFilterHtml"] or None,
                    "imageUrl": item["imageUrl"] or None,
                    "masterUnit": item["masterUnit"],
                    "subUnit": item["subUnit"],
                    "supportUnit": item["supportUnit"],
                    "otherUnit": item["otherUnit"],
                    "webSales": item["webSales"] or None,
                    "sourceWebPromote": item["sourceWebPromote"] or None,
                    "sourceWebName": item["sourceWebName"] or None,
                    "startDate": parse_custom_datetime(item["startDate"]),
                    "endDate": parse_custom_datetime(item["endDate"]),
                    "hitRate": item["hitRate"],
                    "comment": item["comment"] or None,
                    "editModifyDate": item["editModifyDate"] or None,
                }
            )
            if created:
                event_created += 1
            else:
                event_updated += 1

            # 處理場次資訊
            for show in item["showInfo"]:
                location_key = (show["location"], show["locationName"])
                
                # 檢查地點是否已存在，避免重複新增
                if location_key in location_cache:
                    location = location_cache[location_key]
                else:
                    location, _ = Location.objects.get_or_create(
                        location=show["location"],
                        locationName=show["locationName"],
                        defaults={
                            "latitude": show["latitude"] if show["latitude"] else None,
                            "longitude": show["longitude"] if show["longitude"] else None,
                        }
                    )
                    location_cache[location_key] = location  # 加入快取避免重複查詢

                # 新增 ShowInfo
                _, show_created = ShowInfo.objects.update_or_create(
                    event=event,
                    show_time=parse_custom_datetime(show["time"]),
                    location=location,
                    defaults={
                        "endTime": parse_custom_datetime(show["endTime"]) if show["endTime"] else None,
                        "onSales": show["onSales"],
                        "price": show["price"] or None,
                    }
                )
                if show_created:
                    showinfo_created += 1
                else:
                    showinfo_updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n匯入統計：\n"
            f"Event 資料：\n"
            f"  - 新建：{event_created} 筆\n"
            f"  - 更新：{event_updated} 筆\n"
            f"ShowInfo 場次資料：\n"
            f"  - 新建：{showinfo_created} 筆\n"
            f"  - 更新：{showinfo_updated} 筆"
        ))
