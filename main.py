import requests

from twilio.rest import Client
from dotenv import dotenv_values
from requests.exceptions import RequestException
from functools import partial

# OpenWeatherMap condition codes:
# 2xx = Thunderstorm, 3xx = Drizzle, 5xx = Rain, 6xx = Snow
# Codes < 700 indicate precipitation
RAIN_THRESHOLD = 700

# TODO: Consider wrapping config values in a dataclass for type safety and clarity.


# Pure function: loads config without side effects
load_config = partial(dotenv_values, ".env")

# Pure function: fetches forecast and returns result or error
# TODO: Refactor to return a tuple (data, error) instead of mixing types for better functional purity.
def fetch_forecast(url, params):
    try:
        response = requests.get(url, params, timeout=10)
        response.raise_for_status()
        return response.json().get("list", [])
    except RequestException as e:
        return {"error": str(e)}

# TODO: Move extract_weather_id to top-level for reusability and easier testing.
def forecast_indicates_rain(forecast):
    def extract_weather_id(item):
        try:
            return item["weather"][0]["id"]
        except (KeyError, IndexError, TypeError):
            return None

    # Assign weather_id inline using the walrus operator ":=".
    # This lets us check if it's valid and below the rain threshold in one expression.
    # Equivalent to:
    #   weather_id = extract_weather_id(item)
    #   if weather_id is not None and weather_id < RAIN_THRESHOLD: ...
    return any(
        (weather_id := extract_weather_id(item)) is not None and weather_id < RAIN_THRESHOLD
        for item in forecast
    )

# TODO: Make SMS body customizable via config or template system.
def build_sms(config):
    return {
        "body": "It will rain today! Don't forget to bring an umbrella!",
        "from_": config["TWILIO_PHONE_NUMBER"],
        "to": config["MY_PHONE_NUMBER"]
    }

# TODO: Separate Twilio client creation from message sending for better testability.
def send_sms(account_sid, auth_token, sms_data):
    client = Client(account_sid, auth_token)
    return client.messages.create(**sms_data)

def main():
    config = load_config()

    forecast_hours = int(config.get("FORECAST_HOURS"))
    # OpenWeatherMap provides forecast data in fixed 3-hour intervals — this value is not configurable
    forecast_timestamps = forecast_hours // 3

    url = config["API_ENDPOINT"]
    weather_params = {
        "lat": config["LATITUDE"],
        "lon": config["LONGITUDE"],
        "appid": config["API_KEY"],
        # To limit the number of timestamps in the API response, set up cnt.
        "cnt": forecast_timestamps
    }

    account_sid = config["TWILIO_ACCOUNT_SID"]
    auth_token = config["TWILIO_AUTH_TOKEN"]

    forecast = fetch_forecast(url, weather_params)
    rain_today = forecast_indicates_rain(forecast)

    # TODO: Replace print statements with a pure logging function to improve testability.
    if rain_today:
        sms_data = build_sms(config)
        message = send_sms(account_sid, auth_token, sms_data)
        print(f"Message sent: {message.sid}")
    else:
        print("It will not rain today.")


if __name__ == "__main__":
    main()
