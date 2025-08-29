import requests
import os

from twilio.rest import Client
from dotenv import load_dotenv, dotenv_values
from requests.exceptions import RequestException
from functools import partial

# OpenWeatherMap condition codes:
# 2xx = Thunderstorm, 3xx = Drizzle, 5xx = Rain, 6xx = Snow
# Codes < 700 indicate precipitation
RAIN_THRESHOLD = 700

# Pure function: loads config without side effects
load_config = partial(dotenv_values, ".env")

# Pure function: fetches forecast and returns result or error
def fetch_forecast(url, params):
    try:
        response = requests.get(url, params, timeout=10)
        response.raise_for_status()
        return response.json().get("list", [])
    except RequestException as e:
        return {"error": str(e)}

def forecast_indicates_rain(forecast):
    def extract_weather_id(item):
        try:
            return item["weather"][0]["id"]
        except (KeyError, IndexError, TypeError):
            return None

    # Assign weather_id inline using the walrus operator (:=).
    # This lets us check if it's valid and below the rain threshold in one expression.
    # Equivalent to:
    #   weather_id = extract_weather_id(item)
    #   if weather_id is not None and weather_id < RAIN_THRESHOLD: ...
    return any(
        (weather_id := extract_weather_id(item)) is not None and weather_id < RAIN_THRESHOLD
        for item in forecast
    )


def send_sms(account_sid, auth_token, config):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It will rain today!",
        from_=config["TWILIO_PHONE_NUMBER"],
        to=config["MY_PHONE_NUMBER"]
    )
    return message

def main():
    config = load_config()

    url = config["API_ENDPOINT"]
    weather_params = {
        "lat": config["LATITUDE"],
        "lon": config["LONGITUDE"],
        "appid": config["API_KEY"],
        # To limit the number of timestamps in the API response, set up cnt.
        # 3-hour steps - 4 timestamps = 12 hours
        "cnt": 4
    }

    account_sid = config["TWILIO_ACCOUNT_SID"]
    auth_token = config["TWILIO_AUTH_TOKEN"]

    forecast = fetch_forecast(url, weather_params)
    rain_today = forecast_indicates_rain(forecast)

    if rain_today:
        message = send_sms(account_sid, auth_token, config)
        print(f"Message sent: {message.sid}")
    else:
        print("It will not rain today.")


if __name__ == "__main__":
    main()
