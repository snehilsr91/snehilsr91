import requests
import re

# Your usernames
leetcode_username = "snehilsr91"
github_username = "snehilsr91"
gfg_username = "snehilsr91"  # Placeholder, needs scraping

# Fetch LeetCode stats
leetcode_api = f"https://leetcode-stats-api.herokuapp.com/{leetcode_username}"
leetcode_data = requests.get(leetcode_api).json()
leetcode_solved = leetcode_data.get("totalSolved", "N/A")

# Fetch GitHub Contributions (using public repos as a proxy)
github_api = f"https://api.github.com/users/{github_username}"
github_data = requests.get(github_api).json()
github_contributions = github_data.get("public_repos", "N/A")  # Approximate contribution count

# Placeholder for GFG (Web scraping required)
gfg_solved = "N/A"

# Read README.md
with open("README.md", "r", encoding="utf-8") as file:
    readme_content = file.read()

# Update stats in README.md
readme_content = re.sub(r"LeetCode%20Problems%20Solved-\w+", f"LeetCode%20Problems%20Solved-{leetcode_solved}", readme_content)
readme_content = re.sub(r"GFG%20Problems%20Solved-\w+", f"GFG%20Problems%20Solved-{gfg_solved}", readme_content)
readme_content = re.sub(r"GitHub%20Contributions-\w+", f"GitHub%20Contributions-{github_contributions}", readme_content)

# Write back to README.md
with open("README.md", "w", encoding="utf-8") as file:
    file.write(readme_content)
