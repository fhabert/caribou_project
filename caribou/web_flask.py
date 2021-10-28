from flask import Flask, redirect, url_for, render_template, request, session, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "DeErs"
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/individuals', methods=['GET', 'POST'])
def individuals():
    return render_template('my_map.html')

@app.route('/interval', methods=['GET', 'POST'])
def interval():
    return render_template('map_interval.html')

if __name__ == '__main__':
    app.run(debug=True)

