from geopy.geocoders import Nominatim
import secrets
import string

def getLatitudeLongitude(location):
    user = randomString(30)
    geolocator = Nominatim(user_agent=user)
    location = geolocator.geocode(location, timeout=20)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None, None


def randomString(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

#location = "2306 E 3860 S, Saint George, UT"
location = "200 N 200 E, St. George, UT"
#location = "New York City, USA"
latitude, longitude = getLatitudeLongitude(location)
if latitude is not None and longitude is not None:
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Location not found.")

