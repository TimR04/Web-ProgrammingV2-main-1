"""
Wikipedia Summary Module

Fetches a short city description from Wikipedia using the REST API.

API used:
- Wikipedia REST API: https://www.mediawiki.org/wiki/REST_API
"""

import requests


def get_wikipedia_summary(topic: str, lang: str = "de") -> str:
    """
    Fetch a summary text for a given topic from Wikipedia.

    Args:
        topic (str): Page title or search term (e.g., "Berlin").
        lang (str): Language code (default: "de").

    Returns:
        str: Summary extract text or fallback message on error.
    """
    try:
        topic_clean = topic.replace(" ", "_")
        url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{topic_clean}"
        response = requests.get(url, timeout=5, verify=False)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "❌ No description available.")
        else:
            print(f"❌ Wikipedia API error: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Error during Wikipedia call: {e}")
    return "❌ No description available."
