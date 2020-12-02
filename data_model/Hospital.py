class Hospital:
    def __init__(self):
        self.distance = 0.0
        self.address = "HOSPITAL_ADDRESS"
        self.level = "HOSPITAL_LEVEL"
        self.facility = "FACILITY_CLASS"
        self.emergency_code = "EMERGENCY_CODE"
        self.fax_number = "FAX_NUMBER"
        self.status = "RUNNING_STATUS"
        self.name = "HOSPITAL_NAME"
        self.contact = "HOSPITAL_CONTACT"
        self.start_time = "HOSPITAL_START_TIME"
        self.end_time = "HOSPITAL_END_TIME"
        self.hospital_id = "HOSPITAL_ID"
        self.latitude = "HOSPITAL_LATITUDE"
        self.longitude = "HOSPITAL_ALTITUDE"


class Hospital_v2:
    def __init__(self):
        self.address = "HOSPITAL_ADDRESS"  # dutyAddr
        self.level = "HOSPITAL_LEVEL"  # dutyDivNam
        self.emergency_code_name = "EMERGENCY_CODE_NAME"  # dutyEmclsName
        self.emergency_room_available = True  # dutyEryn
        self.information = "HOSPITAL_INFORMATION"  # dutyInf
        self.information_etc = "HOSPITAL_INFORMATION_ETC"  # dutyEtc
        self.address_alias = "HOSPITAL_ADDRESS_ALIAS"  # dutyMapimg
        self.name = "HOSPITAL_NAME"  # dutyName
        self.contact = "HOSPITAL_CONTACT"  # dutyTel1
        self.latitude = "HOSPITAL_LATITUDE"  # wgs84Lat
        self.longitude = "HOSPITAL_LONGITUDE"  # wgs84Lon
        self.start_time_mon = "START TIME - MONDAY"  # dutyTime1s
        self.close_time_mon = "CLOSE TIME - MONDAY"  # dutyTime1c
        self.start_time_tue = "START TIME - MONDAY"  # dutyTime2s
        self.close_time_tue = "CLOSE TIME - MONDAY"  # dutyTime2c
        self.start_time_wed = "START TIME - MONDAY"  # dutyTime3s
        self.close_time_wed = "CLOSE TIME - MONDAY"  # dutyTime3c
        self.start_time_thu = "START TIME - MONDAY"  # dutyTime4s
        self.close_time_thu = "CLOSE TIME - MONDAY"  # dutyTime4c
        self.start_time_fri = "START TIME - MONDAY"  # dutyTime5s
        self.close_time_fri = "CLOSE TIME - MONDAY"  # dutyTime5c
        self.start_time_sat = "START TIME - MONDAY"  # dutyTime6s
        self.close_time_sat = "CLOSE TIME - MONDAY"  # dutyTime6c
        self.start_time_sun = "START TIME - MONDAY"  # dutyTime7s
        self.close_time_sun = "CLOSE TIME - MONDAY"  # dutyTime7c

