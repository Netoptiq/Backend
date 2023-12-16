import requests
import geohash2
def get_coordinates_from_ip(ip_address):
    # Make a request to the ipinfo.io API
    response = requests.get(f"http://ipinfo.io/{ip_address}/json")
    
    # Parse the JSON response
    data = response.json()
    
    # Extract latitude and longitude from the response
    if "loc" in data:
        latitude, longitude = map(float, data["loc"].split(","))
        return latitude, longitude
    else:
        # If the "loc" field is not present in the response, handle the error accordingly
        print(f"Unable to retrieve coordinates for IP address {ip_address}")
        return None

def ip_to_geohash(ip_address):
    coordinates = get_coordinates_from_ip(ip_address)
    print(coordinates)
    if coordinates:
        latitude, longitude = coordinates
        
        # Convert coordinates to geohash
        geohash = geohash2.encode(latitude, longitude)
        
        return geohash
    else:
        return None

# Example usage
ip_address = "8.8.8.8"  # Replace with the desired IP address
result_geohash = ip_to_geohash(ip_address)

if result_geohash:
    print(f"Geohash for {ip_address}: {result_geohash}")
