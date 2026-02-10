import requests

def get_location_from_ip():
    services = [
        # Service 1
        "https://ipapi.co/json/",
        # Service 2
        "http://ip-api.com/json/",
        # Service 3
        "https://ipinfo.io/json"
    ]

    for url in services:
        try:
            r = requests.get(url, timeout=3)
            if r.status_code != 200:
                continue

            data = r.json()

            city = (
                data.get("city")
                or data.get("town")
                or data.get("regionName")
            )

            country = (
                data.get("country_name")
                or data.get("country")
            )

            if city:
                return f"{city}, {country or 'India'}"

        except Exception:
            continue

    # FINAL HARD FALLBACK (never return None)
    return "Delhi, India"
