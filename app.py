from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__, template_folder='templates')

API_KEY = 'f6bf196015464b5fb8273e5522911cfc'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'

def get_weather(city):
    complete_url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
    response = requests.get(complete_url)
    return response.json()

def crop_recommendation(temperature, humidity):
    if temperature > 30:
        return "It's too hot, consider planting heat-resistant crops like millet or sorghum."
    elif 20 < temperature <= 30:
        if humidity < 50:
            return "Good conditions for wheat, maize, and soybean."
        else:
            return "Suitable for rice, sugarcane, and cotton."
    elif 10 < temperature <= 20:
        return "Ideal for cool-weather crops like potatoes, carrots, and lettuce."
    else:
        return "Consider cold-tolerant crops like barley and rye."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
        if weather_data['cod'] != 200:
            return render_template('index.html', error=weather_data.get('message', 'Unknown error'))
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        recommendation = crop_recommendation(temperature, humidity)
        return render_template('ind.html', city=city, temperature=temperature, humidity=humidity, recommendation=recommendation)
    return render_template('ind.html')

if __name__ == '__main__':
    app.run(debug=True)
