import requests

# 和风天气API配置信息
api_key = "248bc367bd1b477ea7359d28b956b49d"  # 在和风天气官网注册后获取
cities = ["Beijing", "Shanghai", "Guangzhou", "Anji"]  # 需要获取天气信息的城市名称列表

# 获取城市的Location ID
def get_location_id(city_name, api_key):
    url = f"https://geoapi.qweather.com/v2/city/lookup?location={city_name}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == '200' and data['location']:
            return data['location'][0]['id']
    return None

# 获取天气信息
def get_weather(location_id, api_key):
    url = f"https://devapi.qweather.com/v7/weather/now?location={location_id}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        weather_info = weather_data['now']
        return f"天气: {weather_info['text']}，温度: {weather_info['temp']}°C"
    return "无法获取天气信息"

# 获取所有城市的天气信息
def get_all_weather():
    weather_reports = []
    for city in cities:
        location_id = get_location_id(city, api_key)
        if location_id:
            weather = get_weather(location_id, api_key)
            weather_reports.append(f"{city}: {weather}")
        else:
            weather_reports.append(f"{city}: 无法获取天气信息")
    return "\n".join(weather_reports)
