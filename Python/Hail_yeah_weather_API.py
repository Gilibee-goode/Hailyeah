# autor: Gili
# reviewer: Itay

from flask import (Flask, request, render_template, Response,
                   stream_with_context, send_from_directory)
from OpenMeteoAPI import (get_lan_lon, get_openmeteo_weather,
                          dynamodb_push, dynamodb_push_bkup, get_weather_mood_emoji,
                          save_query_result)
# from prometheus_flask_exporter import PrometheusMetrics
import requests
# import logging
import os


# from prometheus_client import start_http_server, Counter, Histogram, Summary
# from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
# from flask import jsonify, redirect, url_for
# import json


hailyeah = Flask(__name__)

# ----- Setting up metrics for Prometheus ------
# metrics = PrometheusMetrics(hailyeah)
# metrics = GunicornPrometheusMetrics(hailyeah)

# metrics.info('app_info', 'Hailyeah web app metrics')  # static metric

city = None
# city_query_counter = metrics.counter(
#     'city_queries', 'Number of queries by city', labels={'city': lambda: city})


# ----- Setting up logging ------
# logging.basicConfig(level=logging.INFO, filename='./logs/weather_app.log', filemode='a',
#                     format='%(asctime)s - %(levelname)s - %(message)s')


# ------ read env vars ------
bg_color_code = os.getenv('BG_COLOR', '#d10011')  # Defaulting to a red color if BG_COLOR isn't set
print(bg_color_code)


# ----- Pages ------
@hailyeah.route('/hailyeah/', methods=["GET", "POST"])
def index():
    return render_template('index.html', bg_color_code=bg_color_code)


@hailyeah.route("/hailyeah/city", methods=("GET", "POST"))
def get_weather():
    if request.method == "POST":
        global city  # to allow the @city_query_counter to register it as a metric
        city = request.form["city"]

        # Log the attempt to query weather for a city
        # logging.info(f"Received POST request to query weather for city: {city}")

        try:  # No city match returns to homepage
            coords = get_lan_lon(city)
            # Log successful retrieval of coordinates
            # logging.info(f"Successfully retrieved coordinates for city: {city} -> {coords}")

        except Exception as e:
            # Log the exception when city coordinates cannot be fetched
            # logging.error(f"Failed to retrieve coordinates for city: {city}. Error: {e}", exc_info=True)
            return render_template("index.html", bg_color_code=bg_color_code)

        data = get_openmeteo_weather(coords)
        if not (data.get("error", False) is True):  # if there is no error (i.e., reply 400)
            weather_code = data.get("daily").get('weather_code')  # Assuming 'weather_code' is
            # part of the returned data
            weather_emojis = [get_weather_mood_emoji(i) for i in weather_code]
            city = coords.get("city", "FAILED")

            # Log the successful retrieval of weather data
            # logging.info(f"Successfully retrieved weather data for city: {city}")

            # Update the search history
            save_query_result(city, data)

            # @city_query_counter
            #     def return_render():
            return render_template("index.html", city=city, coords=coords, data=data,
                                       weather_emojis=weather_emojis, bg_color_code=bg_color_code)
            # return return_render()

        else:  # if there is a problem which did not result in data.get("error") == True

            # Log the occurrence of an error in fetching weather data
            # logging.warning(f"Unknown error fetching weather data for city: {city}. Data: {data}")
            return render_template("index.html", bg_color_code=bg_color_code)

    else:
        # Log the receipt of a GET request to the city endpoint
        # logging.info("Received GET request to '/city' endpoint - returned to '/'.")
        return render_template("index.html", bg_color_code=bg_color_code)



@hailyeah.route('/hailyeah/search-history')
def history():
    directory = './search_history'
    files = os.listdir(directory)
    files = [f for f in files if f.endswith('.json')]  # Filter to only include .json files
    # Generate URLs for downloading each file
    files_urls = {f: f'/download/{f}' for f in files}
    return render_template('history.html', files=files_urls)


@hailyeah.route('/hailyeah/download/<filename>')
def download_file(filename):
    directory = os.path.join(os.getcwd(), 'search_history')  # Ensure this matches your directory structure
    try:
        return send_from_directory(directory, filename, as_attachment=True, download_name=filename)
    except Exception as e:
        return str(e)


@hailyeah.route('/hailyeah/download-image')
def download_image():
    image_url = 'https://kick-da-bucket.s3.eu-north-1.amazonaws.com/lovely_sky_view.jpg'

    req = requests.get(image_url, stream=True)

    def generate():
        for chunk in req.iter_content(chunk_size=1024):
            yield chunk

    return Response(stream_with_context(generate()),
                    content_type=req.headers['Content-Type'],
                    headers={"Content-Disposition": "attachment; filename=lovely_sky_view.jpg"}
                    )


@hailyeah.route('/hailyeah/save-data', methods=['POST'])
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
        "city": city,
        "date": date,
        "weather_emojis": weather_emojis,
        "DailyTempMax": DailyTempMax,
        "DailyTempMin": DailyTempMin,
        "DailyHumidity": DailyHumidity
    }

    # print(items)
    dynamodb_push(items)
    return render_template("index.html", bg_color_code=bg_color_code)
    # return redirect(url_for('index'))  # Redirect back to the main page


@hailyeah.route('/hailyeah/bkup_db', methods=("GET", "POST"))
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
    return render_template("index.html", bg_color_code=bg_color_code)
    # return redirect(url_for('index'))  # Redirect back to the main page


if __name__ == "__main__":
    # start_http_server(8001)  # Start Prometheus metrics server on port 8001
    hailyeah.run(host="0.0.0.0")

    # # ----- Setting up logging ------
    # logging.basicConfig(level=logging.INFO, filename='weather_app.log', filemode='a',
    #                     format='%(asctime)s - %(levelname)s - %(message)s')

    # city = request.form["city"]
    # city = "rio de janeiro"
    # coords = get_lan_lon(city)
    # data = get_openmeteo_weather(coords)
    # weather_code = data.get("daily").get('weather_code')  # Assuming 'weather_code' is part of the returned data
    # emojs = [get_weather_mood_emoji(i) for i in weather_code]
    # print(emojs)
