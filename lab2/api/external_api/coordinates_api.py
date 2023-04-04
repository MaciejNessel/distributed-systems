import httpx


async def get_coordinates(token: str, city: str):
    url = f"https://us1.locationiq.com/v1/search.php?key={token}&q={city}&format=json"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            data = response.json()
            data_transform = coordinates_transform(data)
            if len(data_transform):
                return {"status": "ok", "data": data_transform}
            else:
                return {"error": "City was not found"}
        except httpx.HTTPStatusError:
            return {"error": "Coordinates API error"}


def coordinates_transform(data):
    required_types = ["city", "village", "administrative"]
    data_filtered = [item for item in data if item.get("type") in required_types]

    if isinstance(data, list):
        unique_items = {}
        for item in data_filtered:
            key = f"{item.get('lat', '')[:3]},{item.get('lon', '')[:3]}"
            unique_items[key] = {
                "name": item.get("display_name"),
                "lat": item.get("lat"),
                "lon": item.get("lon"),
            }

        return list(unique_items.values())
    else:
        return []
