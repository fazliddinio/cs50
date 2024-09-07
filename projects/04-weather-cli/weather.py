#!/usr/bin/env python3
"""Weather CLI"""
import random

def get_weather_demo(city):
    conditions = ["Clear", "Clouds", "Rain"]
    return {"city": city, "temp": round(random.uniform(-5,35),1), "condition": random.choice(conditions)}

def display_weather(w):
    print(f"Weather in {w['city']}: {w['temp']}C {w['condition']}")

if __name__ == "__main__":
    import sys
    city = sys.argv[1] if len(sys.argv) > 1 else "London"
    display_weather(get_weather_demo(city))

# API integration
