import os
import re
import requests

# -------------------
# CONFIG
# -------------------
LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
CSRF_TOKEN = os.getenv("LEETCODE_CSRFTOKEN")
GITHUB_TOKEN = os.getenv("GH_PAT")
GITHUB_USERNAME = "snehilsr91"
GFG_USERNAME = "snehilsr91"  # adjust if different

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
    print("Error fetching LeetCode stats:", e)

# -------------------
# FETCH GFG STATS (API)
# -------------------
gfg_solved = "N/A"
try:
    res = requests.get(f"https://geeks-for-geeks-stats-api-napiyo.vercel.app/?userName={GFG_USERNAME}")
    if res.status_code == 200:
        gfg_solved = str(res.json().get("totalProblemsSolved", "N/A"))
except Exception as e:
    print("Error fetching GFG stats:", e)

# -------------------
# FETCH GITHUB CONTRIBUTIONS
# -------------------
github_contributions = "N/A"
try:
    query = """
    {
      user(login: "%s") {
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """ % GITHUB_USERNAME

    res = requests.post(
        "https://api.github.com/graphql",
        json={"query": query},
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
    )
    if res.status_code == 200:
        github_contributions = str(res.json()["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"])
except Exception as e:
    print("Error fetching GitHub contributions:", e)

# -------------------
# UPDATE README
# -------------------
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

readme = re.sub(
    r"(LeetCode%20Problems%20Solved-)[\d\+]+",
    rf"\1{leetcode_solved}",
    readme
)
readme = re.sub(
    r"(GFG%20Problems%20Solved-)[\d\+]+",
    rf"\1{gfg_solved}",
    readme
)
readme = re.sub(
    r"(GitHub%20Contributions-)[\d\+]+",
    rf"\1{github_contributions}",
    readme
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("✅ README updated successfully!")
