import requests
import re

# Config
leetcode_username = "snehilsr91"
github_username = "snehilsr91"
gfg_solved = "25+"  # Until scraping is added
github_token = "YOUR_GITHUB_TOKEN"  # For GraphQL contributions API

# Fetch LeetCode stats
leetcode_api = f"https://leetcode-stats-api.herokuapp.com/{leetcode_username}"
leetcode_response = requests.get(leetcode_api)

if leetcode_response.status_code == 200:
    try:
        leetcode_data = leetcode_response.json()
        leetcode_solved = str(leetcode_data.get("totalSolved", "400+"))
    except ValueError:
        leetcode_solved = "400+"
else:
    leetcode_solved = "400+"

# Fetch GitHub contributions (GraphQL API)
headers = {"Authorization": f"Bearer {github_token}"}
query = f"""
{{
  user(login: "{github_username}") {{
    contributionsCollection {{
      contributionCalendar {{
        totalContributions
      }}
    }}
  }}
}}
"""
response = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers=headers
)

if response.status_code == 200:
    data = response.json()
    github_contributions = str(data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"])
else:
    github_contributions = "N/A"

# Read README.md
with open("README.md", "r", encoding="utf-8") as file:
    readme_content = file.read()

# Replace values (allow + in match)
readme_content = re.sub(r"LeetCode%20Problems%20Solved-[\d\+]+", f"LeetCode%20Problems%20Solved-{leetcode_solved}", readme_content)
readme_content = re.sub(r"GFG%20Problems%20Solved-[\d\+]+", f"GFG%20Problems%20Solved-{gfg_solved}", readme_content)
readme_content = re.sub(r"GitHub%20Contributions-[\d\+]+", f"GitHub%20Contributions-{github_contributions}", readme_content)

# Write README.md
with open("README.md", "w", encoding="utf-8") as file:
    file.write(readme_content)

print("✅ README updated successfully!")
