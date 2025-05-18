import os
from serpapi import GoogleSearch

def search_serpapi_inspo(query, num_results=5):
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return [{"error": "❌ Missing SerpAPI key."}]

    params = {
        "engine": "google",
        "q": query,
        "tbm": "isch",
        "api_key": api_key,
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    images = results.get("images_results", [])
    formatted = []

    for img in images[:num_results]:
        formatted.append({
            "title": img.get("title", "Untitled"),
            "image_url": img.get("original"),
            "source": img.get("link")
        })

    return formatted
