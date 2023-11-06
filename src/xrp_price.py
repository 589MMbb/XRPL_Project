import requests

def get_xrp_price():
    # The URL for the CoinGecko API endpoint for XRP
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd"

    # Make a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response as JSON
        data = response.json()
        # Get the price of XRP in USD
        xrp_price_usd = data['ripple']['usd']
        return xrp_price_usd
    else:
        print("Failed to retrieve XRP price")
        return None

# Example usage
price = get_xrp_price()
if price:
    print(f"The current price of XRP is: ${price}")
