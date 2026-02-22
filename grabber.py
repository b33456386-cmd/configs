import requests
import re
import base64

# منابع جدید و تست شده که همین الان دیتای فعال دارند
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vless/base64",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vmess/base64",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/trojan/base64",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity"
]

def grab_configs():
    all_configs = []
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=20)
            content = response.text
            
            # رمزگشایی اگر کل صفحه Base64 بود
            try:
                decoded = base64.b64decode(content).decode('utf-8')
                if "://" in decoded: content = decoded
            except: pass
            
            # استخراج تمام پروتکل‌ها
            found = re.findall(r'(vless|vmess|trojan|ss)://[^\s<"\'|]+', content)
            for proto, rest in found:
                all_configs.append(f"{proto}://{rest}")
        except: continue
    
    unique_list = list(set(all_configs))
    
    # فیلتر هوشمند برای ۶ کشور
    countries = {
        "US": ["US", "USA", "UNITED STATES"],
        "DE": ["DE", "GERMANY", "FRANKFURT"],
        "JP": ["JP", "JAPAN", "TOKYO"],
        "TR": ["TR", "TURKEY", "ISTANBUL"],
        "FI": ["FI", "FINLAND", "HELSINKI"],
        "IR": ["IR", "IRAN", "MCI", "IRANCELL"]
    }
    
    final_stats = {"ALL": len(unique_list)}
    
    # ذخیره فایل هر کشور
    for code, keywords in countries.items():
        filtered = [c for c in unique_list if any(x in c.upper() for x in keywords)]
        final_stats[code] = len(filtered)
        with open(f"{code}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(filtered[:100]))

    # ذخیره فایل اصلی
    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_list))
    
    # آپدیت دقیق آمار برای سایت
    stats_str = f"ALL:{final_stats['ALL']},US:{final_stats['US']},DE:{final_stats['DE']},JP:{final_stats['JP']},TR:{final_stats['TR']},FI:{final_stats['FI']},IR:{final_stats['IR']}"
    with open("stats.txt", "w", encoding="utf-8") as f:
        f.write(stats_str)

if __name__ == "__main__":
    grab_configs()
