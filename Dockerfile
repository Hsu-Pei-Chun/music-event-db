# 使用 Ubuntu 20.04 作為基礎映像
FROM ubuntu:20.04

# 安裝 Python 和必要套件
RUN apt update && apt install -y python3 python3-pip python3-venv

# 設定工作目錄
WORKDIR /app

COPY . .


# 安裝 Django
RUN pip3 install django

# 預設啟動 Django 伺服器
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
