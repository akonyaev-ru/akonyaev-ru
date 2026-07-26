import urllib.request
import re
import json

def update_views_json():
    # 1. Fetch SVG from komarev
    url = "https://komarev.com/ghpvc/?username=akonyaev-ru"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        svg_content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch komarev SVG: {e}")
        return

    # 2. Extract number using regex. Komarev SVG usually has the number in a <text> tag at the end.
    # Looking for a pattern like <text ...>1234</text>
    # Since there are two <text> tags (one for 'Profile Views', one for the number), we find all numbers.
    matches = re.findall(r'<text[^>]*>([0-9,]+)</text>', svg_content)
    
    if not matches:
        print("Could not find view count in SVG.")
        return
    
    # The count is usually the last match
    count_str = matches[-1]
    
    # 3. Write Shields.io JSON endpoint
    endpoint_data = {
        "schemaVersion": 1,
        "label": "Profile Views",
        "message": count_str,
        "color": "0e75b6",
        "style": "for-the-badge",
        "namedLogo": "github",
        "logoColor": "white"
    }
    
    with open("views.json", "w", encoding="utf-8") as f:
        json.dump(endpoint_data, f, indent=2)
        
    print(f"Successfully updated views.json with count: {count_str}")

if __name__ == "__main__":
    update_views_json()
