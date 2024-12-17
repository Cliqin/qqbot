import os
import requests
import json
from plugins.base import Base
class Plugin(Base):
    """天气预测"""
    def __init__(self):
        super().__init__()
        self.is_at = True
        self.url = 'http://t.weather.sojson.com/api/weather/city/'
        self.city_codes = self.load_city_codes()

    def load_city_codes(self):
        fdir = os.path.dirname(os.path.abspath(__file__))
        fpath = os.path.join(fdir, 'city.json')
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"An error occurred while loading city codes: {e}")
            return {}

    def is_match(self, message):
        """检测是否匹配此插件"""
        return message[:4] == r'天气预报'

    async def handle(self, message):
        city = message[4:].strip()
        print(city)
        return self.weather(city)

    def weather(self, city):
        city_code = self.city_codes.get(city)
        if city_code is None:
            return f"未找到该城市的代码，请确认城市名称是否正确。"

        response = requests.get(self.url + city_code)
        d = response.json()

        if d['status'] == 200:
            weather_data = d['data']
            d = response.json()
            return self.princess_speak("西娅", weather_data,d)
        else:
            return "获取天气信息失败。"

    def princess_speak(self, princess_name, weather_info,d):
        city_name = d['cityInfo']['city']
        current_shidu = weather_info['shidu']
        current_pm25 = weather_info['pm25']
        current_pm10 = weather_info['pm10']
        current_quality = weather_info['quality']
        current_wendu = weather_info['wendu']
        current_ganmao = weather_info['ganmao']

        weather_message = f"亲爱的臣民们，这是来自{princess_name}公主的天气通告：\n"
        weather_message += f"今天，我们美丽的城市{city_name}的天气情况如下——\n"
        weather_message += f"湿度为{current_shidu}，PM2.5指数为{current_pm25}，PM10指数为{current_pm10}。\n"
        weather_message += f"空气质量为{current_quality}，当前气温为{current_wendu}摄氏度。\n"
        weather_message += f"公主提醒您：{current_ganmao}。\n"

        # 未来几天的天气预报
        weather_message += "\n接下来，是未来2日的天气预报：\n"
        for day in weather_info['forecast'][:2]:  # 只展示未来三天的天气
            weather_message += f"在{day['ymd']},{day['week']}，我们将会看到{day['type']}。\n"
            weather_message += f"最高气温将达到{day['high']}，而最低气温则会降至{day['low']}。\n"
            weather_message += f"风向为{day['fx']}，风力{day['fl']}。\n"
            weather_message += f"公主的温馨提示：{day['notice']}。\n"

        return weather_message