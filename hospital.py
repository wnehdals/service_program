from flask import Flask, jsonify, render_template
import requests, json
import xml.etree.ElementTree as ET
from data_model.Hospital import Hospital, Hospital_v2
from Response import Response

auth_key = '5jlnt%2BDn%2FmCMkk6r9m80%2F%2BxSNIB52nikP2Oo4iqUJ0eoLcJbIXAcRAAkSbrRACIOQ2IrxfGCmIuSGKMcDW4J2g%3D%3D'


def doc():
    return render_template("hospital_doc.html")


def request_all_hospital_api_address(address_major: str, address_minor: str, item_count: int):
    service_url = 'http://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire'
    query_params = {"serviceKey": auth_key,
                    "Q0": address_major,
                    "Q1": address_minor,
                    "numOfRows": item_count
                    }

    params_url = "?"
    for param in query_params.items():
        param_string = "{}={}&".format(param[0], param[1])
        params_url += param_string
    params_url = params_url[:-1]

    request_url = service_url + params_url
    print(request_url)
    api_request = requests.get(request_url)

    return api_request


def request_api_address(address_major: str, address_minor: str):
    service_url = 'http://apis.data.go.kr/B552657/HsptlAsembySearchService/getBabyListInfoInqire'
    query_params = {"serviceKey": auth_key,
                    "Q0": address_major,
                    "Q1": address_minor,
                    "numOfRows": 100
                    }

    params_url = "?"
    for param in query_params.items():
        param_string = "{}={}&".format(param[0], param[1])
        params_url += param_string
    params_url = params_url[:-1]

    request_url = service_url + params_url
    print(request_url)
    api_request = requests.get(request_url)

    return api_request


def request_api_lonlat(longitude: float, latitude: float):
    service_url = 'http://apis.data.go.kr/B552657/HsptlAsembySearchService/getBabyLcinfoInqire'
    query_params = {"serviceKey": auth_key,
                    "pageNo": 1,
                    "numOfRows": 10,
                    "WGS84_LON": longitude,
                    "WGS84_LAT": latitude
                    }

    params_url = "?"
    for param in query_params.items():
        param_string = "{}={}&".format(param[0], param[1])
        params_url += param_string
    params_url = params_url[:-1]

    request_url = service_url + params_url
    print(request_url)
    api_request = requests.get(request_url)

    return api_request


def demo():
    response_raw = request_api_lonlat(127.0851566, 37.48813256)
    response_raw_tree = ET.fromstring(response_raw.text)

    body_tree = response_raw_tree.find("body")
    hospital_list = []
    if body_tree is not None:
        items_tree = body_tree.find("items")
        if items_tree is not None:
            for item in items_tree:
                hospital = {}

                for information in item:
                    if information.tag == "distance":
                        hospital["distance"] = information.text
                    elif information.tag == "dutyAddr":
                        hospital["address"] = information.text
                    elif information.tag == "dutyDiv":
                        hospital["level"] = information.text
                    elif information.tag == "dutyDivName":
                        hospital["facility"] = information.text
                    elif information.tag == "dutyEmcls":
                        hospital["emergency_code"] = information.text
                    elif information.tag == "dutyFax":
                        hospital["fax_number"] = information.text
                    elif information.tag == "dutyLvkl":
                        hospital["status"] = information.text
                    elif information.tag == "dutyName":
                        hospital["name"] = information.text
                    elif information.tag == "dutyTel1":
                        hospital["contact"] = information.text
                    elif information.tag == "endTime":
                        hospital["end_time"] = information.text
                    elif information.tag == "hpid":
                        hospital["hospital_id"] = information.text
                    elif information.tag == "latitude":
                        hospital["latitude"] = information.text
                    elif information.tag == "longitude":
                        hospital["longitude"] = information.text
                    elif information.tag == "startTime":
                        hospital["start_time"] = information.text

                hospital_list.append(hospital)

    if len(hospital_list) == 0:
        hospital_list.append(Hospital())

    return render_template("hospital.html", item_count=len(hospital_list), items=hospital_list)


