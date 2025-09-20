import os
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

# load local .env when running locally (do NOT commit .env)
load_dotenv()

app = Flask(__name__)

API_KEY = os.environ.get("OPENWEATHER_API_KEY")  # set on host or in .env locally

def get_weather(city):
    if not API_KEY:
        return {"error": "API key not set. Set OPENWEATHER_API_KEY."}
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    resp = requests.get(url, params=params, timeout=10)
    if resp.status_code != 200:
        return {"error": f"City not found or API error ({resp.status_code})"}
    data = resp.json()
    return {
        "city": data.get("name"),
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].title()
    }

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if city:
            weather = get_weather(city)
        else:
            weather = {"error": "Please enter a city name."}
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    # dev server
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
