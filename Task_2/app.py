from flask import Flask, jsonify, Response
import json
from weather_model import check_bad_weather
import requests

API_KEY = "vpTs47R4nUhFPiHkgDmuuSqosORifUjv"

def get_location_key(latitude, longitude):
    """Получает locationKey по координатам."""
    url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
    params = {
        "apikey": API_KEY,
        "q": f"{latitude},{longitude}"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("Key")
    else:
        raise Exception(f"Ошибка получения locationKey: {response.text}")

def get_current_weather(location_key):
    """Получает текущую погоду, включая влажность и скорость ветра."""
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
    params = {
        "apikey": API_KEY,
        "details": True
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()[0]
        precipitation = data.get("PrecipitationSummary", {}).get("Precipitation", {}).get("Metric", {}).get("Value", 0)
        return {
            "temperature": data["Temperature"]["Metric"]["Value"],
            "humidity": data["RelativeHumidity"],
            "wind_speed": data["Wind"]["Speed"]["Metric"]["Value"],
            "precipitation_probability": f"{precipitation} мм" if precipitation > 0 else "Нет осадков"
        }
    else:
        raise Exception(f"Ошибка получения данных о текущей погоде: {response.text}")

app = Flask(__name__)

@app.route('/weather/<float:latitude>/<float:longitude>', methods=['GET'])
def weather(latitude, longitude):
    """Получает прогноз и оценивает погодные условия."""
    try:
        location_key = get_location_key(latitude, longitude)
        weather_data = get_current_weather(location_key)

        # Проверяем неблагоприятные условия
        condition = check_bad_weather(
            weather_data["temperature"],
            weather_data["wind_speed"],
            weather_data["precipitation_probability"]
        )

        # Объединяем прогноз и оценку условий
        weather_data["condition"] = condition
        return Response(json.dumps(weather_data, ensure_ascii=False), content_type='application/json')
    except Exception as e:
        return Response(json.dumps({"error": str(e)}, ensure_ascii=False), content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)

