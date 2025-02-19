# 使用 Ubuntu 20.04 作為基礎映像
FROM ubuntu:20.04

# 環境變數：自動設定時區，避免 tzdata 提示交互式輸入
ENV TZ=Asia/Taipei
RUN apt update && apt install -y tzdata

# 安裝 Python 和必要套件
RUN apt update && apt install -y python3 python3-pip python3-venv


# 設定工作目錄
WORKDIR /app

COPY . .

# 安裝 Django 和依賴套件
RUN pip3 install --no-cache-dir -r requirements.txt

# 預設啟動 Django 伺服器
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
