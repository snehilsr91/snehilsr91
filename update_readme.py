import os
import re
import requests

# -------------------
# CONFIG
# -------------------
LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
CSRF_TOKEN = os.getenv("LEETCODE_CSRFTOKEN")
GFG_USERNAME = "snehilsr91"
MONKEYTYPE_USERNAME = "snehilsr91"
BOOTDEV_USERNAME = "snehilsr91"

# -------------------
# FETCH LEETCODE STATS (via session cookie)
# -------------------
leetcode_solved = "N/A"
try:
    cookies = {
        "LEETCODE_SESSION": LEETCODE_SESSION,
        "csrftoken": CSRF_TOKEN
    }
    headers = {
        "x-csrftoken": CSRF_TOKEN,
        "referer": "https://leetcode.com",
    }
    res = requests.get("https://leetcode.com/api/problems/all/", cookies=cookies, headers=headers)
    if res.status_code == 200:
        data = res.json()
        total = sum(1 for q in data["stat_status_pairs"] if q["status"] == "ac")
        leetcode_solved = str(total)
except Exception as e:
    print("❌ Error fetching LeetCode stats:", e)

print("LeetCode problems solved:", leetcode_solved)

# -------------------
# FETCH GFG STATS (API)
# -------------------
gfg_solved = "N/A"
try:
    res = requests.get(f"https://geeks-for-geeks-stats-api-napiyo.vercel.app/?userName={GFG_USERNAME}")
    if res.status_code == 200 and "totalProblemsSolved" in res.json():
        gfg_solved = str(res.json().get("totalProblemsSolved", "N/A"))
except Exception as e:
    print("❌ Error fetching GFG stats:", e)

print("GFG problems solved:", gfg_solved)

# -------------------
# FETCH MonkeyType WPM (API)
# -------------------
monkey_wpm = "N/A"
try:
    res = requests.get(f"https://monkeytype.com/api/users/{MONKEYTYPE_USERNAME}/performance")
    if res.status_code == 200:
        data = res.json()
        if "average_wpm" in data:
            monkey_wpm = str(round(data["average_wpm"]))
except Exception as e:
    print("❌ Error fetching MonkeyType stats:", e)

print("MonkeyType WPM:", monkey_wpm)

# -------------------
# FETCH Boot.dev level (API)
# -------------------
bootdev_level = "N/A"
try:
    res = requests.get(f"https://boot.dev/api/users/{BOOTDEV_USERNAME}/progress")
    if res.status_code == 200:
        data = res.json()
        if "level" in data:
            bootdev_level = str(data["level"])
except Exception as e:
    print("❌ Error fetching Boot.dev stats:", e)

print("Boot.dev level:", bootdev_level)

# -------------------
# UPDATE README
# -------------------
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

# Update badges
readme = re.sub(
    r'(LeetCode%20Problems%20Solved-)[^"\s<]+',
    rf'\1{leetcode_solved}',
    readme
)
readme = re.sub(
    r'(GFG%20Problems%20Solved-)[^"\s<]+',
    rf'\1{gfg_solved}',
    readme
)
readme = re.sub(
    r'(MonkeyType%20WPM-)[^"\s<]+',
    rf'\1{monkey_wpm}',
    readme
)
readme = re.sub(
    r'(Boot\.dev%20Level-)[^"\s<]+',
    rf'\1{bootdev_level}',
    readme
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("✅ README updated successfully!")
