import requests
import json
import os
import pymongo
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time
import django
import sys
import subprocess

sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# 爬取資料的 API
DATA_URL = "https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=1"

JSON_FILE_PATH = os.path.join(os.getcwd(), "music_events", "data", "music_events.json")

# MongoDB 連線設定
MONGO_URI = "mongodb://mongo_db:27017/"
DB_NAME = "scraper_logs"
COLLECTION_NAME = "logs"

def fetch_and_save_data():
    """ 爬取最新資料並儲存為 JSON 檔案 """
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        data = response.json()

        # 將 JSON 存到 music_events.json
        with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"[{datetime.now()}] 成功爬取資料，已儲存至 {JSON_FILE_PATH}")
        return True, len(data)  # 回傳成功狀態與資料數量

    except Exception as e:
        print(f"[{datetime.now()}] 爬取失敗: {str(e)}")
        return False, 0

def log_to_mongodb(status, data_count):
    """ 將爬取紀錄存入 MongoDB """
    
    print("🔍 正在連接 MongoDB...")
    print(f"MongoDB 連線字串: {MONGO_URI}")

    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    log_entry = {
        "timestamp": datetime.utcnow(),
        "status": "成功" if status else "失敗",
        "data_count": data_count
    }

    collection.insert_one(log_entry)
    print(f"[{datetime.now()}] 爬取紀錄已存入 MongoDB")

def job():
    """ 定時執行的爬取作業 """
    print("✅ [DEBUG] 爬蟲 job() 執行中...")
    success, count = fetch_and_save_data()

    if success:
        print("✅ [DEBUG] 爬取成功，開始執行資料匯入...")
        result = subprocess.run(["python3", "manage.py", "import_json"], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"❌ [ERROR] import_json.py 執行錯誤: {result.stderr}")    

    log_to_mongodb(success, count)

def start_scheduler():
    """ 啟動爬蟲排程 """
    print("✅ [DEBUG] start_scheduler() 被呼叫")
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, "cron", hour=1, minute=0, timezone="Asia/Taipei")  # 每天 01:00 執行
    scheduler.start()
    print("✅ 爬蟲排程已啟動，每日 01:00 執行")

if __name__ == "__main__":
    print("🚀 Scraper 容器啟動成功...", flush=True)
    start_scheduler()
    while True:
        print("🔄 Scraper 容器正在運行...", flush=True)
        time.sleep(1)  # 讓容器保持運行