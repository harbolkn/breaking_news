from flask import Flask, render_template, request
from flask import jsonify
import requests, json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/city_latlon")
def get_latlon_from_city():
    try:
        city = request.args.get('city')
        req = requests.get('http://nominatim.openstreetmap.org?format=json&city='+city)
        j = json.loads(req.text)
        latlon = [j[0]['lat'], j[0]['lon']]
        return city + "," + j[0]['lat'] + "," + j[0]['lon']
    except Exception:
        return ","

if __name__ == "__main__":
    app.run()
