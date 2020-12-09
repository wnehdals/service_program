from flask import Flask, request, jsonify, render_template
import hospital, festivalInfo, kinderInfo
import requests, json, re
from CityCode import CityCode
from Response import Response

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


@app.route('/children/<cityCode>')
@app.route('/children/<cityCode>/<pageNum>', methods=['GET'])
def getChildren(cityCode, pageNum=1):
    return kinderInfo.getChildren(cityCode, pageNum)

@app.route('/children_doc.html')
def children_doc():
    return render_template('children_doc.html')

@app.route('/children.html/<cityCode>/<pageNum>')

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


@app.route('/hospital/request/address/<major>/<minor>', methods=['GET'])
def hospital_request_address(major, minor):
    return hospital.response_hospital_info_address(major, minor)


@app.route('/hospital/request/all/address/<major>/<minor>/', defaults={'item_count': 10}, methods=['GET'])
@app.route('/hospital/request/all/address/<major>/<minor>/<item_count>/', methods=['GET'])
def hospital_request_all_address_limit(major, minor, item_count):
    city_code = CityCode()
    if minor.isdigit():
        minor = city_code.get_name(minor)
        if minor == "-":
            response = Response(39)
            return json.dumps(response.getResponse(), ensure_ascii=False, indent=4)
    return hospital.response_all_hospital_info_address(major, minor, item_count)


@app.route('/hospital/<code>/', methods=['GET'])
def hospital_request_simple(code):
    city_code = CityCode()
    if code.isdigit():
        city_name = city_code.get_name(code)
        if city_name != "-":
            return hospital.response_all_hospital_info_address("경기도", city_name, 10)
    
    response = Response(39)
    return json.dumps(response.getResponse(), ensure_ascii=False, indent=4)


@app.route('/hospital/demo')
def hospital_demo():
    return hospital.demo()


@app.route('/hospital/doc')
def hospital_doc():
    return hospital.doc()


if __name__ == '__main__':
    app.run()
