import requests
import re

# لیست منابع کانفیگ (می‌توانی لینک‌های مستقیم یا سورس‌های گیت‌هاب را اینجا بگذاری)
sources = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vless",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vmess"
]

def get_configs():
    all_configs = ""
    for url in sources:
        try:
            res = requests.get(url)
            all_configs += res.text + "\n"
        except:
            pass
    return all_configs

# ذخیره در یک فایل متنی برای استفاده سایت
with open("configs.txt", "w") as f:
    f.write(get_configs())
