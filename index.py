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


@app.route('/children')
@app.route('/children/<pageNum>')
def getChildren(pageNum=1):
    host = 'https://e-childschoolinfo.moe.go.kr/api/notice/basicInfo.do'

    para = {'key': 'b65bc721a0d74ff3a210500ab06563bf',
              'sidoCode': '41',
              'sggCode': '41190',
              'pageCnt': '11',
              'currentPage': '1'}

    para['currentPage'] = pageNum

    res = requests.get(host, params=para).json()

    list = []
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

    lst4 = []
    for i in kinder:
        lst4.append(i['hpaddr'])
    #print(lst4)

    for i in range(11):
        children = dict(title="", overview="", telNo="", hpAddr="")
        children['title'] = lst1[i]
        children['overview'] = lst2[i]
        children['telNo'] = lst3[i]
        children['hpAddr'] = lst4[i]
        list.append(children)
    jsonVal = json.dumps(list, ensure_ascii=False, indent=4)
    return jsonVal

@app.route('/children.html/<pageNum>')
@app.route('/children.html', methods=['GET'])
def children(pageNum=1):
    return render_template('children.html')

@app.errorhandler(404)
def not_found(error):

    return render_template('404.html')
@app.route('/festival')
@app.route('/festival/<pageNum>')
def getFestival(pageNum=1):
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
    list = []
    item = getFestivalItem(host, params)
    imgList = getFestivalImgUrl(item)
    titleList = getFestivalTitle(item)
    contentIdList = getFestivalContentId(item)
    overviewList = getFestivalOverView(contentIdList)
    startList, endList = getFestivalDate(contentIdList)
    for i in range(12):
        festival = dict(img="", title="", contentId="", overview="", startDate="", endDate="")
        festival['img'] = imgList[i]
        festival['title'] = titleList[i]
        festival['contentId'] = contentIdList[i]
        festival['overview'] = overviewList[i]
        festival['startDate'] = startList[i]
        festival['endDate'] = endList[i]
        list.append(festival)
    jsonVal = json.dumps(list, ensure_ascii=False, indent=4)
    return jsonVal
@app.route('/festival.html/<pageNum>')
@app.route('/festival.html', methods=['GET'])
def festival(pageNum=1):
    '''
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
    '''
    #return render_template('festival.html', imgList=imgList, titleList=titleList, overviewList=overviewList)
    return render_template('festival.html')

def getFestivalDate(contentIdList):
    host = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailIntro'
    query = {
        'ServiceKey': 'mjcDOZkT0XqWULC1L3PAFfxCere4Wq1oXpTJv6jmdF5RmBMPaN6A6Ju112m74zBmsXVsYDW7YJOCH40Q4nmDwg==',
        'contentTypeId': '15',
        'contentId': '2615383',
        'MobileOS': 'ETC',
        'MobileApp': 'soc_project',
        'introYN': 'Y',
        '_type': 'json'
    }
    startlist = []
    endlist = []
    for i in contentIdList:
        query['contentId'] = i
        item = getFestivalItem(host, query)
        endDate = makeDate(str(item['eventenddate']))

        startDate = makeDate(str(item['eventstartdate']))
        startlist.append(startDate)
        endlist.append(endDate)
    return startlist, endlist

def makeDate(date: str):
    d = ''
    d += (date[0:4] + '년 ')
    d += (date[4:6] + '월 ')
    d += (date[6:] + '일')
    return d
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
