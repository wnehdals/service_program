from flask import Flask, request, jsonify, render_template
import requests, json, re
import kinderInfo, festivalInfo, index
import Response

def getErrorSearch():
    response = Response.Response(400).getResponse()

    jsonVal = json.dumps(response, ensure_ascii=False, indent=4)

    return jsonVal

def getSearch(city):
    jsonStringA = kinderInfo.getChildren(city)
    jsonStringB = festivalInfo.getFestival(city)
    jsonStringC = index.hospital_request_simple(city)
    dictA = json.loads(jsonStringA)
    dictB = json.loads(jsonStringB)
    dictC = json.loads(jsonStringC)

    merged_dict = {}
    merged_dict['kinder'] = dictA["body"]
    merged_dict['festival'] = dictB["body"]
    merged_dict['hospital'] = dictC["body"]

    response = Response.Response(200)
    response.setBody(merged_dict)
    response = response.getResponse()
    jsonVal = json.dumps(response, ensure_ascii=False, indent=4)

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
    address = []
    for i in contentIdList:
        query['contentId'] = i
        item = getFestivalItem(host, query)
        s = item['overview']
        addr = item['addr1']
        s = re.sub('(<([^>]+)>)', '', s)
        list.append(s)
        address.append(addr)
    return list, address


def getFestivalItem(url, query):
    res = requests.get(url, params=query).json()
    response = res['response']
    body = response['body']
    items = body['items']
    item = items['item']
    return item

def getFestivalTotalCount(url, query):
    res = requests.get(url, params=query).json()
    response = res['response']
    body = response['body']
    totalCount = body['totalCount']
    return totalCount


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