from flask import Flask, render_template, request
from flask import jsonify
import simplejson as json
import datetime
import requests 
import csv
import settings
app = Flask(__name__)

access_token = settings.access_token
api_base="https://api-ssl.bitly.com"
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/data")
def data():
    endpoint = api_base+"/v3/search" 
    top = {"data": []}

    with open('cities/cities.csv', 'r') as city_file:
        reader = csv.reader(city_file, delimiter=",")
        for line in reader:
            query_params = {'access_token': access_token, 'limit': 1, 'cities': line[1], 'fields': 'title,url'}
            response = requests.get(endpoint, params= query_params)
            data = json.loads(response.content)['data']
            if 'results' in data and len(data['results']) > 0:
                results = data['results'][0]
                top["data"].append({"title": results['title'], "link": results['url'], "name": line[0], "coordinates": _get_latlon_from_city(line[0])})

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
    return [j[0]['lon'], j[0]['lat']]

@app.route("/do_everything")
def do_everything():
    phrases = get_phrases()
    story_ids = story_from_phrases(phrases)
    story_cities = get_distribution(story_ids)
    for i in range(0,len(story_ids)):
        print json.dumps({'story_id':story_ids[i], 'story_cities':story_cities[i]})

    return #json.dumps(story_ids)  

def get_phrases():
    response = requests.get('https://api-ssl.bitly.com/v3/realtime/hot_phrases?access_token=' + access_token)
    data = json.loads(response.content)
    phrases = map(lambda(a): a["phrase"],data['data']["phrases"])
    return phrases

def story_from_phrases(phrases):
    endpoint = api_base+"/v3/story_api/story_from_phrases"
    stories_links = []
    for phrase in phrases:
        response = requests.get(endpoint, params={'access_token': access_token, 'phrases': phrase})
#        print response.text
        response_data = json.loads(response.text)
        stories_links.append({'story_id':response_data['data']['story_id'], 'link':response_data['data']['aggregate_link'][0]})
    return stories_links

def get_distribution(story_ids):
    endpoint = api_base+"/v3/story_api/distribution"
    cities_data = []
    for s_id in story_ids:
        response = requests.get(endpoint, params={'access_token': access_token, 'story_id': s_id['story_id'], 'field':'cities'})
        response_data = json.loads(response.text)
        if response_data['data'] is not None and response_data['data']['cities'] is not None:
            cities_data.append(response_data['data']['cities'])
        else:
            cities_data.append(None)
    return cities_data

if __name__ == "__main__":
    app.run(debug=True)
