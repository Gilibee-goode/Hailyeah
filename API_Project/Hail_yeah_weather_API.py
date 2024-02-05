# autor: Gili
# reviewer: Itay
# testing Jenkins

from flask import Flask, request, render_template
from OpenMeteoAPI import get_lan_lon, get_openmeteo_weather

def get_weather_mood_emoji(weather_code):
    # Mapping WMO weather codes to emojis based on detailed categories
    code_to_emoji = {
        range(0, 4): "🌤️",   # Cloud development and visibility changes
        4: "🌫️",             # Smoke
        5: "🌫️",             # Haze
        6: "💨",             # Dust in suspension
        7: "🌪️",             # Dust or sand raised by wind
        8: "🌪️",             # Well developed dust/sand whirls
        9: "🌪️",             # Duststorm or sandstorm
        10: "🌫️",            # Mist
        11: "🌫️",            # Shallow fog or ice fog
        12: "🌫️",            # Continuous fog or ice fog
        13: "⚡",             # Lightning
        14: "🌧️",            # Precipitation not reaching ground
        15: "🌧️",            # Precipitation distant
        16: "🌧️",            # Precipitation nearby
        17: "⛈️",            # Thunderstorm, no precipitation
        18: "💨",            # Squalls
        19: "🌪️",            # Funnel cloud(s)
        20: "💧",            # Drizzle or snow grains
        21: "🌧️",            # Rain
        22: "❄️",            # Snow
        23: "🌨️",            # Rain and snow or ice pellets
        24: "🌧️",            # Freezing drizzle/rain
        25: "🌦️",            # Shower(s) of rain
        26: "🌨️",            # Shower(s) of snow
        27: "⛈️",            # Shower(s) of hail
        28: "🌫️",            # Fog or ice fog
        29: "⛈️",            # Thunderstorm
        range(30, 40): "🌪️", # Dust/sand storms, blowing snow
        range(40, 50): "🌫️", # Fog or ice fog
        range(50, 60): "💧",  # Drizzle
        range(60, 70): "🌧️",  # Rain
        range(70, 80): "❄️",  # Solid precipitation not in showers
        range(80, 100): "🌦️", # Showery precipitation, thunderstorms
    }

    for code_range, emoji in code_to_emoji.items():
        if isinstance(code_range, range):
            if weather_code in code_range:
                return emoji
        elif weather_code == code_range:
            return emoji

    # Default emoji if no specific weather code matches
    return "🌈"


hailyeah = Flask(__name__)


@hailyeah.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


@hailyeah.route("/city", methods=("GET", "POST"))
def get_weather():
    if request.method == "POST":
        city = request.form["city"]
        coords = get_lan_lon(city)
        data = get_openmeteo_weather(coords)
        # print(data.get("error", 0))
        if not (data.get("error", False) is True):  # if there is no error (i.e., reply 400)
            weather_code = data.get("daily").get('weather_code')  # Assuming 'weather_code' is part of the returned data
            weather_emojis = [get_weather_mood_emoji(i) for i in weather_code]

            return render_template("index.html", city=coords.get("city", "FAILED"), coords=coords, data=data, weather_emojis=weather_emojis)
        else:  # if there is an error
            return render_template("index.html")

    else:
        return render_template("index.html")


if __name__ == "__main__":
    hailyeah.run(host="0.0.0.0")

    # city = request.form["city"]
    # city = "rio de janeiro"
    # coords = get_lan_lon(city)
    # data = get_openmeteo_weather(coords)
    # weather_code = data.get("daily").get('weather_code')  # Assuming 'weather_code' is part of the returned data
    # emojs = [get_weather_mood_emoji(i) for i in weather_code]
    # print(emojs)
