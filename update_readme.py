import os
import requests
from datetime import datetime

LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
LEETCODE_CSRF = os.getenv("LEETCODE_CSRF")
GH_PAT = os.getenv("GH_PAT")  # GitHub token

USERNAME = "snehilsr91"
REPO_NAME = "snehilsr91"

# LeetCode API endpoint
LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION}; csrftoken={LEETCODE_CSRF}",
    "x-csrftoken": LEETCODE_CSRF,
    "Referer": "https://leetcode.com",
}

# GraphQL query to fetch solved problems
QUERY = {
    "operationName": "userProfileUserQuestionProgressV2",
    "variables": {"userSlug": "snehilsr91"}, 
    "query": """
        query userProfileUserQuestionProgressV2($userSlug: String!) {
            userProfileUserQuestionProgressV2(userSlug: $userSlug) {
                numAcceptedQuestions {
                    difficulty
                    count
                }
                numFailedQuestions {
                    difficulty
                    count
                }
                numUntouchedQuestions {
                    difficulty
                    count
                }
            }
        }
    """,
}

def fetch_leetcode_stats():
    try:
        response = requests.post(LEETCODE_GRAPHQL_URL, json=QUERY, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        stats = data["data"]["userProfileUserQuestionProgressV2"]["numAcceptedQuestions"]

        easy = next(item["count"] for item in stats if item["difficulty"] == "EASY")
        medium = next(item["count"] for item in stats if item["difficulty"] == "MEDIUM")
        hard = next(item["count"] for item in stats if item["difficulty"] == "HARD")

        return easy, medium, hard
    except Exception as e:
        print("Error fetching LeetCode stats:", e)
        return 0, 0, 0

def update_readme(easy, medium, hard):
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()

        start_marker = "<!-- LEETCODE:START -->"
        end_marker = "<!-- LEETCODE:END -->"

        new_stats = f"**LeetCode Stats**\n\n✅ Easy: {easy} | 🟠 Medium: {medium} | 🔴 Hard: {hard}\n_Last updated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}_"

        if start_marker in content and end_marker in content:
            before = content.split(start_marker)[0]
            after = content.split(end_marker)[1]
            content = f"{before}{start_marker}\n{new_stats}\n{end_marker}{after}"
        else:
            content += f"\n{start_marker}\n{new_stats}\n{end_marker}\n"

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)

        print("README.md updated successfully.")
    except Exception as e:
        print("Error updating README.md:", e)

if __name__ == "__main__":
    easy, medium, hard = fetch_leetcode_stats()
    update_readme(easy, medium, hard)
