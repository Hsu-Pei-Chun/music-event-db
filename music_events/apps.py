from django.apps import AppConfig
import threading
import os
import time

class MusicEventsConfig(AppConfig):
    name = 'music_events'

    def ready(self):
        """ 當 Django 啟動時，確保爬蟲只執行一次 """
        print("✅ [DEBUG] MusicEventsConfig.ready() 已執行")  # 新增 debug 訊息
        if os.environ.get('RUN_MAIN') == 'true':
            from music_events.scripts.scraper import start_scheduler
            print("✅ [DEBUG] 開始執行 start_scheduler()")  # 新增 debug 訊息
            thread = threading.Thread(target=start_scheduler)
            thread.daemon = True
            thread.start()
            print("✅ [DEBUG] 爬蟲排程啟動完成")  # 新增 debug 訊息