def response_hospital_info_lonlat(longitude, latitude):
    response_raw = request_api_lonlat(longitude, latitude)
    response_raw_tree = ET.fromstring(response_raw.text)

    response_dict = {"status": True,
                     "hospital_list": []
                     }

    header_tree = response_raw_tree.find("header")
    result_code = header_tree.find("resultCode")
    if result_code is None or result_code.text != "00":
        response_dict.update({"status": False})

    body_tree = response_raw_tree.find("body")
    if body_tree is None:
        response_dict.update({"status": False})
    else:
        hospital_list = []
        items_tree = body_tree.find("items")
        if items_tree is not None:
            for item in items_tree:
                hospital = {}

                for information in item:
                    if information.tag == "distance":
                        hospital["distance"] = information.text
                    elif information.tag == "dutyAddr":
                        hospital["address"] = information.text
                    elif information.tag == "dutyDiv":
                        hospital["level"] = information.text
                    elif information.tag == "dutyDivName":
                        hospital["facility"] = information.text
                    elif information.tag == "dutyEmcls":
                        hospital["emergency_code"] = information.text
                    elif information.tag == "dutyFax":
                        hospital["fax_number"] = information.text
                    elif information.tag == "dutyLvkl":
                        hospital["status"] = information.text
                    elif information.tag == "dutyName":
                        hospital["name"] = information.text
                    elif information.tag == "dutyTel1":
                        hospital["contact"] = information.text
                    elif information.tag == "endTime":
                        hospital["end_time"] = information.text
                    elif information.tag == "hpid":
                        hospital["hospital_id"] = information.text
                    elif information.tag == "latitude":
                        hospital["latitude"] = information.text
                    elif information.tag == "longitude":
                        hospital["longitude"] = information.text
                    elif information.tag == "startTime":
                        hospital["start_time"] = information.text

                hospital_list.append(hospital)

            response_dict.update({"hospital_list": hospital_list})

    json_response = json.dumps(response_dict, ensure_ascii=False, indent=4)
    return json_response


def response_hospital_info_address(address_major: str, address_minor: str):
    response_raw = request_api_address(address_major, address_minor)
    response_raw_tree = ET.fromstring(response_raw.text)

    response_dict = {"status": True,
                     "hospital_list": []
                     }

    header_tree = response_raw_tree.find("header")
    result_code = header_tree.find("resultCode")
    if result_code is None or result_code.text != "00":
        response_dict.update({"status": False})

    body_tree = response_raw_tree.find("body")
    if body_tree is None:
        response_dict.update({"status": False})
    else:
        hospital_list = []
        items_tree = body_tree.find("items")
        if items_tree is not None:
            for item in items_tree:
                hospital = Hospital_v2()

                for information in item:
                    if information.tag == "dutyAddr":
                        hospital.address = information.text
                    elif information.tag == "dutyDivNam":
                        hospital.level = information.text
                    elif information.tag == "dutyEmclsName":
                        hospital.emergency_code_name = information.text
                    elif information.tag == "dutyEryn":
                        hospital.emergency_room_available = (True if information.text is "2" else False)
                    elif information.tag == "dutyInf":
                        hospital.information = information.text
                    elif information.tag == "dutyEtc":
                        hospital.information_etc = information.text
                    elif information.tag == "dutyMapimg":
                        hospital.address_alias = information.text
                    elif information.tag == "dutyName":
                        hospital.name = information.text
                    elif information.tag == "dutyTel1":
                        hospital.contact = information.text
                    elif information.tag == "wgs84Lat":
                        hospital.latitude = information.text
                    elif information.tag == "wgs84Lon":
                        hospital.longitude = information.text
                    elif information.tag == "dutyTime1s":
                        hospital.start_time_mon = information.text
                    elif information.tag == "dutyTime1c":
                        hospital.close_time_mon = information.text
                    elif information.tag == "dutyTime2s":
                        hospital.start_time_tue = information.text
                    elif information.tag == "dutyTime2c":
                        hospital.close_time_tue = information.text
                    elif information.tag == "dutyTime3s":
                        hospital.start_time_wed = information.text
                    elif information.tag == "dutyTime3c":
                        hospital.close_time_wed = information.text
                    elif information.tag == "dutyTime4s":
                        hospital.start_time_thu = information.text
                    elif information.tag == "dutyTime4c":
                        hospital.close_time_thu = information.text
                    elif information.tag == "dutyTime5s":
                        hospital.start_time_fri = information.text
                    elif information.tag == "dutyTime5c":
                        hospital.close_time_fri = information.text
                    elif information.tag == "dutyTime6s":
                        hospital.start_time_sat = information.text
                    elif information.tag == "dutyTime6c":
                        hospital.close_time_sat = information.text
                    elif information.tag == "dutyTime7s":
                        hospital.start_time_sun = information.text
                    elif information.tag == "dutyTime7c":
                        hospital.close_time_sun = information.text

                hospital_list.append(hospital.__dict__)

            response_dict.update({"hospital_list": hospital_list})

    json_response = json.dumps(response_dict, ensure_ascii=False, indent=4)
    return json_response


