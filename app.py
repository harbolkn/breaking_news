from flask import Flask, render_template, request
from flask import jsonify
import simplejson as json
import datetime
import requests 
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/data")
def data():
    access_token = "bafda5b39a752043052cbec72ae9908e5e15c9d4"
    endpoint = "https://api-ssl.bitly.com/v3/search"

	cities = [ line.split(', ')[1] for line in open('./cities.csv') ]
	top = {}
	for city in cities:
		query_params = {'access_token': access_token,
		'limit': 1,
		'cities': city,
		'fields': 'title,url'}

		response = requests.get(endpoint, params= query_params)
		data = json.loads(response.contents)
		top[city] = [data['url'], data['title']]

	return jsonify(top)

@app.route("/city_latlon")
def get_latlon_from_city():
    try:
        city = request.args.get('city')
        lat, lon = _get_latlon_from_city(city)
        return city + "," + lat + "," + lon
    except Exception:
        return ","

def _get_latlon_from_city(city):
        req = requests.get('http://nominatim.openstreetmap.org?format=json&limit=1&city='+city)
        j = json.loads(req.text)
        return j[0]['lat'], j[0]['lon']

if __name__ == "__main__":
    app.run()
