import os
import requests
from urllib.parse import quote_plus

def download_city_background(city: str) -> str | None:
    """
    Downloads a city background image from Unsplash and stores it in /static/city_photos.
    Returns relative path to be used in templates.
    """
    # sauberer Dateiname
    safe_name = quote_plus(city.lower())
    filename = f"{safe_name}.jpg"

    # absoluter Pfad zur Datei
    folder_path = os.path.join(os.path.dirname(__file__), "..", "static", "city_photos")
    full_path = os.path.join(folder_path, filename)

    if os.path.exists(full_path):
        return f"/static/city_photos/{filename}"

    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": "Client-ID K5UNzccA5Hdmt5iM41OgovwMCVQ1XJwYUlE3jFuQdS4"}
    params = {
        "query": city,
        "per_page": 1,
        "orientation": "landscape",
        "content_filter": "high"
    }

    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        results = res.json().get("results")
        if not results:
            return None

        img_url = results[0]["urls"]["regular"]
        img_data = requests.get(img_url).content

        os.makedirs(folder_path, exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(img_data)

        print(f"✅ Image saved as '{full_path}'")
        return f"/static/city_photos/{filename}"

    except Exception as e:
        print(f"❌ Error downloading city image: {e}")
        return None
