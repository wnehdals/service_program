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
    if response_tree[0][0].text != "00":
        print("BAD RESPONSE FROM SERVER.")

    # check body
    body_tree = response_tree[1]

    hospital_list = []

    for body_element in body_tree:
        if body_element.tag == "items":
            # parse returned hospitals
            for item in body_element:
                hospital = Hospital()
                hospital.distance = item[1].text
                hospital.address = item[2].text
                hospital.level = item[3].text
                hospital.facility = item[4].text
                hospital.emergency_code = item[5].text
                hospital.fax_number = item[6].text
                hospital.status = item[7].text
                hospital.name = item[8].text
                hospital.contact = item[9].text
                hospital.end_time = item[10].text
                hospital.hospital_id = item[11].text
                hospital.latitude = item[12].text
                hospital.longitude = item[13].text
                hospital.start_time = item[14].text
                hospital_list.append(hospital)
        elif body_element.tag == "numOfRows":
            num_or_rows = body_tree[1].text
        elif body_element.tag == "pageNo":
            page_no = body_tree[2].text
        elif body_element.tag == "totalCount":
            hospital_count = body_tree[3].text

    print("THERE ARE {} NUMBER OF ROWS PER PAGE.".format(num_or_rows))
    print("CURRENT PAGE NUMBER IS {}.".format(page_no))
    print("TOTAL ITEM COUNT IS {}.".format(hospital_count))

    print("END OF DEMO")

    return render_template("hospital.html", item_count=hospital_count, items=hospital_list)
