
import requests
import json

def get_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    weather_data = response.json()

    if response.status_code == 200:
        main_weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        print(f"Weather in {city_name}: {main_weather} ({description}). The temperature is {temp} degrees Celsius.")
    else:
        print(f"Error getting weather data for {city_name}. HTTP response code: {response.status_code}")

# Get 'City' and 'your_api_key' from the user
city_name = input("Which city:")
api_key = "bf4501c4365c3180664200edc5b43f55"

# Call the function with the user's inputs
get_weather(city_name, api_key)
input()
