from flask import Flask, render_template, request
import requests
from weather_model import check_bad_weather

API_KEY = "vpTs47R4nUhFPiHkgDmuuSqosORifUjv"

app = Flask(__name__)

def get_weather_data(city):
    """Получает данные о погоде для заданного города."""
    try:
        # Получение координат города
        location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
        location_params = {"apikey": API_KEY, "q": city}
        location_response = requests.get(location_url, params=location_params, timeout=10)

        if location_response.status_code != 200:
            raise Exception("Ошибка подключения к API")

        location_data = location_response.json()
        if not location_data:
            raise ValueError(f"Город '{city}' не найден")

        location_key = location_data[0]["Key"]

        # Получение погодных данных
        weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
        weather_params = {"apikey": API_KEY, "details": True}
        weather_response = requests.get(weather_url, params=weather_params, timeout=10)

        if weather_response.status_code != 200:
            raise Exception("Ошибка подключения к API")

        weather_data = weather_response.json()
        if not weather_data:
            raise ValueError("Ошибка получения погодных данных")

        return {
            "temperature": weather_data[0]["Temperature"]["Metric"]["Value"],
            "wind_speed": weather_data[0]["Wind"]["Speed"]["Metric"]["Value"],
            "precipitation_probability": weather_data[0].get("PrecipitationSummary", {}).get("Precipitation", {}).get("Metric", {}).get("Value", 0)
        }
    except ValueError as ve:
        return {"error": str(ve)}
    except requests.exceptions.Timeout:
        return {"error": "Превышено время ожидания API"}
    except requests.exceptions.RequestException as re:
        return {"error": "Ошибка сети или подключения"}
    except Exception as e:
        return {"error": f"Неизвестная ошибка: {str(e)}"}



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получение данных из формы
        start_city = request.form.get('start_city')
        end_city = request.form.get('end_city')

        # Проверка пустых полей
        if not start_city or not end_city:
            return render_template('index.html', error="Пожалуйста, заполните оба поля!")

        # Получение данных о погоде
        start_weather = get_weather_data(start_city)
        end_weather = get_weather_data(end_city)

        # Проверка на ошибки
        if "error" in start_weather:
            return render_template('index.html', error=f"Ошибка для города '{start_city}': {start_weather['error']}")
        if "error" in end_weather:
            return render_template('index.html', error=f"Ошибка для города '{end_city}': {end_weather['error']}")

        # Проверка неблагоприятных условий
        start_condition = check_bad_weather(
            start_weather["temperature"],
            start_weather["wind_speed"],
            start_weather["precipitation_probability"]
        )
        end_condition = check_bad_weather(
            end_weather["temperature"],
            end_weather["wind_speed"],
            end_weather["precipitation_probability"]
        )

        return render_template('result.html',
                               start_city=start_city,
                               end_city=end_city,
                               start_weather=start_weather,
                               end_weather=end_weather,
                               start_condition=start_condition,
                               end_condition=end_condition)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
