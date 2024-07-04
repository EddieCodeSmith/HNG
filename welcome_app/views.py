from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import requests

@require_GET
def hello(request):
    visitor_name = request.GET.get('visitor_name', "mark")
    client_ip = request.META.get('REMOTE_ADDR')
    weather_api = '06f0ab4ef5e53b544d63f0a72f870b21'
    location_api = "f195617ff6f34b4e8c606d052e0969d7"
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0]
    else:
        client_ip = request.META.get("REMOTE_ADDR")
        
    try:
        location_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={location_api}&ip={client_ip}"
        location_response = requests.get(location_url)
        location_data = location_response.json()
        city = location_data.get("city", "New York")
    except requests.RequestException as e:
        print(f"Location API Request Failed: {e}")
        city = "New York"

    try:
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        if weather_data.get("cod") == 200:
            temperature = weather_data['main']['temp']
        else:
            temperature = None
    except requests.RequestException as e:
        print(f"Weather API Request Failed: {e}")
        temperature = None

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} in {city}"
    response = {
        'client_ip': client_ip,
        'location': city,
        'greeting': greeting,
    }
    return JsonResponse(response)