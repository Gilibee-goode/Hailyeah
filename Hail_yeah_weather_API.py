# autor: Gili
# reviewer: Itay

from flask import Flask, request, render_template
from OpenMeteoAPI import get_lan_lon, get_openmeteo_weather


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
            return render_template("index.html", city=coords.get("city", "FAILED"), coords=coords, data=data)
        else:  # if there is an error
            return render_template("index.html")

    else:
        return render_template("index.html")


if __name__ == "__main__":
    hailyeah.run(host="0.0.0.0")
