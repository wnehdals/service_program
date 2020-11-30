from flask import Flask, request, jsonify, render_template
import hospital_demo
import requests
import json
import re

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
    #parser = reqparse.RequestParser()
    #parser.add_argument('pageNum', required=true, type=string)
    #arg = parser.parse_args()
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


def festival(pageNum=1):
    return render_template('festival.html')