from django.apps import AppConfig
import os

class MusicEventsConfig(AppConfig):
    name = 'music_events'

    def ready(self):
        """ 當 Django 啟動時，避免在此啟動爬蟲 """
        print("✅ [DEBUG] MusicEventsConfig.ready() 已執行")
        if os.environ.get('RUN_MAIN') == 'true':
            print("✅ [DEBUG] Django 應用已啟動（但不啟動爬蟲）")
