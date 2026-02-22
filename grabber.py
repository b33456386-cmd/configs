import requests
import re

# لیست منابع (کانال‌های تلگرام و لینک‌های گیت‌هاب)
SOURCES = [
    "https://t.me/s/v2ray_outlinefree",
    "https://t.me/s/v2ray_free_conf",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vless/base64",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vmess/base64"
]

def grab_configs():
    all_configs = []
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=10)
            # استخراج لینک‌های کانفیگ با Regex
            configs = re.findall(r'(vless|vmess|ss|trojan)://[^\s<"]+', response.text)
            for proto, link in configs:
                all_configs.append(f"{proto}://{link}")
        except:
            continue
    
    # حذف تکراری‌ها
    unique_configs = list(set(all_configs))
    
    # ذخیره در فایل اصلی
    with open("configs.txt", "w") as f:
        f.write("\n".join(unique_configs))

    # دسته‌بندی بر اساس کشور (فیلتر کردن ساده)
    countries = {"US": [], "DE": [], "TR": []}
    for conf in unique_configs:
        for code in countries.keys():
            if code in conf.upper():
                countries[code].append(conf)
    
    # ذخیره فایل‌های جداگانه برای هر کشور
    for code, confs in countries.items():
        with open(f"{code}.txt", "w") as f:
            f.write("\n".join(confs[:10])) # ۱۰ تا از جدیدترین‌ها

if __name__ == "__main__":
    grab_configs()
