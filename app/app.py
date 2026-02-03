from flask import Flask
import os

app = Flask(__name__)

@app.get("/")
def home():
    app_name = os.getenv("APP_NAME", "unknown")
    app_color = os.getenv("APP_COLOR", "none")
    api_key = os.getenv("API_KEY", "missing")
    return {
        "app": app_name,
        "color": app_color,
        "api_key_present": api_key != "missing"
    }

@app.get("/healthz")
def healthz():
    return "ok", 200

@app.get("/readyz")
def readyz():
    # i ekte liv ville du sjekket db/avhengigheter
    return "ready", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
