import httpx


async def get_weather_ext(start_date: str, end_date, latitude: str, longitude: str):
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max&timezone=GMT"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            data = response.json()

            return {
                "date": data["daily"]["time"],
                "temperature": data["daily"]["temperature_2m_max"],
            }
        except httpx.HTTPStatusError:
            return {"error": "Coordinates api error"}
