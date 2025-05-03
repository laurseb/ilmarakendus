from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_google_image(city):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    query = city.replace(" ", "+")
    url = f"https://www.google.com/search?tbm=isch&q={query}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        if len(images) > 1:
            return images[1]['src']
    return None

@app.route('/', methods=['GET'])
def index():
    return render_template('weather.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    api_key = "f6704ba628b0c2635ecb657b3662f990"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200 or "main" not in data:
            raise ValueError("Linna ei leitud")

        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        clouds = data['clouds']['all']
        rain_1h = data.get('rain', {}).get('1h')
        rain_3h = data.get('rain', {}).get('3h')
        snow_1h = data.get('snow', {}).get('1h')
        snow_3h = data.get('snow', {}).get('3h')
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        image_url = get_google_image(city)

        if rain_1h:
            sademed = f"Vihma {rain_1h} mm viimase 1h jooksul"
        elif rain_3h:
            sademed = f"Vihma {rain_3h} mm viimase 3h jooksul"
        elif snow_1h:
            sademed = f"Lund {snow_1h} mm viimase 1h jooksul"
        elif snow_3h:
            sademed = f"Lund {snow_3h} mm viimase 3h jooksul"
        else:
            sademed = "Sademed puuduvad"

        description = data['weather'][0]['description']

        return render_template(
            'weather.html',
            temp=temperature,
            city=city,
            humidity=humidity,
            wind=wind_speed,
            clouds=clouds,
            sademed=sademed,
            data=data,
            description=description,
            lat=lat,
            lon=lon,
            image_url=image_url
        )
    except Exception as e:
        return render_template('weather.html', error="Antud linna ei leitud, proovige uuesti")

if __name__ == '__main__':
    app.run(debug=True)
