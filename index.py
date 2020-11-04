from flask import Flask, request, jsonify, render_template
import requests
import json
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
    host = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList'
    params = {'ServiceKey': 'mjcDOZkT0XqWULC1L3PAFfxCere4Wq1oXpTJv6jmdF5RmBMPaN6A6Ju112m74zBmsXVsYDW7YJOCH40Q4nmDwg==',
              'contentTypeId': '15',
              'areaCode': '31',
              'listYN': 'Y',
              'MobileOS': 'ETC',
              'MobileApp': 'TourAPI3.0_Guide',
              'arrange': 'A',
              'numOfRows': '12',
              'pageNo': '1',
              '_type': 'json'}
    url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey=mjcDOZkT0XqWULC1L3PAFfxCere4Wq1oXpTJv6jmdF5RmBMPaN6A6Ju112m74zBmsXVsYDW7YJOCH40Q4nmDwg==&contentTypeId=15&areaCode=31&sigunguCode=&cat1=&cat2=&cat3=&listYN=Y&MobileOS=ETC&MobileApp=TourAPI3.0_Guide&arrange=A&numOfRows=12&pageNo=1&_type=json'
    res = requests.get(host,params=params).json()
    response = res['response']
    body = response['body']
    items = body['items']
    item = items['item']
    print(item)



    return render_template('festival.html')
@app.route('/hospital.html')
def hospital():
    return render_template('hospital.html')


if __name__ == '__main__':
    app.run()
