import requests
from dotenv import load_dotenv, dotenv_values
from requests.exceptions import RequestException


def load_config(path=".env"):
    load_dotenv()
    return dotenv_values(path)


def fetch_forecast(url, params):
    try:
        response = requests.get(url, params, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        return {"error": str(e)}


def check_for_rain(forecast):
    for item in forecast:
        if item["weather"][0]["id"] < 700:
            return True
    return False


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

    forecast = fetch_forecast(url, weather_params)["list"]
    will_rain_today = check_for_rain(forecast)

    if will_rain_today:
        print("It will rain today!")
    else:
        print("It will not rain today.")


if __name__ == "__main__":
    main()
