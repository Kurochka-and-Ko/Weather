import unittest
from weather_model import check_bad_weather

class TestWeatherModel(unittest.TestCase):
    def test_good_weather(self):
        self.assertEqual(check_bad_weather(20, 10, 30), "Хорошие условия")

    def test_low_temperature(self):
        self.assertEqual(check_bad_weather(-5, 10, 30), "Плохие условия")

    def test_high_temperature(self):
        self.assertEqual(check_bad_weather(40, 10, 30), "Плохие условия")

    def test_high_wind_speed(self):
        self.assertEqual(check_bad_weather(20, 60, 30), "Плохие условия")

    def test_high_precipitation_probability(self):
        self.assertEqual(check_bad_weather(20, 10, 80), "Плохие условия")

if __name__ == "__main__":
    unittest.main()
