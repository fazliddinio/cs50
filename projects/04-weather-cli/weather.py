#!/usr/bin/env python3
"""
Weather CLI - Get current weather for any city
Uses OpenWeatherMap API
"""
import argparse
import json
import os
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from datetime import datetime


# Demo mode - simulated weather data
DEMO_MODE = True


def get_weather_demo(city: str) -> dict:
    """Get simulated weather data for demo purposes."""
    import random
    conditions = ["Clear", "Clouds", "Rain", "Drizzle", "Snow", "Mist"]
    return {
        "city": city,
        "country": "US",
        "temp": round(random.uniform(-5, 35), 1),
        "feels_like": round(random.uniform(-8, 38), 1),
        "humidity": random.randint(30, 90),
        "pressure": random.randint(990, 1030),
        "wind_speed": round(random.uniform(0, 20), 1),
        "condition": random.choice(conditions),
        "description": "moderate weather",
    }


def get_weather_api(city: str, api_key: str) -> dict:
    """Get real weather from OpenWeatherMap API."""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    url = f"{base_url}?{urlencode(params)}"
    
    try:
        req = Request(url, headers={"User-Agent": "WeatherCLI/1.0"})
        with urlopen(req) as response:
            data = json.loads(response.read())
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "condition": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
            }
    except Exception as e:
        return {"error": str(e)}


def display_weather(weather: dict) -> None:
    """Display weather information."""
    if "error" in weather:
        print(f"❌ Error: {weather['error']}")
        return
    
    # Weather icons
    icons = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Snow": "❄️",
        "Thunderstorm": "⛈️",
        "Mist": "🌫️",
        "Fog": "🌫️",
    }
    
    icon = icons.get(weather["condition"], "🌡️")
    
    print(f"\n{icon} Weather in {weather['city']}, {weather['country']}")
    print("=" * 40)
    print(f"🌡️  Temperature: {weather['temp']}°C")
    print(f"🤔 Feels like:  {weather['feels_like']}°C")
    print(f"💧 Humidity:    {weather['humidity']}%")
    print(f"🌬️  Wind:        {weather['wind_speed']} m/s")
    print(f"📊 Pressure:    {weather['pressure']} hPa")
    print(f"📝 Condition:   {weather['condition']} - {weather['description']}")
    print("=" * 40)


def main():
    parser = argparse.ArgumentParser(description="Weather CLI")
    parser.add_argument("city", help="City name")
    parser.add_argument("-k", "--api-key", 
                       default=os.environ.get("OPENWEATHER_API_KEY"),
                       help="OpenWeatherMap API key")
    
    args = parser.parse_args()
    
    if DEMO_MODE:
        weather = get_weather_demo(args.city)
    else:
        if not args.api_key:
            print("❌ API key required. Set OPENWEATHER_API_KEY or use -k")
            return
        weather = get_weather_api(args.city, args.api_key)
    
    display_weather(weather)


if __name__ == "__main__":
    main()
