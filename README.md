# ☔ Rain Alert

Rain Alert is a Python-based notification tool that checks the weather forecast using the OpenWeatherMap API and sends an SMS alert via Twilio if rain is expected in the upcoming hours. It is designed for simplicity, configurability, and automation, making it suitable for personal use, smart home setups, or weather-aware workflows.

---

## 📌 Features

- Detects precipitation using OpenWeatherMap condition codes
- Sends SMS alerts via Twilio when rain is forecasted
- Configurable forecast window via `.env`
- Validates environment configuration at runtime
- Clean, modular code with functional purity

---

## 📁 Project Structure

    rain_alert/
    ├── main.py               # Core script logic
    ├── .env.example          # Environment configuration template
    ├── .gitignore            # Git exclusions
    ├── README.md             # Project documentation
    └── requirements.txt      # Python dependencies

---

## ⚙️ Installation

1. Clone the repository

        git clone https://github.com/SLS-BLN/rain_alert.git
        cd rain_alert

2. Install dependencies

        pip install -r requirements.txt

3. Configure environment

        cp .env.example .env

   Edit `.env` with your API keys, location, and phone numbers.

---

## 🌐 API Reference

### OpenWeatherMap
- Endpoint: `https://api.openweathermap.org/data/2.5/forecast`
- Forecast interval: Fixed 3-hour blocks
- Condition codes:
  - `2xx` = Thunderstorm
  - `3xx` = Drizzle
  - `5xx` = Rain
  - `6xx` = Snow
  - Codes `< 700` indicate precipitation

### Twilio
- Used to send SMS alerts
- Requires:
  - `TWILIO_ACCOUNT_SID`
  - `TWILIO_AUTH_TOKEN`
  - `TWILIO_PHONE_NUMBER`
  - `MY_PHONE_NUMBER`

---

## 🐞 Known Issues / TODOs

- [ ] Replace `print()` with structured logging
- [ ] Add unit tests with mocks for API and Twilio
- [ ] Wrap config in a dataclass for type safety
- [ ] Make SMS body customizable via template or config
- [ ] Add Docker support for deployment

## 🤖 AI Assistance Disclosure

This project was developed with the support of AI tools to accelerate prototyping and improve architectural decisions. All code has been reviewed and customized to reflect personal understanding and intent.
