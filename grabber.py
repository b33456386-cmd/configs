import requests
import re
import base64

SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/all",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://raw.githubusercontent.com/LonUp/V2Ray-Configs/main/All_Configs_Sub.txt"
]

def grab_configs():
    all_configs = []
    for url in SOURCES:
        try:
            res = requests.get(url, timeout=20)
            text = res.text
            try:
                if "://" not in text[:50]:
                    text = base64.b64decode(text).decode('utf-8')
            except: pass
            
            found = re.findall(r'(vless|vmess|trojan|ss)://[^\s<"\'|]+', text)
            for proto, rest in found:
                all_configs.append(f"{proto}://{rest}")
        except: continue
    
    unique_list = list(set(all_configs))
    
    # فیلتر هوشمند برای ۶ کشور مورد نظر تو
    # US: آمریکا | DE: آلمان | JP: ژاپن | TR: ترکیه | FI: فنلاند | IR: ایران
    countries = {
        "US": ["US", "USA", "UNITED STATES"],
        "DE": ["DE", "GERMANY", "FRANKFURT"],
        "JP": ["JP", "JAPAN", "TOKYO"],
        "TR": ["TR", "TURKEY", "ISTANBUL"],
        "FI": ["FI", "FINLAND", "HELSINKI"],
        "IR": ["IR", "IRAN", "MCI", "IRANCELL"]
    }
    
    results = {}
    for code, keywords in countries.items():
        results[code] = [c for c in unique_list if any(x in c.upper() for x in keywords)]
        with open(f"{code}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(results[code][:100]))

    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_list))
    
    # ساخت آمار برای نمایش در سایت
    stats_str = f"ALL:{len(unique_list)},US:{len(results['US'])},DE:{len(results['DE'])},JP:{len(results['JP'])},TR:{len(results['TR'])},FI:{len(results['FI'])},IR:{len(results['IR'])}"
    with open("stats.txt", "w", encoding="utf-8") as f:
        f.write(stats_str)

if __name__ == "__main__":
    grab_configs()
