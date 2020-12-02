from flask import Flask, request, jsonify, render_template
import requests
import json
import re
import Response
def getErrorFestival():
    response = Response.Response(400).getResponse()

    jsonVal = json.dumps(response, ensure_ascii=False, indent=4)

    return jsonVal

def getFestival(city):
    host = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList'
    cityDic = {
        '가평군' : '1',
        '고양시' : '2',
        '과천시' : '3',
        '광명시' : '4',
        '광주시' : '5',
        '구리시' : '6',
        '군포시' : '7',
        '김포시' : '8',
        '남양주시' : '9',
        '동두천시' : '10',
        '부천시' : '11',
        '성남시' : '12',
        '수원시' : '13',
        '시흥시' : '14',
        '안산시' : '15',
        '안성시' : '16',
        '안양시' : '17',
        '양주시' : '18',
        '양평군' : '19',
        '여주시' : '20',
        '연천군' : '21',
        '오산시' : '22',
        '용인시' : '23',
        '의왕시' : '24',
        '의정부시' : '25',
        '이천시' : '26',
        '파주시' : '27',
        '평택시' : '28',
        '포천시' : '29',
        '하남시' : '30',
        '화성시' : '31'
    }
    params = {'ServiceKey': 'mjcDOZkT0XqWULC1L3PAFfxCere4Wq1oXpTJv6jmdF5RmBMPaN6A6Ju112m74zBmsXVsYDW7YJOCH40Q4nmDwg==',
              'contentTypeId': '15',
              'areaCode': '31',
              'sigunguCode' : '1',
              'listYN': 'Y',
              'MobileOS': 'ETC',
              'MobileApp': 'TourAPI3.0_Guide',
              'arrange': 'A',
              'numOfRows': '12',
              'pageNo': '1',
              '_type': 'json'}
    if(city == ""):
        params['sigunguCode'] = city
    else:
        params['sigunguCode'] = city
    list = []
    #parser = reqparse.RequestParser()
    #parser.add_argument('pageNum', required=true, type=string)
    #arg = parser.parse_args()
    totalCount = getFestivalTotalCount(host, params)
    print(totalCount)
    params['numOfRows'] = totalCount
    if(totalCount == 0):
        festival = dict(img="", title="", contentId="", overview="", startDate="", endDate="", addr="")
        response = Response.Response(200)
        response.setBody(festival)
        response = response.getResponse()
        jsonVal = json.dumps(response, ensure_ascii=False, indent=4)
        return jsonVal
    elif totalCount == 1:
        item = getFestivalItem(host,params)
        oneList = []
        oneList.append(item)
        item = oneList
        imgList = getFestivalImgUrl(item)
        titleList = getFestivalTitle(item)
        contentIdList = getFestivalContentId(item)
        overviewList,addrList = getFestivalOverView(contentIdList)
        startList, endList = getFestivalDate(contentIdList)
        for i in range(len(item)):
            festival = dict(img="", title="", contentId="", overview="", startDate="", endDate="",addr="")
            festival['img'] = imgList[i]
            festival['title'] = titleList[i]
            festival['contentId'] = contentIdList[i]
            festival['overview'] = overviewList[i]
            festival['startDate'] = startList[i]
            festival['endDate'] = endList[i]
            festival['addr'] = addrList[i]
            list.append(festival)
        response = Response.Response(200)
        response.setBody(list)
        response = response.getResponse()
        jsonVal = json.dumps(response, ensure_ascii=False, indent=4)
        return jsonVal
    else:
        item = getFestivalItem(host, params)
        imgList = getFestivalImgUrl(item)
        titleList = getFestivalTitle(item)
        contentIdList = getFestivalContentId(item)
        overviewList, addrList = getFestivalOverView(contentIdList)
        startList, endList = getFestivalDate(contentIdList)
        for i in range(len(item)):
            festival = dict(img="", title="", contentId="", overview="", startDate="", endDate="", addr="")
            festival['img'] = imgList[i]
            festival['title'] = titleList[i]
            festival['contentId'] = contentIdList[i]
            festival['overview'] = overviewList[i]
            festival['startDate'] = startList[i]
            festival['endDate'] = endList[i]
            festival['addr'] = addrList[i]
            list.append(festival)
        response = Response.Response(200)
        response.setBody(list)
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