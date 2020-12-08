from flask import Flask, request, jsonify, render_template
import hospital
import requests
import json
import re
import festivalInfo
import kinderInfo

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


@app.route('/children/<city>', methods=['GET'])
def get_children(city):
    if int(city) > 0 or int(city) < 32:
        return kinderInfo.getChildren(city)
    return kinderInfo.getErrorChildren()


@app.route('/children/<city>/<page>', methods=['GET'])
def get_children_page(city, page):
    return kinderInfo.getChildrenPage(city, page)


@app.route('/children_doc.html')
def children_doc():
    return render_template('children_doc.html')


@app.route('/children.html/<city>')
@app.route('/children.html', methods=['GET'])
def children():
    return kinderInfo.info()


@app.route('/children')
def get_kinder():
    return kinderInfo.getErrorChildren()


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


@app.route('/festival')
def getFestival():
    return festivalInfo.getErrorFestival()


@app.route('/festival/<city>', methods=['GET'])
def getCityFestival(city):
    if ((int(city) <= 0 or int(city) >= 32)):
        return festivalInfo.getErrorFestival()
    else:
        return festivalInfo.getFestival(city)


@app.route('/festival.html/<city>')
@app.route('/festival.html', methods=['GET'])
def festival(pageNum=1):
    return festivalInfo.festival()


@app.route('/hospital/request/lonlat/<longitude>/<latitude>', methods=['GET'])
def hospital_request_lonlat(longitude, latitude):
    return hospital.response_hospital_info_lonlat(longitude, latitude)


@app.route('/hospital/request/address/<major>')
def hospital_request_address_majoronly(major):
    return hospital.response_hospital_info_address(major)


@app.route('/hospital/request/address/<major>/<minor>', methods=['GET'])
def hospital_request_address(major, minor):
    return hospital.response_hospital_info_address(major, minor)


@app.route('/hospital/demo')
def hospital_demo():
    return hospital.demo()


@app.route('/hospital/doc')
def hospital_doc():
    return hospital.doc()


if __name__ == '__main__':
    app.run()
