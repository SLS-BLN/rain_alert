import requests
from dotenv import load_dotenv, dotenv_values
from requests.exceptions import RequestException


def load_config(path=".env"):
    load_dotenv()
    return dotenv_values(path)


def build_forecast_url(endpoint, lat, lon, key):
    return f"{endpoint}?lat={lat}&lon={lon}&appid={key}"


def fetch_forecast(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        return {"error": str(e)}


def main():
    config = load_config()
    url = build_forecast_url(
        config["API_ENDPOINT"],
        config["LATITUDE"],
        config["LONGITUDE"],
        config["API_KEY"]
    )
    forecast = fetch_forecast(url)
    print(forecast)


if __name__ == "__main__":
    main()
