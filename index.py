from flask import Flask, request, jsonify, render_template
import requests
app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')
@app.route('/about.html')
def about():
    return render_template('about.html')
@app.route('/services.html')
def service():
    return render_template('services.html')

@app.route('/children.html')
def childeren():
    return render_template('children.html')
@app.route('/festival.html')
def festival():
    return render_template('festival.html')
@app.route('/hospital.html')
def hospital():
    return render_template('hospital.html')


if __name__ == '__main__':
    app.run()
