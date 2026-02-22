import requests
import re
import base64

# منابع تست شده و پر قدرت
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vless/base64",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vmess/base64",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/trojan/base64",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/ss/base64",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt"
]

def grab_configs():
    all_configs = []
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=15)
            content = response.text
            
            # اگر محتوا Base64 بود، آن را باز کن
            try:
                content = base64.b64decode(content).decode('utf-8')
            except: pass
            
            # پیدا کردن تمام لینک‌های استاندارد
            links = re.findall(r'(vless|vmess|ss|trojan)://[^\s<"]+', content)
            for proto, link in links:
                all_configs.append(f"{proto}://{link}")
        except: continue
    
    unique_configs = list(set(all_configs))
    
    # ذخیره فایل اصلی
    with open("configs.txt", "w") as f:
        f.write("\n".join(unique_configs))

    # فیلتر کردن هوشمند برای آمریکا و آلمان
    us_confs = [c for c in unique_configs if any(x in c.upper() for x in ["US", "USA", "UNITED"])]
    de_confs = [c for c in unique_configs if any(x in c.upper() for x in ["DE", "GERMANY", "FRANKFURT"])]
    
    with open("US.txt", "w") as f: f.write("\n".join(us_confs[:50]))
    with open("DE.txt", "w") as f: f.write("\n".join(de_confs[:50]))
    
    # آپدیت آمار (اعداد واقعی!)
    stats = f"ALL:{len(unique_configs)},US:{len(us_confs)},DE:{len(de_confs)}"
    with open("stats.txt", "w") as f:
        f.write(stats)

if __name__ == "__main__":
    grab_configs()
