from flask import Flask, render_template, request
from flask import jsonify
import requests
app = Flask(__name__)

@app.route("/")
def hello():
    blah = {'dave':100, 'blah':200}
    return jsonify(blah)


@app.route("/city_latlon")
def get_latlon_from_city():
    city = request.args.get('city')
    return city 
    

if __name__ == "__main__":
    app.run(debug=True)
