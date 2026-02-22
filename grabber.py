import requests
import re

# منابع بسیار فعال برای پر شدن سریع لیست کشورها
SOURCES = [
    "https://t.me/s/v2ray_outlinefree",
    "https://t.me/s/v2rayngvpn",
    "https://t.me/s/v2ray_vpn_ir",
    "https://t.me/s/V2rayNG_VPNN",
    "https://t.me/s/free4allvpn",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/protocols/vless/base64"
]

def grab_configs():
    all_configs = []
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=15)
            configs = re.findall(r'(vless|vmess|ss|trojan)://[^\s<"]+', response.text)
            for proto, link in configs:
                all_configs.append(f"{proto}://{link}")
        except: continue
    
    unique_configs = list(set(all_configs))
    with open("configs.txt", "w") as f:
        f.write("\n".join(unique_configs))

    # دسته‌بندی هوشمند
    countries = {"US": [], "DE": []}
    for conf in unique_configs:
        c_up = conf.upper()
        if any(x in c_up for x in ["US", "USA", "UNITED STATES", "NEWYORK"]):
            countries["US"].append(conf)
        elif any(x in c_up for x in ["DE", "GERMANY", "FRANKFURT"]):
            countries["DE"].append(conf)
    
    # ذخیره فایل‌ها و آمار
    stats = f"ALL:{len(unique_configs)},"
    for code, confs in countries.items():
        with open(f"{code}.txt", "w") as f:
            f.write("\n".join(confs[:20]))
        stats += f"{code}:{len(confs)},"
    
    with open("stats.txt", "w") as f:
        f.write(stats.strip(","))

if __name__ == "__main__":
    grab_configs()
 
