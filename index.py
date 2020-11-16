from flask import Flask, request, jsonify, render_template
import hospital_demo
import requests
import json
import re

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

@app.route('/festival.html/<pageNum>')
@app.route('/festival.html', methods=['POST', 'GET'])
def festival(pageNum=1):
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
    params['pageNo'] = pageNum

    item = getFestivalItem(host, params)
    imgList = getFestivalImgUrl(item)
    titleList = getFestivalTitle(item)
    contentIdList = getFestivalContentId(item)
    overviewList = getFestivalOverView(contentIdList)
    return render_template('festival.html', imgList=imgList, titleList=titleList, overviewList=overviewList)


def getFestivalOverView(contentIdList):
    host = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailCommon'
    query = {
        'ServiceKey': 'mjcDOZkT0XqWULC1L3PAFfxCere4Wq1oXpTJv6jmdF5RmBMPaN6A6Ju112m74zBmsXVsYDW7YJOCH40Q4nmDwg==',
        'contentTypeId': '15',
        'contentId': '2624592',
        'MobileOS': 'ETC',
        'MobileApp': 'TourAPI3.0_Guide',
        'defaultYN': 'Y',
        'firstImageYN': 'N',
        'areacodeYN': 'N',
        'catcodeYN': 'N',
        'addrinfoYN': 'Y',
        'mapinfoYN': 'Y',
        'overviewYN': 'Y',
        'transGuideYN': 'N',
        '_type': 'json'

    }
    list = []

    for i in contentIdList:
        query['contentId'] = i
        item = getFestivalItem(host, query)
        s = item['overview']
        s = re.sub('(<([^>]+)>)', '', s)
        list.append(s)
    return list


def getFestivalItem(url, query):
    res = requests.get(url, params=query).json()
    response = res['response']
    body = response['body']
    items = body['items']
    item = items['item']
    return item


def getFestivalContentId(item):
    list = []
    for i in item:
        list.append(i['contentid'])
    return list


def getFestivalImgUrl(item):
    list = []
    for i in item:
        if ('firstimage' in i):
            list.append(i['firstimage'])
        else:
            list.append("http://placehold.it/700x300")

    return list


def getFestivalTitle(item):
    list = []
    for i in item:
        list.append(i['title'])
    return list


@app.route('/hospital')
def hospital():
    # return render_template('hospital.html')
    return hospital_demo.demo()


if __name__ == '__main__':
    app.run()
