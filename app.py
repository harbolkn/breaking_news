from flask import Flask, render_template, request
from flask import jsonify
import simplejson as json
import datetime
import requests 
app = Flask(__name__)

access_token = "bafda5b39a752043052cbec72ae9908e5e15c9d4"
api_base="https://api-ssl.bitly.com"
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/data")
def data():
    endpoint = api_base+"/v3/search"

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

def story_from_phrases(phrases):
    endpoint = api_base+"/v3/story_api/story_from_phrases"
    story_ids = []
    for phrase in phrases:
        response = requests.get(endpoint, params={'access_token': access_token, 'phrases': phrase})
        response_data = json.loads(response)
        story_id = response_data['data']['story_id']

        

if __name__ == "__main__":
    app.run()
