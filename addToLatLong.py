from geopy.geocoders import Nominatim
import secrets
import string

def getLatitudeLongitude(location, username):
    geolocator = Nominatim(user_agent=username)
    location = geolocator.geocode(location)

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

#Example usage:
location = "2306 E 3860 S, Saint George, Utah"
user = randomString(30)
latitude, longitude = getLatitudeLongitude(location, user)
if latitude is not None and longitude is not None:
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Location not found.")

