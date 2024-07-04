from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def hello(request):
    visitor_name = request.GET.get('visitor_name')
    client_ip = request.META.get('REMOTE ADDR')
    location =  "New York"
    temperature = "11 Degrees Celcius"
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} in {location}"
    
    response = {
        'client_ip':client_ip,
        'location':location,
        'greeting':greeting,
    }

    return JsonResponse(response)
