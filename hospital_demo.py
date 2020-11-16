from flask import Flask, jsonify, render_template
import requests
import xml.etree.ElementTree as ET
from data_model.Hospital import Hospital


def demo():
    service_url = 'http://apis.data.go.kr/B552657/HsptlAsembySearchService/getBabyLcinfoInqire'
    auth_key = '5jlnt%2BDn%2FmCMkk6r9m80%2F%2BxSNIB52nikP2Oo4iqUJ0eoLcJbIXAcRAAkSbrRACIOQ2IrxfGCmIuSGKMcDW4J2g%3D%3D'
    query_params = {"serviceKey": auth_key,
                    "pageNo": 1,
                    "numOfRows": 10,
                    "WGS84_LON": 127.0851566,
                    "WGS84_LAT": 37.48813256
                    }

    params_url = "?"
    for param in query_params.items():
        param_string = "{}={}&".format(param[0], param[1])
        params_url += param_string
    params_url = params_url[:-1]

    request_url = service_url + params_url
    api_request = requests.get(request_url)

    # print(api_request.url)
    # print(api_request.text)

    response_tree = ET.fromstring(api_request.text)

    # check response code
    # print(response_tree[0][0].tag)
    # print(response_tree[0][0].attrib)
    result_code = response_tree.find("resultCode")
    if result_code is None or result_code.text != "00":
        print("BAD RESPONSE FROM SERVER - result code is not 00")

    # check body
    body_tree = response_tree.find("body")
    if body_tree is None:
        print("BAD RESPONSE FROM SERVER - body element not exist.")

    hospital_list = []

    items_tree = body_tree.find("items")
    if items_tree is not None:
        for item in items_tree:
            hospital = Hospital()

            for information in item:
                if information.tag == "distance":
                    hospital.distance = information.text
                elif information.tag == "dutyAddr":
                    hospital.address = information.text
                elif information.tag == "dutyDiv":
                    hospital.level = information.text
                elif information.tag == "dutyDivName":
                    hospital.facility = information.text
                elif information.tag == "dutyEmcls":
                    hospital.emergency_code = information.text
                elif information.tag == "dutyFax":
                    hospital.fax_number = information.text
                elif information.tag == "dutyLvkl":
                    hospital.status = information.text
                elif information.tag == "dutyName":
                    hospital.name = information.text
                elif information.tag == "dutyTel1":
                    hospital.contact = information.text
                elif information.tag == "endTime":
                    hospital.end_time = information.text
                elif information.tag == "hpid":
                    hospital.hospital_id = information.text
                elif information.tag == "latitude":
                    hospital.latitude = information.text
                elif information.tag == "longitude":
                    hospital.longitude = information.text
                elif information.tag == "startTime":
                    hospital.start_time = information.text

            hospital_list.append(hospital)

    print("END OF DEMO")

    return render_template("hospital.html", item_count=len(hospital_list), items=hospital_list)
