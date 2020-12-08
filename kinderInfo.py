from flask import Flask, request, jsonify, render_template
import requests
import json
import Response

def getErrorChildren():
    response = Response.Response(400).getResponse()

    jsonVal = json.dumps(response, ensure_ascii=False, indent=4)

    return jsonVal

def getChildren(cityCode=1, pageNum=1):
    host = 'https://e-childschoolinfo.moe.go.kr/api/notice/basicInfo.do'

    para = {'key': 'b65bc721a0d74ff3a210500ab06563bf',
              'sidoCode': '41',
              'sggCode': '41190',
              'pageCnt': '11',
              'currentPage': '1'}

    para['sggCode'] = getCity(cityCode)
    para['currentPage'] = pageNum

    tmp_para = {'key': 'b65bc721a0d74ff3a210500ab06563bf',
              'sidoCode': '41',
              'sggCode': '41190',}
    tmp_para['sggCode'] = getCity(cityCode)
    tmp_data1 = requests.get(host, params=tmp_para).json()
    tmp_data2 = tmp_data1['kinderInfo']
    totalCnt = tmp_data2[-1]['key']

    para['pageCnt'] = int(totalCnt) // 12

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
    lst5 = []
    for i in kinder:
        a = 0
        if i['ppcnt3'] is not None:
            a += int(i['ppcnt3'])
        if i['ppcnt4'] is not None:
            a += int(i['ppcnt4'])
        if i['ppcnt5'] is not None:
            a += int(i['ppcnt5'])
        if i['mixppcnt'] is not None:
            a += int(i['mixppcnt'])
        if i['shppcnt'] is not None:
            a += int(i['shppcnt'])

        lst5.append(a)

    for i in range(para['pageCnt']):
        children = dict(title="", overview="", telNo="", hpAddr="")
        children['title'] = lst1[i]
        children['overview'] = lst2[i]
        children['telNo'] = lst3[i]
        children['hpAddr'] = lst4[i]
        children['childNo'] = lst5[i]
        list.append(children)
    response = Response.Response(200)
    response.setBody(list)
    response = response.getResponse()
    jsonVal = json.dumps(response, ensure_ascii=False, indent=4)
    return jsonVal

def info(pageNum=1):
    return render_template('children.html')

def getCity(cityIdx):
    cityDic = {
        '가평군': ('1','41820'),
        '고양시': ('2','41281'),
        '과천시': ('3','41173'),
        '광명시': ('4','41210'),
        '광주시': ('5','41610'),
        '구리시': ('6','41310'),
        '군포시': ('7','41410'),
        '김포시': ('8','41570'),
        '남양주시': ('9','41360'),
        '동두천시': ('10','41250'),
        '부천시': ('11','41190'),
        '성남시': ('12','41131'),
        '수원시': ('13','41111'),
        '시흥시': ('14','41390'),
        '안산시': ('15','41271'),
        '안성시': ('16','41550'),
        '안양시': ('17','41171'),
        '양주시': ('18','41630'),
        '양평군': ('19','41830'),
        '여주시': ('20','41670'),
        '연천군': ('21','41800'),
        '오산시': ('22','41370'),
        '용인시': ('23','41461'),
        '의왕시': ('24','41430'),
        '의정부시': ('25','41150'),
        '이천시': ('26','41500'),
        '파주시': ('27','41480'),
        '평택시': ('28','41220'),
        '포천시': ('29','41650'),
        '하남시': ('30','41450'),
        '화성시': ('31','41590')
    }

    for v in cityDic.values():
        if v[0] == str(cityIdx):
            return v[1]

    #오류코드
    return None