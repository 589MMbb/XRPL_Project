import requests

def get_xrp_price():

    url = "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd"


    response = requests.get(url)


    if response.status_code == 200:
        
        data = response.json()
     
        xrp_price_usd = data['ripple']['usd']
        return xrp_price_usd
    else:
        print("Failed to retrieve XRP price")
        return None

# Example usage
price = get_xrp_price()
if price:
    print(f"The current price of XRP is: ${price}")
