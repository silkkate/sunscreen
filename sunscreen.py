import requests
import ssl
import certifi
import geopy.geocoders
from config import sun_api
from geopy.geocoders import Nominatim
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geolocator = Nominatim(user_agent="sunscreen.py")

while True:
    zipcode = input("Input your zipcode: ")
    location = geolocator.geocode(zipcode)
    if zipcode.isalpha():
        print("Invalid zipcode. Try again.")
        continue
    elif location:
        lat = location.latitude
        lon = location.longitude
        break
    else:
        print("Invalid zipcode. Try again.")
        continue

url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&appid={sun_api}"

response = requests.get(url)
data = response.json()

if response.status_code == 200:
    current_uvi = data["current"]["uvi"]
    uvi_float = float(current_uvi)
    if 0 <= uvi_float < 3:
        print(f"UV index is low. No sunscreen needed.")
    elif 3 <= uvi_float < 7:
        print("UV index is moderate. Apply SPF15 or higher.")
    else:
        print("UV index is high. Wear high SPF protection (30+) and seek shade whenever possible.")