############################################################################
#                           USE THIS VERSION!!!                            #
############################################################################
def response_all_hospital_info_address(address_major: str, address_minor: str, item_count):
    response_raw = request_all_hospital_api_address(address_major, address_minor, item_count)
    response_raw_tree = ET.fromstring(response_raw.text)

    header_tree = response_raw_tree.find("header")
    result_code = header_tree.find("resultCode")
    if result_code is None or result_code.text != "00":
        response = Response(31)
        response = response.getResponse()
        return json.dumps(response, ensure_ascii=False, indent=4)

    body_tree = response_raw_tree.find("body")
    if body_tree is None:
        response = Response(32)
        response = response.getResponse()
        return json.dumps(response, ensure_ascii=False, indent=4)
    else:
        response = Response(200)
        hospital_list = []
        items_tree = body_tree.find("items")
        if items_tree is not None:
            for item in items_tree:
                hospital = Hospital_v2()

                for information in item:
                    if information.tag == "dutyAddr":
                        hospital.address = information.text
                    elif information.tag == "dutyDivNam":
                        hospital.level = information.text
                    elif information.tag == "dutyEmclsName":
                        hospital.emergency_code_name = information.text
                    elif information.tag == "dutyEryn":
                        hospital.emergency_room_available = (True if information.text is "2" else False)
                    elif information.tag == "dutyInf":
                        hospital.information = information.text
                    elif information.tag == "dutyEtc":
                        hospital.information_etc = information.text
                    elif information.tag == "dutyMapimg":
                        hospital.address_alias = information.text
                    elif information.tag == "dutyName":
                        hospital.name = information.text
                    elif information.tag == "dutyTel1":
                        hospital.contact = information.text
                    elif information.tag == "wgs84Lat":
                        hospital.latitude = information.text
                    elif information.tag == "wgs84Lon":
                        hospital.longitude = information.text
                    elif information.tag == "dutyTime1s":
                        hospital.start_time_mon = information.text
                    elif information.tag == "dutyTime1c":
                        hospital.close_time_mon = information.text
                    elif information.tag == "dutyTime2s":
                        hospital.start_time_tue = information.text
                    elif information.tag == "dutyTime2c":
                        hospital.close_time_tue = information.text
                    elif information.tag == "dutyTime3s":
                        hospital.start_time_wed = information.text
                    elif information.tag == "dutyTime3c":
                        hospital.close_time_wed = information.text
                    elif information.tag == "dutyTime4s":
                        hospital.start_time_thu = information.text
                    elif information.tag == "dutyTime4c":
                        hospital.close_time_thu = information.text
                    elif information.tag == "dutyTime5s":
                        hospital.start_time_fri = information.text
                    elif information.tag == "dutyTime5c":
                        hospital.close_time_fri = information.text
                    elif information.tag == "dutyTime6s":
                        hospital.start_time_sat = information.text
                    elif information.tag == "dutyTime6c":
                        hospital.close_time_sat = information.text
                    elif information.tag == "dutyTime7s":
                        hospital.start_time_sun = information.text
                    elif information.tag == "dutyTime7c":
                        hospital.close_time_sun = information.text

                hospital_list.append(hospital.__dict__)

            response.setBody(hospital_list)

    return json.dumps(response.getResponse(), ensure_ascii=False, indent=4)
