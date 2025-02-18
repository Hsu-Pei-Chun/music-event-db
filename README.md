# music-event-db

## 🎵 音樂表演資訊 ERD 設計

本專案的資料庫設計遵循 **1NF → 2NF → 3NF** 的正規化規則，確保數據結構最佳化。

### 📌 ERD 圖與詳細說明
- ERD 圖：[點此查看](https://dbdiagram.io/d/db_music_event_-67b2da4e263d6cf9a0617e04)
- 設計與正規化過程：[完整指南](https://realnewbie.com/coding/basic-concent/data-normalization-complete-guide-from-json-to-structured-data/)

## 🚀 啟動專案
本專案使用 **Docker** 啟動容器。

### 啟動指令
```sh
docker compose up
```

### 背景執行
若要在背景執行，請加上 `-d` 參數：
```sh
docker compose up -d
```

### 資料庫遷移與導入
執行以下指令進行資料庫遷移與 JSON 資料導入：
```sh
docker compose exec web python3 manage.py makemigrations
docker compose exec web python3 manage.py migrate
docker compose exec web python3 manage.py import_json
```
