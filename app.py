from flask import Flask, render_template
from flask import jsonify
app = Flask(__name__)

@app.route("/data")
def data():
    blah = {'dave':100, 'blah':200}
    return jsonify(blah)

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
