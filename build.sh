#!/usr/bin/env bash
# 當發生錯誤時立即停止腳本
set -o errexit

echo "開始安裝套件..."
pip install -r requirements.txt

echo "收集靜態檔案 (Collectstatic)..."
python manage.py collectstatic --no-input

echo "執行資料庫遷移 (Migrate to Supabase)...1"
python manage.py makemigrations

echo "執行資料庫遷移 (Migrate to Supabase)...2"
python manage.py migrate