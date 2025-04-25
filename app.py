from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('weather.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    api_key = "f6704ba628b0c2635ecb657b3662f990"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    clouds = data['clouds']['all']
    rain = data.get('rain', {}).get('1h', 0)
    snow = data.get('snow', {}).get('1h', 0)
    if rain > 0:
        sademed = f"Vihma {rain} mm"
    elif snow > 0:
        sademed = f"Lund {snow} mm"
    else:
        sademed = "Sademed puuduvad"
    return render_template(
        'weather.html',
        temp=temperature,
        city=city,
        humidity=humidity,
        wind=wind_speed,
        clouds=clouds,
        sademed=sademed
    )
if __name__ == '__main__':
    app.run(debug=True)