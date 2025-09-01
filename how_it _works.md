### 🌦️ Rain Alert SMS Script — Step-by-Step Breakdown

This Python script checks the weather forecast using OpenWeatherMap and sends an SMS alert via Twilio if rain is expected. Here's how it works, step by step:

---

#### 1. **Imports and Constants**

    import requests
    from twilio.rest import Client
    from dotenv import dotenv_values
    from requests.exceptions import RequestException
    from functools import partial

- `requests`: For making HTTP calls to the weather API.  
- `twilio.rest.Client`: To send SMS messages via Twilio.  
- `dotenv_values`: Loads environment variables from a `.env` file.  
- `RequestException`: Handles HTTP errors gracefully.  
- `partial`: Used to preconfigure the config loader.

    RAIN_THRESHOLD = 700

- Weather condition codes below 700 indicate precipitation (rain, snow, etc.).

---

#### 2. **Configuration Loader**

    load_config = partial(dotenv_values, ".env")

- Loads key-value pairs from `.env` file.  
- Uses `partial` to fix the filename argument, making `load_config()` a zero-argument function.

---

#### 3. **Fetching the Forecast**

    def fetch_forecast(url, params):
        try:
            response = requests.get(url, params, timeout=10)
            response.raise_for_status()
            return response.json().get("list", [])
        except RequestException as e:
            return {"error": str(e)}

- Makes a GET request to OpenWeatherMap.  
- Returns a list of forecast entries or an error dictionary.

---

#### 4. **Rain Detection Logic**

    def forecast_indicates_rain(forecast):
        def extract_weather_id(item):
            try:
                return item["weather"][0]["id"]
            except (KeyError, IndexError, TypeError):
                return None

        return any(
            (weather_id := extract_weather_id(item)) is not None and weather_id < RAIN_THRESHOLD
            for item in forecast
        )

- Extracts weather condition codes from each forecast entry.  
- Uses the walrus operator `:=` for inline assignment and filtering.  
- Returns `True` if any forecast entry indicates rain.

---

#### 5. **SMS Message Builder**

    def build_sms(config):
        return {
            "body": "It will rain today! Don't forget to bring an umbrella!",
            "from_": config["TWILIO_PHONE_NUMBER"],
            "to": config["MY_PHONE_NUMBER"]
        }

- Constructs the SMS payload using config values.  
- Message body is hardcoded (but marked as a TODO for future customization).

---

#### 6. **Sending the SMS**

    def send_sms(account_sid, auth_token, sms_data):
        client = Client(account_sid, auth_token)
        return client.messages.create(**sms_data)

- Initializes Twilio client with credentials.  
- Sends the SMS using the provided data.

---

#### 7. **Main Execution Flow**

    def main():
        config = load_config()

        forecast_hours = int(config.get("FORECAST_HOURS"))
        forecast_timestamps = forecast_hours // 3

        url = config["API_ENDPOINT"]
        weather_params = {
            "lat": config["LATITUDE"],
            "lon": config["LONGITUDE"],
            "appid": config["API_KEY"],
            "cnt": forecast_timestamps
        }

        account_sid = config["TWILIO_ACCOUNT_SID"]
        auth_token = config["TWILIO_AUTH_TOKEN"]

        forecast = fetch_forecast(url, weather_params)
        rain_today = forecast_indicates_rain(forecast)

        if rain_today:
            sms_data = build_sms(config)
            message = send_sms(account_sid, auth_token, sms_data)
            print(f"Message sent: {message.sid}")
        else:
            print("It will not rain today.")

- Loads config values.  
- Calculates how many 3-hour forecast intervals to request.  
- Builds API parameters and fetches forecast.  
- Checks for rain and sends SMS if needed.

---

#### 8. **Entry Point**

    if __name__ == "__main__":
        main()

- Ensures the script runs only when executed directly (not imported).

---

### ✅ Summary

This script is a clean, functional approach to automating weather alerts via SMS. It emphasizes:
- **Functional purity** (pure functions, minimal side effects)  
- **Modularity** (clear separation of concerns)  
- **Extensibility** (marked TODOs for future improvements)
