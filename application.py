import boto3
import requests
from flask import Flask, render_template, request, send_file

application = Flask(__name__, template_folder='templates')
url = "https://s3.eu-central-1.amazonaws.com/odedrub.weather/sky-purple-sky.gif"
BUCKET_NAME = 'odedrub.weather'
KEY = 'sky-purple-sky.gif'

s3 = boto3.client('s3')  # use client to get item from s3
location = ''
data = {}


@application.route('/', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        try:
            city = request.form['City']
            # print(city)
            app_id = "8afde337"
            app_key = "54cfb1cc2d416faa9ba79e54a60818e4"
            geo_key = "93c8227801e25c807c9e5c3e839b0273"
            geo_json = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={geo_key}")
            # print(geo_json.json())
            geo_country = geo_json.json()[0]['country']
            # geo_state = geo_json.json()[0]['state']  # add country state to print
            # full_city = [city, geo_country, geo_state]
            full_city = [city, geo_country]
            geo_lon = geo_json.json()[0]['lon']
            geo_lat = geo_json.json()[0]['lat']
            # geo_stat = [geo_lon, geo_lat]
            # print(f"\t\tCity name: {city}\nLongitude/Altitude coordinates: {geo_stat}")
            weather_json = requests.get(f"http://api.weatherunlocked.com/api/forecast/{geo_lat},{geo_lon}?app_id={app_id}&app_key={app_key}")
            weather_stat = weather_json.json()
            # print(weather_stat) # prints all database
            dicta = weather_stat['Days']
            # print(f"Weather in {city}:\n")

            dictb = {}

            for i in range(0, 7):
                dictb[dicta[i].get('date')] = [{'min_temp': dicta[i].get('temp_min_c'),
                                               'max_temp': dicta[i].get('temp_max_c'),
                                                'min_humidity': dicta[i].get('humid_min_pct'),
                                                'max_humidity': dicta[i].get('humid_max_pct')}]

            # dictb = weather(dicta)
            # name = backup(dictb)
            global data
            data = dictb
            global location
            location = city

            return render_template('index.html', dictb=dictb, full_city=full_city), location, data
            # return render_template('index.html', form_data=city)
        except Exception:
            print("Invalid input.")
            return render_template('error.html')
    if request.method == 'GET':
        # print("Enter input.")
        return render_template('index.html')


@application.route('/download', methods=['GET'])
def download():
    path = 'sky-purple-sky.gif'
    s3.download_file(BUCKET_NAME, KEY, path)
    return send_file(path, as_attachment=True)
    # return render_template('index_downloaded.html')


@application.route('/backup', methods=['GET'])
def backup():
    dynamodb = boto3.resource('dynamodb')  # use resource to put item in dynamodb
    table = dynamodb.Table('weather')
    item = {
            'City': f'{location}',
            'Weather': f'{data}'
    }
    #item = {'city': f'{location}', 'Date': f'{data}', 'Min temp': '-2', 'Max temp': '6', 'Min humidity': '75', 'Max humidity': '92'}

    table.put_item(Item=item)
    return render_template('backup.html')


if __name__ == '__main__':
    application.run(host='localhost', port=5000, debug=True)
