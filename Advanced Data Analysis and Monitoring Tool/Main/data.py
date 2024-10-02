import requests
import json

def fetch_data_from_api(api_endpoint, params):
    """
    Function to fetch data from the API endpoint.
    
    Args:
    - api_endpoint: The URL of the API endpoint.
    - params: Dictionary containing any parameters to be sent with the request.
    
    Returns:
    - JSON response from the API.
    """
    try:
        response = requests.get(api_endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data from the API. Status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred while fetching data:", str(e))
        return None

def main():
    # Define the API endpoint URL
    api_endpoint = "http://www.cybersyndrome.net/plz.html"
    
    # Define parameters to be sent with the request (if any)
    params = {
        "limit": 100,  # Example parameter
        "category": "news"  # Example parameter
    }
    
    # Fetch data from the API
    data = fetch_data_from_api(api_endpoint, params)
    
    if data:
        # Process the fetched data
        # For demonstration purposes, let's just print the JSON response
        print(json.dumps(data, indent=4))
    else:
        print("Failed to fetch data. Check your API endpoint and parameters.")

if __name__ == "__main__":
    main()
