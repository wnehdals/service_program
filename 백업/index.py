from flask import Flask, request, jsonify, render_template
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

@app.route('/children.html/<pageNum>')
@app.route('/children.html', methods=['GET'])
def getchilderen():
    pass

@app.route('/children.html/<pageNum>')
@app.route('/children.html', methods=['GET'])
def children():

    host = 'https://e-childschoolinfo.moe.go.kr/api/notice/basicInfo.do?key=b65bc721a0d74ff3a210500ab06563bf&sidoCode=11&sggCode=11110'

    res = requests.get(host).json()
    kinder = res['kinderInfo']

    lst1 = []
    for i in kinder:
        lst1.append(i['kindername'])

    lst2 = []
    for i in kinder:
        lst2.append(i['addr'])

    lst3 = []
    for i in kinder:
        lst3.append(i['telno'])

    return render_template('children.html', titleList=lst1, overviewList=lst2)


@app.route('/festival.html', methods=['POST','GET'])

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
    '''res = requests.get(host, params=params).json()
    response = res['response']
    body = response['body']
    items = body['items']
    item = items['item']
    print(item)
    '''

    item = getItem(host, params)
    imgList = getImgUrl(item)
    titleList = getTitle(item)
    contentIdList = getContentId(item)
    overviewList = getOverView(contentIdList)
    return render_template('festival.html', imgList=imgList, titleList=titleList, overviewList=overviewList)
def getOverView(contentIdList):
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
        '_type' : 'json'

    }
    list = []

    for i in contentIdList:
        query['contentId'] = i
        item = getItem(host, query)
        s = item['overview']
        s = re.sub('(<([^>]+)>)', '', s)
        list.append(s)
    return list


def getItem(url, query):
    res = requests.get(url, params=query).json()
    response = res['response']
    body = response['body']
    items = body['items']
    item = items['item']
    return item


def getContentId(item):
    list = []
    for i in item:
        list.append(i['contentid'])
    return list


def getImgUrl(item):
    list = []
    for i in item:
        list.append(i['firstimage'])

    return list


def getTitle(item):
    list = []
    for i in item:
        list.append(i['title'])
    return list




@app.route('/hospital.html')
def hospital():
    return render_template('hospital.html')


if __name__ == '__main__':
    app.run()
