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
# FETCH LEETCODE STATS
# -------------------
leetcode_solved = "455"
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

# -------------------
# FETCH GFG STATS
# -------------------
gfg_solved = "28"
try:
    res = requests.get(f"https://geeks-for-geeks-stats-api-napiyo.vercel.app/?userName={GFG_USERNAME}")
    if res.status_code == 200 and "totalProblemsSolved" in res.json():
        gfg_solved = str(res.json().get("totalProblemsSolved", "N/A"))
except Exception as e:
    print("❌ Error fetching GFG stats:", e)

# -------------------
# FETCH MonkeyType WPM
# -------------------
monkey_wpm = "98"
try:
    res = requests.get(f"https://monkeytype.com/api/users/{MONKEYTYPE_USERNAME}/performance")
    if res.status_code == 200:
        data = res.json()
        if "average_wpm" in data:
            monkey_wpm = str(round(data["average_wpm"]))
except Exception as e:
    print("❌ Error fetching MonkeyType stats:", e)

# -------------------
# FETCH Boot.dev LEVEL
# -------------------
bootdev_level = "4"
try:
    res = requests.get(f"https://boot.dev/api/users/{BOOTDEV_USERNAME}/progress")
    if res.status_code == 200:
        data = res.json()
        if "level" in data:
            bootdev_level = str(data["level"])
except Exception as e:
    print("❌ Error fetching Boot.dev stats:", e)

# -------------------
# UPDATE README
# -------------------
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

# Construct new badges HTML
badges_html = f"""
<p align="center">
  <img src="https://img.shields.io/badge/LeetCode%20Problems%20Solved-{leetcode_solved}-orange?style=for-the-badge&logo=leetcode" />
  <img src="https://img.shields.io/badge/GFG%20Problems%20Solved-{gfg_solved}-brightgreen?style=for-the-badge&logo=geeksforgeeks" />
  <img src="https://img.shields.io/badge/MonkeyType%20WPM-{monkey_wpm}-e2b714?style=for-the-badge&logo=monkeytype" />
  <img src="https://img.shields.io/badge/Boot.dev%20Level-{bootdev_level}-0a2540?style=for-the-badge&logo=bootdotdev" />
</p>
"""

# Replace old badges section between markers
readme = re.sub(
    r'<!-- BADGES_START -->.*<!-- BADGES_END -->',
    f'<!-- BADGES_START -->{badges_html}<!-- BADGES_END -->',
    readme,
    flags=re.DOTALL
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("✅ README updated successfully!")
