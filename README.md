﻿## 📌 專案簡介

本專案透過 [⾳樂表演資訊 | 政府資料開放平臺](https://data.gov.tw/dataset/6017) 作為資料來源，並對數據進行 **第三正規化**，儲存至 **SQLite3** 資料庫。

網站連結：https://musicevent.realnewbie.com/ (已關閉站點)

後端使用 `Django` + `Django REST Framework`，前端使用 `Alpine.js` 搭配 `Tailwind CSS`，並透過 `Docker` 進行環境管理。

本系統提供：
- 📌 **登入/登出 API**
- 🔄 **CRUD 操作 API**
- 🕒 **每日 01:00:00 (UTC+8) 自動更新資料**
- 📊 **爬取紀錄儲存至 MongoDB**

---

## 🛠 技術架構

- **後端**：Django + Django REST Framework (CBV 風格)
- **前端**：Alpine.js + Tailwind CSS
- **資料庫**：
  - **SQLite3**（存儲音樂表演資訊）
  - **MongoDB**（存儲爬取紀錄）
- **環境管理**：Docker（Ubuntu 20.04）

---

## 📖 ERD 設計

📌 ERD 圖：[點此查看](https://dbdiagram.io/d/db_music_event_-67b2da4e263d6cf9a0617e04)

---

## 🔧 安裝與使用

### 1️⃣ 環境需求

請確保安裝以下工具：
- **Docker**（建議版本 `>= 20.10`）

### 2️⃣ 啟動專案

```sh
# 1. 克隆專案
git clone https://github.com/Hsu-Pei-Chun/music-event-db.git
cd music-event-api

# 2. 啟動 Docker
docker-compose up -d --build
```

### 3️⃣ 進入 Docker 環境並進行 Migrations

```sh
docker exec -it django_app bash

# 進行資料庫遷移
docker compose exec web python3 manage.py migrate
```

## 🚀 API 使用方式

| 方法 | 端點 | 說明 |
|------|------|------|
| `POST` | `/api/users/register/` | 登出 |
| `POST` | `/api/users/login/` | 登入 |
| `POST` | `/api/users/logout/` | 登出 |
| `GET` | `/api/events/operation/` | 取得資料 |
| `PUT` | `/api/events/operation/` | 更新資料 |
| `DELETE` | `/api/events/operation/` | 刪除資料 |


### 🔍 資料查詢 API

📌 **允許未登入及已登入用戶訪問**
```sh
GET /api/events/operation/
```

📌 **回應範例**
```json
{
    "version": "1.4",
    "UID": "669eab3226b3240c380463f1",
    "title": "新觀點．新世界～Kimball Gallagher 2024台灣巡迴音樂會",
    "category": "1",
    "showInfo": [
      {
        "time": "2025/02/19 19:30:00",
        "location": "高雄市鳳山區三多一路1號",
        "locationName": "衛武營國家藝術文化中心表演廳",
        "onSales": "Y",
        "price": "",
        "latitude": "22.6230179238508",
        "longitude": "120.342434118507",
        "endTime": "2025/02/19 21:05:00"
      }
    ],
    "showUnit": "",
    "discountInfo": "",
    "descriptionFilterHtml": "",
    "imageUrl": "",
    "masterUnit": [],
    "subUnit": [],
    "supportUnit": [],
    "otherUnit": [],
    "webSales": "https://www.opentix.life/program/1811063063948378113",
    "sourceWebPromote": "https://www.opentix.life/program/1811063063948378113",
    "comment": "",
    "editModifyDate": "",
    "sourceWebName": "OPENTIX兩廳院文化生活",
    "startDate": "2025/02/19",
    "endDate": "2025/02/19",
    "hitRate": 34
  }
```

---

## 🔄 自動更新機制

系統將於 **每日 01:00:00 (UTC+8)** 自動從 [政府資料開放平臺](https://data.gov.tw/dataset/6017) 爬取最新資料，並更新 SQLite3 資料庫，爬取紀錄將存於 MongoDB。

手動執行爬取：
```sh
docker exec -it django_app python manage.py import_json
```

