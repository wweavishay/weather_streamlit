import requests
import json
from datetime import datetime, timedelta, timezone
import pytz
import pandas as pd


API_KEY = "cc684ce23b3296f9598c4187825107eb"

def load_settings():
    try:
        with open('data/settings.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'timezone': 'UTC'}


def display_weather_image(temperature):
    if float(temperature) < 10:
        return "https://cdn-icons-png.flaticon.com/128/2469/2469994.png"  # Cold icon
    elif 10 <= float(temperature) < 20:
        return "https://cdn-icons-png.flaticon.com/128/1163/1163624.png"  # Moderate icon
    else:
        return "https://cdn-icons-png.flaticon.com/128/9231/9231728.png"  # Warm icon

def get_weather_info(city_name, country_name):
    weather_data = get_weather(city_name, country_name)
    if weather_data:
        temperature = weather_data.get("main", {}).get("temp")
        weather_conditions = weather_data.get("weather", [{}])[0].get("description")
        humidity = weather_data.get("main", {}).get("humidity")
        timezone_offset = weather_data.get("timezone")
        return temperature, weather_conditions, humidity, timezone_offset
    else:
        return None, None, None, None
def get_temperature_unit():
    settings = load_settings()
    return settings.get('temperature_unit', 'Celsius')

def set_temperature_unit(unit):
    if unit.lower() in ['celsius', 'fahrenheit']:
        settings = load_settings()
        settings['temperature_unit'] = unit.lower()
        save_settings(settings)
        return f"Temperature unit preference set to: {unit.capitalize()}."
    else:
        return "Invalid temperature unit. Please enter either Celsius or Fahrenheit."

def save_settings(settings):
    with open('data/settings.json', 'w') as f:
        json.dump(settings, f)

def set_default_location(city_name, country_name=None, timezone_name=None):
    settings = load_settings()

    if timezone_name is None:
        timezone_name = 'UTC'

    if country_name:
        settings['default_location'] = {'city': city_name, 'country': country_name, 'timezone': timezone_name}
    else:
        settings['default_location'] = {'city': city_name, 'timezone': timezone_name}

    save_settings(settings)
    return "Default location set successfully."


def get_default_location():
    # Assuming settings is a dictionary containing default location information
    settings = load_settings()
    default_location = settings.get('default_location')

    if default_location:
        default_city = default_location.get('city')
        default_country = default_location.get('country')
        default_timezone = default_location.get('timezone', 'UTC')

        return default_city, default_country, default_timezone
    else:
        return None


def get_weather(city_name, country_name=None):
    if country_name:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name},{country_name}&appid={API_KEY}&units=metric"
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: Failed to retrieve weather data.")
        return None

    data = response.json()

    if data.get("cod") == 404:
        print("Error: city not found.")
        return None

    weather_info = {
        "temperature": data["main"]["temp"],
        "weather_conditions": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "timezone": data.get("timezone", 0)
    }

    return weather_info



def compare_weather_and_time(default_city, default_country, default_timezone, user_city, user_country, user_timezone):
    default_timezone = pytz.timezone(default_timezone)
    user_timezone = pytz.timezone(user_timezone)

    default_data = get_weather(default_city, default_country)
    user_data = get_weather(user_city, user_country)

    if default_data is not None and user_data is not None:
        default_temperature = float(default_data['temperature'])
        user_temperature = float(user_data['temperature'])

        # Get current time for default location
        default_time = datetime.now(default_timezone)

        # Get current time for user location
        user_time = datetime.now(user_timezone)

        # Create response data
        comparison_data = {
            'default_location': {
                'city': default_city,
                'country': default_country,
                'temperature': default_temperature,
                'weather_conditions': default_data['weather_conditions'],
                'humidity': default_data['humidity'],
                'time': default_time.strftime("%Y-%m-%d %H:%M:%S"),
                'timezone': default_timezone.zone
            },
            'user_location': {
                'city': user_city,
                'country': user_country,
                'temperature': user_temperature,
                'weather_conditions': user_data['weather_conditions'],
                'humidity': user_data['humidity'],
                'time': user_time.strftime("%Y-%m-%d %H:%M:%S"),
                'timezone': user_timezone.zone
            }
        }

        # Calculate time difference
        time_difference = user_time - default_time
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        comparison_data['time_difference'] = f"{hours} hours and {minutes} minutes"

        return comparison_data
    else:
        return {"error": "Weather data not available for one or both locations."}