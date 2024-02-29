# autor: Gili
# reviewer: Itay
# testing Jenkins3

from flask import Flask, request, render_template, Response, stream_with_context, jsonify, redirect, url_for
from OpenMeteoAPI import get_lan_lon, get_openmeteo_weather, dynamodb_push, dynamodb_push_bkup
# from prometheus_client import start_http_server, Counter, Histogram, Summary
from prometheus_flask_exporter import PrometheusMetrics
# from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
import requests
import json


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
metrics = PrometheusMetrics(hailyeah)
# metrics = GunicornPrometheusMetrics(hailyeah)

metrics.info('app_info', 'Hailyeah web app metrics')  # static metric

city = None
city_query_counter = metrics.counter(
    'city_queries', 'Number of queries by city', labels={'city': lambda: city})


@hailyeah.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


@hailyeah.route("/city", methods=("GET", "POST"))
def get_weather():
    if request.method == "POST":
        global city
        city = request.form["city"]

        try:  # No city match returns to homepage
            coords = get_lan_lon(city)
        except Exception as e:
            return render_template("index.html")

        data = get_openmeteo_weather(coords)
        # print(data.get("error", 0))
        if not (data.get("error", False) is True):  # if there is no error (i.e., reply 400)
            weather_code = data.get("daily").get('weather_code')  # Assuming 'weather_code' is part of the returned data
            weather_emojis = [get_weather_mood_emoji(i) for i in weather_code]
            city = coords.get("city", "FAILED")
            @city_query_counter
            def return_render():
                return render_template("index.html", city=city, coords=coords, data=data, weather_emojis=weather_emojis)
            return return_render()

        else:  # if there is an error
            return render_template("index.html")

    else:
        return render_template("index.html")


@hailyeah.route('/download-image')
def download_image():
    image_url = 'https://kick-da-bucket.s3.eu-north-1.amazonaws.com/lovely_sky_view.jpg'

    req = requests.get(image_url, stream=True)

    def generate():
        for chunk in req.iter_content(chunk_size=1024):
            yield chunk

    return Response(stream_with_context(generate()),
                    content_type=req.headers['Content-Type'],
                    headers={"Content-Disposition":
                                 "attachment; filename=lovely_sky_view.jpg"})




@hailyeah.route('/save-data', methods=['POST'])
def save_data():
    city = request.form.get('city')
    date = request.form.get('date')
    weather_emojis = request.form.get('weather_emojis')
    DailyTempMax = request.form.get('DailyTempMax')
    DailyTempMin = request.form.get('DailyTempMin')
    DailyHumidity = request.form.get('DailyHumidity')

    # print("in save data")
    # print(date)

    items = {
        "city":city,
        "date":date,
        "weather_emojis": weather_emojis,
        "DailyTempMax": DailyTempMax,
        "DailyTempMin": DailyTempMin,
        "DailyHumidity": DailyHumidity
    }

    # print(items)
    dynamodb_push(items)
    return render_template("index.html")
    # return redirect(url_for('index'))  # Redirect back to the main page



@hailyeah.route('/bkup_db', methods=("GET", "POST"))
def bkup_db():
    city = "Tel Aviv"
    coords = get_lan_lon(city)
    data = get_openmeteo_weather(coords)

    if not (data.get("error", False) is True):  # if there is no error (i.e., reply 400)
        weather_code = data.get("daily").get('weather_code')  # Assuming 'weather_code' is part of the returned data
        weather_emojis = [get_weather_mood_emoji(i) for i in weather_code]


    city = "Tel Aviv"
    date = data["daily"]["time"]
    weather_emojis = weather_emojis
    DailyTempMax = data["daily"]["temperature_2m_max"]
    DailyTempMin = data["daily"]["temperature_2m_min"]
    DailyHumidity = data["daily"]["relative_humidity_2m_mean"]

    # print("in bkup db")
    # print(date)


    items = {
        "city": city,
        "date": date,
        "weather_emojis": weather_emojis,
        "DailyTempMax": DailyTempMax,
        "DailyTempMin": DailyTempMin,
        "DailyHumidity": DailyHumidity
    }

    # print(items)

    dynamodb_push_bkup(items)
    return render_template("index.html")
    # return redirect(url_for('index'))  # Redirect back to the main page



if __name__ == "__main__":
    # start_http_server(8001)  # Start Prometheus metrics server on port 8001
    hailyeah.run(host="0.0.0.0")

    # city = request.form["city"]
    # city = "rio de janeiro"
    # coords = get_lan_lon(city)
    # data = get_openmeteo_weather(coords)
    # weather_code = data.get("daily").get('weather_code')  # Assuming 'weather_code' is part of the returned data
    # emojs = [get_weather_mood_emoji(i) for i in weather_code]
    # print(emojs)
