import requests
import re

# Your usernames
leetcode_username = "snehilsr91"
github_username = "snehilsr91"
gfg_username = "snehilsr91"  # Placeholder for scraping

# Fetch LeetCode stats
leetcode_api = f"https://leetcode-stats-api.herokuapp.com/{leetcode_username}"
leetcode_response = requests.get(leetcode_api)

# Debugging: Print API response
print(f"🔍 Debug: LeetCode API Status = {leetcode_response.status_code}")
print(f"🔍 Debug: LeetCode API Response = {leetcode_response.text}")

# Check if the API returned a valid response
if leetcode_response.status_code == 200:
    try:
        leetcode_data = leetcode_response.json()
        leetcode_solved = leetcode_data.get("totalSolved", "N/A")
    except requests.exceptions.JSONDecodeError:
        print("❌ Error: Failed to decode LeetCode API response")
        leetcode_solved = "400+"
else:
    print(f"❌ Error: Failed to fetch LeetCode stats. HTTP Status: {leetcode_response.status_code}")
    leetcode_solved = "400+"

# Fetch GitHub Contributions (using public repos as a proxy)
github_api = f"https://api.github.com/users/{github_username}"
github_response = requests.get(github_api)

if github_response.status_code == 200:
    github_data = github_response.json()
    github_contributions = github_data.get("public_repos", "N/A")  # Approximate contribution count
else:
    print(f"❌ Error: Failed to fetch GitHub stats. HTTP Status: {github_response.status_code}")
    github_contributions = "N/A"

# Placeholder for GFG (Web scraping required)
gfg_solved = "25+"

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

print("✅ Successfully updated README.md!")
