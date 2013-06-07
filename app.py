from flask import Flask, render_template, request
from flask import jsonify
import requests
import simplejson as json
import datetime
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/city_latlon")
def get_latlon_from_city():
    access_token = "bafda5b39a752043052cbec72ae9908e5e15c9d4"
    endpoint = "https://api-ssl.bitly.com/v3/search"

    city_list = ['us-il-chicago']
    for city in city_list:
        query_params = { 'access_token': access_token
        , 'limit': 50
        , 'city': city
        , 'fields': 'score,title,url'
        }
	response = requests.get(endpoint, params= query_params)
	data = json.loads(response.content)

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
