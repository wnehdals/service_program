import pymysql

my_db = pymysql.connect(
    user='root',
    passwd='{ssw15Wrnjsgh}',
    host='127.0.0.1',
    db='MYSQL80',
    charset='utf8'
)

cursor = my_db.cursor(pymysql.cursors.DictCursor)

class KinderInfo:

    key = 00
    officeedu = 'officeedu'
    subofficeedu = 'subofficeedu'
    kindername = 'kindername'
    establish = 'establish'
    rppnname = 'rppnname'
    ldgrname = 'ldgrname'
    edate = 'edate'
    odate = 'odate'
    addr = 'addr'
    telno = 'telno'
    hpaddr = 'hpaddr'
    opertime = 'opertime'
    clcnt3 = 0
    clcnt4 = 0
    clcnt5 = 0
    mixclcnt = 0
    shclcnt = 0
    ppcnt3 = 0
    ppcnt4 = 0
    ppcnt5 = 0
    mixppcnt = 0
    shppcnt = 0

    def __init__(self):
        pass