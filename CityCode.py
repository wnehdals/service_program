class CityCode:
    def __init__(self):
        self.city_codes = {
            '가평군': '1',
            '고양시': '2',
            '과천시': '3',
            '광명시': '4',
            '광주시': '5',
            '구리시': '6',
            '군포시': '7',
            '김포시': '8',
            '남양주시': '9',
            '동두천시': '10',
            '부천시': '11',
            '성남시': '12',
            '수원시': '13',
            '시흥시': '14',
            '안산시': '15',
            '안성시': '16',
            '안양시': '17',
            '양주시': '18',
            '양평군': '19',
            '여주시': '20',
            '연천군': '21',
            '오산시': '22',
            '용인시': '23',
            '의왕시': '24',
            '의정부시': '25',
            '이천시': '26',
            '파주시': '27',
            '평택시': '28',
            '포천시': '29',
            '하남시': '30',
            '화성시': '31'
        }

    def get_code(self, city_name: str):
        code = self.city_codes.get(city_name)
        return -1 if code is None else code

    def get_name(self, city_code: int):
        for name, code in self.city_codes.items():
            if code == city_code:
                return name

        return "-"
