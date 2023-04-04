from enum import Enum
import pandas as pd


class WeatherMode(Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


def preprocess_weather_data(data) -> pd.DataFrame:
    df = pd.DataFrame({"date": data["date"], "temperature": data["temperature"]})
    df = df.dropna()
    return df


def get_daily_weather(data):
    df = preprocess_weather_data(data)
    daily_temperatures = df.groupby(["date"]).mean()
    return daily_temperatures["temperature"]


def get_weekly_weather(data):
    df = preprocess_weather_data(data)
    df["week"] = pd.DatetimeIndex(df["date"]).week
    weekly_temperatures = df.groupby(["week"]).mean()
    return weekly_temperatures["temperature"]


def get_monthly_weather(data):
    df = preprocess_weather_data(data)
    df["month"] = pd.DatetimeIndex(df["date"]).month
    daily_temperatures = df.groupby(["month"]).mean()
    return daily_temperatures["temperature"]


def get_year_weather(data):
    df = preprocess_weather_data(data)
    df["year"] = pd.DatetimeIndex(df["date"]).year
    daily_temperatures = df.groupby(["year"]).mean()
    return daily_temperatures["temperature"]


def agg_weather_by_mode(data, mode):
    match mode:
        case WeatherMode.DAY.value:
            return get_daily_weather(data)
        case WeatherMode.WEEK.value:
            return get_weekly_weather(data)
        case WeatherMode.MONTH.value:
            return get_monthly_weather(data)
        case WeatherMode.YEAR.value:
            return get_year_weather(data)
