import requests
import re
import base64

# این منابع مستقیماً به مخازن بزرگ متصل هستند
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vless/base64",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vmess/base64",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/trojan/base64",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://raw.githubusercontent.com/t-v2ray/v2ray-config/main/All_Configs_Sub.txt"
]

def grab_configs():
    all_configs = []
    for url in SOURCES:
        try:
            res = requests.get(url, timeout=20)
            text = res.text
            # اگر محتوا کدگذاری شده بود، بازش کن
            if "://" not in text[:50]:
                try:
                    text = base64.b64decode(text).decode('utf-8')
                except: pass
            
            # استخراج لینک‌ها
            found = re.findall(r'(vless|vmess|trojan|ss)://[^\s<"\'|]+', text)
            for proto, rest in found:
                all_configs.append(f"{proto}://{rest}")
        except: continue
    
    unique_list = list(set(all_configs))
    
    # تفکیک کشورها (بر اساس کلمات کلیدی در نام کانفیگ)
    countries = {
        "US": ["US", "USA", "UNITED"],
        "DE": ["DE", "GERMANY", "FRANKFURT"],
        "JP": ["JP", "JAPAN", "TOKYO"],
        "TR": ["TR", "TURKEY", "ISTANBUL"],
        "FI": ["FI", "FINLAND", "HELSINKI"],
        "IR": ["IR", "IRAN", "MCI", "MTN"]
    }
    
    counts = {"ALL": len(unique_list)}
    
    for code, keywords in countries.items():
        filtered = [c for c in unique_list if any(x in c.upper() for x in keywords)]
        counts[code] = len(filtered)
        with open(f"{code}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(filtered[:100]))

    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_list))
    
    # آپدیت آمار برای سایت
    stats_str = f"ALL:{counts['ALL']},US:{counts['US']},DE:{counts['DE']},JP:{counts['JP']},TR:{counts['TR']},FI:{counts['FI']},IR:{counts['IR']}"
    with open("stats.txt", "w", encoding="utf-8") as f:
        f.write(stats_str)

if __name__ == "__main__":
    grab_configs()
