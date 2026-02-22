import requests
import re
import base64

# این منابع به تنهایی شامل تمام کانال‌های تلگرامی و گیت‌هاب‌های معروف هستند
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vless/base64",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vmess/base64",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/trojan/base64",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://raw.githubusercontent.com/Iranian_V2Ray/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://t.me/s/v2rayngvpn", # اسکن مستقیم محتوای کانال تلگرام (نسخه وب)
    "https://t.me/s/v2ray_outlinefree"
]

def grab_configs():
    all_configs = []
    print("شروع جستجوی جهانی...")
    
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=20)
            content = response.text
            
            # رمزگشایی اگر محتوا Base64 بود
            try:
                if not content.startswith(('vless', 'vmess', 'ss', 'trojan')):
                    content = base64.b64decode(content).decode('utf-8')
            except: pass
            
            # استخراج تمام لینک‌ها با متد پیشرفته
            found = re.findall(r'(vless|vmess|trojan|ss)://[^\s<"\'|]+', content)
            for proto, rest in found:
                all_configs.append(f"{proto}://{rest}")
        except Exception as e:
            print(f"خطا در منبع {url}: {e}")
            continue
    
    # حذف تکراری‌ها
    unique_configs = list(set(all_configs))
    print(f"تعداد کل یافت شده: {len(unique_configs)}")

    # تفکیک دقیق بر اساس کد کشورها
    # این بخش به دنبال نام کشور در نام (Remark) کانفیگ می‌گردد
    us_confs = [c for c in unique_configs if any(x in c.upper() for x in ["US", "USA", "UNITED STATES"])]
    de_confs = [c for c in unique_configs if any(x in c.upper() for x in ["DE", "GERMANY", "FRANKFURT"])]
    
    # ذخیره فایل‌ها برای سایت
    with open("configs.txt", "w", encoding="utf-8") as f: f.write("\n".join(unique_configs))
    with open("US.txt", "w", encoding="utf-8") as f: f.write("\n".join(us_confs[:100]))
    with open("DE.txt", "w", encoding="utf-8") as f: f.write("\n".join(de_confs[:100]))
    
    # ارسال آمار نهایی به سایت
    stats = f"ALL:{len(unique_configs)},US:{len(us_confs)},DE:{len(de_confs)}"
    with open("stats.txt", "w", encoding="utf-8") as f:
        f.write(stats)
    print("فایل‌ها با موفقیت آپدیت شدند.")

if __name__ == "__main__":
    grab_configs()
