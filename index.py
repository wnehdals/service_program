from flask import Flask, request, jsonify, render_template
import hospital_demo
import requests
import json
import re
import festivalInfo
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
@app.errorhandler(404)
def not_found(error):

    return render_template('404.html')
@app.route('/festival')
@app.route('/festival/<pageNum>', methods=['GET'])
def getFestival(pageNum=1):
    return festivalInfo.getFestival(pageNum)

@app.route('/festival.html/<pageNum>')
@app.route('/festival.html', methods=['GET'])
def festival(pageNum=1):
    return festivalInfo.festival()


@app.route('/hospital/request/<longitude>/<latitude>', methods=['GET'])
def hospital_request(longitude, latitude):
    return hospital_demo.response_hospital_info(longitude, latitude)


@app.route('/hospital')
def hospital():
    # return render_template('hospital.html')
    return hospital_demo.demo()


if __name__ == '__main__':
    app.run()
