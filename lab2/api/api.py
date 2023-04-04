from fastapi import FastAPI, Header
from starlette.middleware.cors import CORSMiddleware

from common.auth import check_token
from common.config import Config
from common.utils import validate_date, get_last_decade, get_month_name
from common.weather_utils import agg_weather_by_mode, WeatherMode

from external_api.coordinates_api import get_coordinates
from external_api.news_api import get_news_ext
from external_api.weather_api import get_weather_ext

origins = [
    "*",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/coordinates/{city}")
async def get_city_coordinates(city: str, token: str = Header(None)):
    await check_token(token)
    return await get_coordinates(Config.WEATHER_API_TOKEN, city)


@app.get("/weather/{mode}/{city}")
async def get_weather(mode: str, city: str, start_date: str, end_date: str, token: str = Header(None)):
    await check_token(token)

    if not validate_date(start_date) or not validate_date(end_date):
        return {"error": "Incorrect dates - only dates from past"}

    available_modes = [mode.value for mode in WeatherMode]
    if mode not in available_modes:
        return {"error": f"Incorrect mode - available values: {available_modes}"}

    try:
        coordinates = await get_coordinates(Config.WEATHER_API_TOKEN, city)
        coordinates_data = coordinates.get("data", [])
    except Exception as e:
        return {"error": f"Error getting coordinates for {city}: {str(e)}"}

    try:
        result = [
            {
                "name": item.get("name"),
                "date": {"start": start_date, "end": end_date},
                "mode": mode,
                "weather": agg_weather_by_mode(
                    await get_weather_ext(start_date, end_date, item["lat"], item["lon"]),
                    mode,
                ),
            }
            for item in coordinates_data
        ]
        return result

    except Exception as e:
        return {"error": f"Error getting weather data for {city}. {str(e)}"}


@app.get("/news/{city}")
async def get_news(city: str, token: str = Header(None)):
    await check_token(token)

    try:
        coordinates = await get_coordinates(Config.WEATHER_API_TOKEN, city)
        coordinates_data = coordinates.get("data", [])[0]
    except Exception as e:
        return {"error": f"Error getting coordinates for {city}: {str(e)}"}

    try:
        default_radius = 30
        news = await get_news(coordinates_data.get("lat"), coordinates_data.get("lon"), default_radius)
        return news
    except Exception as e:
        return {"error": f"Error getting news data for {city}. {str(e)}"}


@app.get("/city-info/{city}")
async def get_city_info(city: str, token: str = Header(None)):
    await check_token(token)

    try:
        coordinates = await get_coordinates(Config.WEATHER_API_TOKEN, city)
        coordinates_data = coordinates.get("data", [])[0]
    except Exception as e:
        return {"error": f"Error getting coordinates for {city}: {str(e)}"}

    start_date, end_date = get_last_decade()
    try:
        weather_raw_data = await get_weather_ext(
            start_date,
            end_date,
            coordinates_data.get("lat"),
            coordinates_data.get("lon"),
        )
        weather_month = agg_weather_by_mode(weather_raw_data, WeatherMode.MONTH.value)
        weather_month_transformed = {get_month_name(item): "{:.2f}".format(value) for item, value in weather_month.items()}
        weather_year = agg_weather_by_mode(weather_raw_data, WeatherMode.YEAR.value)
        weather_year_transformed = {item: "{:.2f}".format(value) for item, value in weather_year.items()}

    except Exception as e:
        return {"error": f"Error getting weather data for {city}. {str(e)}"}

    try:
        default_radius = 30
        news = await get_news_ext(coordinates_data.get("lat"), coordinates_data.get("lon"), default_radius)
    except Exception as e:
        return {"error": f"Error getting news data for {city}. {str(e)}"}

    return {
        "name": coordinates_data.get("name"),
        "weather": {
            "months": weather_month_transformed,
            "years": weather_year_transformed,
        },
        "news": news,
    }
