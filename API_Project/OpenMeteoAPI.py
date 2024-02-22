# autor: Gili
# reviewer: Itay

import requests
import json
import boto3


def get_lan_lon(usr_input):
    # usr_input = "Honolulu"
    geocoding_api_url = "https://geocoding-api.open-meteo.com/v1/search"
    payload = {"name":    usr_input,
               "count":   "1",
               "language": "en",
               "format":   "json"
               }
    r = requests.get(geocoding_api_url, payload)

    # print(r.url)
    # print(r.status_code)
    # print(r.text)
    # print(type(r.text))
    lonlat_dict = json.loads(r.text)
    lat = lonlat_dict.get("results")[0].get("latitude")
    lon = lonlat_dict.get("results")[0].get("longitude")
    city = lonlat_dict.get("results")[0].get("name")
    country = lonlat_dict.get("results")[0].get("country")


    # print(f"Longitude and Latitude for {city} in {country}: ")
    # print(f"Latitude {input_lon}")
    # print(f"Latitude {input_lat}")
    ret = {"ret_status": r.status_code,
           "city": city,
           "country": country,
           "longitude": lon,
           "latitude": lat,
           }

    return ret

def get_openmeteo_weather(lon_lat_dict):
    openmeteo_api_url = "https://api.open-meteo.com/v1/forecast"
    payload = {"latitude": lon_lat_dict.get("latitude"),
              "longitude": lon_lat_dict.get("longitude"),
              "current": "temperature_2m",
              "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "relative_humidity_2m_mean"]
              # "timezone": "Africa/Cairo"
              }

    response = requests.get(openmeteo_api_url, payload)

    return response.json()# , response.status_code


# def dynamodb_push(city, data):
#     # print("yolo")
#     dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
#     table = dynamodb.Table('WeatherData')
#     response = table.put_item(Item={
#         "city" : "MORDOR",
#         "date" : "now"
#     }
#     )
#     return response


def dynamodb_push(items):
    dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

    def convert_to_dynamodb_type(value):
        if isinstance(value, list):
            return {'L': [convert_to_dynamodb_type(item) for item in value]}
        elif isinstance(value, int):
            return {'N': str(value)}
        elif isinstance(value, float):
            return {'N': str(value)}
        elif isinstance(value, bool):
            return {'BOOL': value}
        else:
            return {'S': str(value)}

    # print(items)
    for key, value in items.items():
        items[key] = convert_to_dynamodb_type(value)
    # print("_----------------___-")
    # print(items)
    response = dynamodb.put_item(
        TableName="WeatherData",
        Item=items
    )
    return response


def dynamodb_push_bkup(items):
    dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

    def convert_to_dynamodb_type(value):
            return {'S': str(value)}

    print(items)
    for key, value in items.items():
        items[key] = convert_to_dynamodb_type(value)
    # print("_----------------___-")
    print(items)
    response = dynamodb.put_item(
        TableName="WeatherData",
        Item=items
    )
    return response
# dd = get_lan_lon("Tokyo")
# print(dd)
# rr = get_openmeteo_weather(dd)
# print(rr)
# print("---------")
# print(rr["daily"]["time"])
# print(sc)