"""Refresh the shields.io endpoint JSON consumed by README.md.

The profile-views counter used to live here too, but it was scraping
komarev.com for a number that nothing incremented: the README stopped
embedding komarev's tracking pixel in 284f4ed, so the count was frozen at 9
for the entire life of views.json. Scraping it from CI never moved it --
komarev counts views of its own image, not requests to it from a workflow.
Removed rather than restored, so the profile carries no third-party tracker.
"""
import urllib.request
import json


def update_stars_json():
    url = "https://api.github.com/users/akonyaev-ru/repos?per_page=100"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        repos = json.loads(response.read().decode('utf-8'))
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    except Exception as e:
        print(f"Failed to fetch repos for stars: {e}")
        return

    endpoint_data = {
        "schemaVersion": 1,
        "label": "Total Stars",
        "message": str(total_stars),
        "color": "ffb000",
        "style": "flat",
        "namedLogo": "github",
        "logoColor": "white"
    }
    
    with open("stars.json", "w", encoding="utf-8") as f:
        json.dump(endpoint_data, f, indent=2)
        
    print(f"Successfully updated stars.json with count: {total_stars}")

if __name__ == "__main__":
    update_stars_json()
