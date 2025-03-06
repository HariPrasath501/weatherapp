from django.shortcuts import render 
from django.contrib import messages
import requests
import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'
    
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=56afe594a50b475d97342f08b3ea3dda'
    PARAMS = {'units': 'metric'}
    
    API_KEY = 'AIzaSyDBn74C7oVQfZDRcF9BowglffenT26HDUE'
    SEARCH_ENGINE_ID = 'f764e84ce1ab44ee0'
    
    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"
    
    data = requests.get(city_url).json()
    search_items = data.get("items")
    
    # Check if search_items is None or too short
    if search_items and len(search_items) > 1:
        image_url = search_items[1]['link']
    else:
        image_url = "/static/default.jpg"  # Provide a default image in case of API failure
    
    try:
        data = requests.get(url, PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
    
        day = datetime.date.today()
        return render(request, 'index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except KeyError:
        exception_occurred = True
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()
        
        return render(request, 'index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': exception_occurred,
            'image_url': image_url  # Even if API fails, show a fallback image
        })
