from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('weather.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = requests.form['city']
    api_key = "f6704ba628b0c2635ecb657b3662f990"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']
    return render_template('weather.html', temp=temperature, city=city)
if __name__ == '__main__':
    app.run(debug=True)