import requests
import re
import base64
import json

SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/all",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity"
]

def grab_configs():
    all_configs = []
    for url in SOURCES:
        try:
            res = requests.get(url, timeout=30)
            text = res.text
            if "://" not in text[:100]:
                try: text = base64.b64decode(text).decode('utf-8')
                except: pass
            found = re.findall(r'(vless|vmess|trojan|ss)://[^\s<"\'|]+', text)
            all_configs += [f"{p}://{r}" for p, r in found]
        except: continue

    unique_list = list(set(all_configs))
    
    # لیست کدهای کشورها برای شناسایی خودکار
    country_codes = ["US", "DE", "JP", "TR", "FI", "IR", "UK", "FR", "CA", "NL", "SG", "AU", "KR", "HK"]
    organized_data = {"ALL": len(unique_list)}
    
    # ذخیره فایل اصلی
    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_list))

    # تفکیک خودکار بر اساس کد کشور در نام کانفیگ
    for code in country_codes:
        filtered = [c for c in unique_list if f"-{code}" in c.upper() or f" {code}" in c.upper() or f"_{code}" in c.upper()]
        if len(filtered) > 0:
            organized_data[code] = len(filtered)
            with open(f"{code}.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(filtered))

    # ذخیره آمار به صورت JSON برای سایت حرفه‌ای
    with open("stats.json", "w", encoding="utf-8") as f:
        json.dump(organized_data, f)

if __name__ == "__main__":
    grab_configs()
