def check_bad_weather(temperature, wind_speed, precipitation_probability):
    """
    Оценивает погодные условия как хорошие или плохие.

    Параметры:
    - temperature (float): Температура в °C.
    - wind_speed (float): Скорость ветра в км/ч.
    - precipitation_probability (float): Вероятность осадков в процентах.

    Возвращает:
    - str: "Плохие условия" или "Хорошие условия".
    """
    if temperature < 0 or temperature > 35:
        return "Плохие условия"
    if wind_speed > 50:
        return "Плохие условия"
    if precipitation_probability > 70:
        return "Плохие условия"
    return "Хорошие условия"
