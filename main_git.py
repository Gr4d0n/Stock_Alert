import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "----------------------------------"
NEWS_ENDPOINT = "-------------------------------------"

STOCK_API_KEY = "---------------------------------"
NEWS_API_KEY = "-------------------------------------"

account_sid = "---------------------------------------"
sms_auth_token = "----------------------------------------"
sms_number = '-------------------------------'

stock_params = {"function": "TIME_SERIES_DAILY",
                "symbol": STOCK_NAME,
                "apikey": STOCK_API_KEY
                }
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]

yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]

day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))

diff = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

diff_percentage = difference/float(yesterday_closing_price) * 100
if diff_percentage > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"][:3]
    message = [f"{COMPANY_NAME}: 🔺{"%.2f" % diff_percentage}% \nHeadline: {article['title']}, \nBrief: {article['description']}" if diff > 0 else f"{COMPANY_NAME}: 🔻{"%.2f" % diff_percentage}% \nHeadline: {article['title']}, \nBrief: {article['description']}" for article in articles]


    client = Client(account_sid, sms_auth_token)

    for x in message:
        sms = client.messages.create(
            body=x,
            from_=sms_number,
            to='-------------'
        )

    print("Message Sent")