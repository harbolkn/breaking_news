from flask import Flask, render_template
from flask import jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    blah = {'dave':100, 'blah':200}
    return jsonify(blah)

if __name__ == "__main__":
    app.run()
