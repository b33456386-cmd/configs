import requests
import re
import base64

# این منابع مستقیماً هزاران کانفیگ فعال رو از تمام دنیا جمع‌آوری می‌کنن
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/all",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://raw.githubusercontent.com/LonUp/V2Ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/SamanGhaffarzad/v2ray-configs/main/subscriptions/v2ray.txt"
]

def grab_configs():
    all_configs = []
    print("شروع جستجوی جهانی...")
    
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=20)
            text = response.text
            
            # باز کردن قفل Base64 اگر دیتای خام نبود
            if "://" not in text[:50]:
                try:
                    text = base64.b64decode(text).decode('utf-8')
                except: pass
            
            # پیدا کردن تمام پروتکل‌ها (vless, vmess, trojan, ss)
            found = re.findall(r'(vless|vmess|trojan|ss)://[^\s<"\'|]+', text)
            for proto, rest in found:
                all_configs.append(f"{proto}://{rest}")
        except: continue
    
    unique_list = list(set(all_configs))
    
    # تفکیک بر اساس ۶ کشوری که خواستی
    countries = {
        "US": ["US", "USA", "UNITED"],
        "DE": ["DE", "GERMANY", "FRANKFURT"],
        "JP": ["JP", "JAPAN", "TOKYO"],
        "TR": ["TR", "TURKEY", "ISTANBUL"],
        "FI": ["FI", "FINLAND", "HELSINKI"],
        "IR": ["IR", "IRAN", "MCI", "MTN", "IRANCELL"]
    }
    
    stats_data = {"ALL": len(unique_list)}
    
    # ذخیره فایل‌های جداگانه برای هر کشور
    for code, keywords in countries.items():
        filtered = [c for c in unique_list if any(x in c.upper() for x in keywords)]
        stats_data[code] = len(filtered)
        with open(f"{code}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(filtered[:100]))

    # ذخیره کل کانفیگ‌ها
    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_list))
    
    # ساخت خط آمار برای سایت
    stats_str = ",".join([f"{k}:{v}" for k, v in stats_data.items()])
    with open("stats.txt", "w", encoding="utf-8") as f:
        f.write(stats_str)
    print(f"تموم شد! {len(unique_list)} کانفیگ پیدا شد.")

if __name__ == "__main__":
    grab_configs()
