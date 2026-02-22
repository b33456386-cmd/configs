import requests
import re
import base64
import json

# منابعی که همین الان هزاران کانفیگ دارند
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vless/base64",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity"
]

def grab_configs():
    all_configs = []
    for url in SOURCES:
        try:
            res = requests.get(url, timeout=20)
            text = res.text
            if "://" not in text[:50]:
                try: text = base64.b64decode(text).decode('utf-8')
                except: pass
            
            # استخراج لینک‌ها
            found = re.findall(r'(vless|vmess|trojan|ss)://[^\s<"\'|]+', text)
            all_configs.extend(found)
        except: continue

    unique_configs = list(set(all_configs))
    
    # ذخیره فایل اصلی برای دکمه کپی
    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_configs))

    # ساخت دیتابیس کوچک برای نمایش کارتی در سایت
    # فقط ۵۰ تای اول را برای سرعت بالاتر سایت می‌فرستیم
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(unique_configs[:50], f)

    # آپدیت آمار (فقط برای نمایش عدد در سایت)
    with open("stats.txt", "w", encoding="utf-8") as f:
        f.write(f"ALL:{len(unique_configs)},US:0,DE:0,JP:0,TR:0,FI:0,IR:0")

if __name__ == "__main__":
    grab_configs()
