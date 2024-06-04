import streamlit as st
import re
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Download NLTK data if not already downloaded
nltk.data.path.append("/path/to/nltk_data")

# Initialize NLTK stemmer and lemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Initialize stemmer and lemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Function to get weather data from OpenWeather API
def get_weather(city):
    api_key = 'cc684ce23b3296f9598c4187825107eb'  # Replace with your OpenWeather API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    return response.json()

# Function to tokenize, stem, and lemmatize user input
def preprocess_input(user_input):
    tokens = word_tokenize(user_input.lower())
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in stemmed_tokens]
    return ' '.join(lemmatized_tokens)

# Function to parse user input and determine the query type and city
def parse_input(user_input):
    detected_city = None
    if 'wind' in user_input:
        return 'wind_speed', None
    elif 'temp' in user_input or 'hot' in user_input or 'cold' in user_input:
        return 'temperature', None
    elif 'humidity' in user_input:
        return 'humidity', None
    else:
        patterns = {
            'general': r'weather in (\w+)',
            'sunny_rainy': r'is it (sunny|rainy) in (\w+)',
            'cloudy': r'is it cloudy in (\w+)',
            'detailed': r'show all detail for (\w+)',
            'general_short': r'(\w+)\s+in\s+(\w+)',
        }

        for query_type, pattern in patterns.items():
            match = re.search(pattern, user_input)
            if match:
                if query_type in ['sunny_rainy', 'cloudy', 'general_short']:
                    return query_type, match.groups()
                else:
                    return query_type, (match.group(1),)
            # Attempt to detect a city even if the pattern isn't fully matched
            city_match = re.search(r'(\w+)', user_input)
            if city_match:
                detected_city = city_match.group(1)
        return None, detected_city

# Function to generate a response based on the weather data and query type
def generate_response(query_type, query_params, weather_data):
    if weather_data['cod'] != 200:
        return "Sorry, I couldn't find the weather for that location."

    city = weather_data['name']
    country = weather_data['sys']['country']
    description = weather_data['weather'][0]['description']
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    cloudy = 'clouds' in description

    # Apply rules
    temp_desc = "cold" if temp < 10 else "hot" if temp > 30 else "moderate"
    humidity_desc = "high" if humidity > 50 else "low"
    wind_desc = "high" if wind_speed > 5 else "low"

    if query_type == 'general':
        return f"The weather in {city}, {country} is currently {description} with a temperature of {temp}°C, which is considered {temp_desc}."
    elif query_type == 'sunny_rainy' or query_type == 'general_short':
        condition = query_params[0]
        if (condition == 'sunny' and 'sun' in description) or (condition == 'rainy' and 'rain' in description):
            return f"Yes, it is currently {condition} in {city}."
        elif condition == 'weather':
            return f"The weather in {city}, {country} is currently {description} with a temperature of {temp}°C, which is considered {temp_desc}."
        else:
            return f"No, it is not {condition} in {city}."
    elif query_type == 'humidity':
        return f"The humidity in {city}, {country} is currently {humidity}%, which is considered {humidity_desc}."
    elif query_type == 'wind_speed':
        return f"The wind speed in {city}, {country} is currently {wind_speed} m/s ({wind_desc})."
    elif query_type == 'cloudy':
        if cloudy:
            return f"Yes, it is currently cloudy in {city}."
        else:
            return f"No, it is not cloudy in {city}."
    elif query_type == 'detailed' or query_type is None:
        details = (
            f"Weather details for {city}, {country}:\n"
            f"- Description: {description}\n"
            f"- Temperature: {temp}°C ({temp_desc})\n"
            f"- Humidity: {humidity}% ({humidity_desc})\n"
            f"- Pressure: {pressure} hPa\n"
            f"- Wind Speed: {wind_speed} m/s ({wind_desc})\n"
        )
        return details

# Main chatbot function
def chatbot(user_input):
    responses = []
    processed_input = preprocess_input(user_input)
    query_type, query_params = parse_input(processed_input)

    if query_type and query_params:
        city = query_params[-1]
        weather_data = get_weather(city)
        response = generate_response(query_type, query_params, weather_data)
        responses.append(response)
    elif query_params:
        city = query_params
        weather_data = get_weather(city)
        response = generate_response('detailed', (city,), weather_data)
        responses.append(response)
    else:
        responses.append("Sorry, I didn't understand that. Please ask about the weather.")

    return responses

if __name__ == "__main__":
    user_input = input("You: ")
    responses = chatbot(user_input)
    for response in responses:
        print("Bot:", response)
