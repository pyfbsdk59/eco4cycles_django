from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CycleRecord
from fredapi import Fred
import pandas as pd
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as ET

# 這裡放入您原本的 fetch_fred_data 函式邏輯
# def fetch_fred_data(...): ... 
# def evaluate_stage(...): ... (稍作修改讓它回傳分數而不是印出文字)

def home(request):
    api_key = "31c9ce02b76b2d4e4942671c7f86624a" # 實務上建議放入環境變數 os.environ.get('FRED_API_KEY')
    
    if request.method == 'POST':
        try:
            fred = Fred(api_key=api_key)
            indicators = {
                "貨幣供給 (M2)": ("M2SL", "US M2 Money Supply"),
                "美元指數 (USD)": ("DTWEXAFEGS", "US Dollar Index"),
                "股市表現 (S&P 500)": ("SP500", "S&P 500 Stock Market"),
                # ... 其他指標略 ...
            }
            
            results = {}
            for name, (series_id, query) in indicators.items():
                # 呼叫原本寫好的抓取邏輯
                data = fetch_fred_data(fred, series_id, name, query)
                results[name] = {"latest": float(data['latest']), "trends": data['trends']} if data.get('source') == 'FRED' else None

            # 呼叫判定邏輯取得各時段的判定階段
            stages = evaluate_stage(results) # 假設您將 evaluate_stage 修改為回傳 {"3年": 1, "1年": 2, "6個月": 2, "3個月": 3}
            
            # 將資料存入 Supabase
            CycleRecord.objects.create(
                stage_3y=stages.get("3年"),
                stage_1y=stages.get("1年"),
                stage_6m=stages.get("6個月"),
                stage_3m=stages.get("3個月"),
                raw_data=results
            )
            
            messages.success(request, '資料抓取與分析成功！已儲存至資料庫。')
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'發生錯誤: {e}')

    # GET 請求時，從資料庫撈取最新一筆資料呈現在網頁上
    latest_record = CycleRecord.objects.first()
    return render(request, 'analyzer/home.html', {'record': latest_record})