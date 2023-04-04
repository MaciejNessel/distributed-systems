import httpx

from common.config import Config


async def get_news_ext(latitude: str, longitude: str, radius: int):
    # Max 50 request per day !
    url = f"https://api.worldnewsapi.com/search-news?api-key={Config.NEWS_API_TOKEN}&location-filter={latitude},{longitude},{radius}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            data = response.json()
            return data.get("news", [])
        except httpx.HTTPStatusError:
            return {"error": "News API error"}
