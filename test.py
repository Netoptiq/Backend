import requests

def fetch_threat_intel(api_key, limit=10):
    url = f'https://otx.alienvault.com/api/v1/indicators/IPv4/?limit={limit}'

    headers = {
        'Content-Type': 'application/json',
        'X-OTX-API-KEY': api_key,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        threat_intel_data = response.json()
        return threat_intel_data['indicators']
    else:
        print(f"Error fetching threat intelligence: {response.status_code}")
        return None

# Example usage:
otx_api_key = '3d4f925f687e1722d4243bdfee5f69071d1aca2a149511171220c73f57260789'
threat_intel_data = fetch_threat_intel(otx_api_key)

if threat_intel_data:
    for indicator in threat_intel_data:
        print(f"Indicator: {indicator['indicator']}, Type: {indicator['type']}")
