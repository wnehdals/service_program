from flask import Flask, request, jsonify, render_template
import requests
import json
import Response

def getErrorChildren():
    response = Response.Response(400).getResponse()

    jsonVal = json.dumps(response, ensure_ascii=False, indent=4)

    return jsonVal

def getChildren(cityCode=41190, pageNum=1):
    host = 'https://e-childschoolinfo.moe.go.kr/api/notice/basicInfo.do'

    para = {'key': 'b65bc721a0d74ff3a210500ab06563bf',
              'sidoCode': '41',
              'sggCode': '41190',
              'pageCnt': '11',
              'currentPage': '1'}

    para['sggCode'] = cityCode
    para['currentPage'] = pageNum

    tmp_para = {'key': 'b65bc721a0d74ff3a210500ab06563bf',
              'sidoCode': '41',
              'sggCode': '41190',}
    tmp_para['sggCode'] = cityCode
    tmp_data1 = requests.get(host, params=tmp_para).json()
    tmp_data2 = tmp_data1['kinderInfo']
    totalCnt = tmp_data2[-1]['key']
    print(totalCnt)

    para['pageCnt'] = int(totalCnt) // 12
    print(para['pageCnt'])

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