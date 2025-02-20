# music-event-db

## 🎵 音樂表演資訊 ERD 設計
本專案的資料庫設計遵循 **1NF → 2NF → 3NF** 的正規化規則，確保數據結構最佳化。

### 📌 ERD 圖與詳細說明
- ERD 圖：[點此查看](https://dbdiagram.io/d/db_music_event_-67b2da4e263d6cf9a0617e04)
- 設計與正規化過程：[完整指南](https://realnewbie.com/coding/basic-concent/data-normalization-complete-guide-from-json-to-structured-data/)

## 🚀 啟動專案
本專案使用 **Docker** 啟動容器，包含以下三個服務：
- `web`：Django 應用程式，提供 API 及管理後台
- `scraper`：爬蟲程式，自動抓取音樂活動資訊
- `mongodb`：MongoDB 資料庫

### 啟動所有服務
```sh
docker compose up
```
若要在背景執行：
```sh
docker compose up -d
```

### 📦 MongoDB 連線資訊
啟動後，MongoDB 可透過 `mongodb://mongo_db:27017` 連線。

### 🔄 資料庫遷移與導入
```sh
docker compose exec web python3 manage.py makemigrations
docker compose exec web python3 manage.py migrate
docker compose exec web python3 manage.py import_json
```

### 🕵️‍♂️ 手動執行爬蟲
若想手動執行 `scraper` 來更新音樂活動資料：
```sh
docker compose exec scraper python3 /app/music_events/scripts/scraper.py
```

