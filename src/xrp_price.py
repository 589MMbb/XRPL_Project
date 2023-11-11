import requests

def get_xrp_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    xrp_price = data['ripple']['usd']
    return xrp_price

# Now you can call the function and it will return the current price of XRP
price = get_xrp_price()
print(f"The current price of XRP is: ${price}")

