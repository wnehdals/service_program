class Response:
    body = ""
    def __init__(self, resultCode):
        self.resultCode = resultCode
    def setBody(self, body):
        self.body = body
    def getResponse(self):
        header = dict(resultCode = "", resultMsg="")
        if(self.resultCode == 200):
            response = dict(header="", body="")
            header['resultCode'] = "200"
            header['resultMsg'] = 'OK'
            response['header'] = header
            response['body'] = self.body
            return response
        elif(self.resultCode == 10):
            response = dict(header="")
            header['resultCode'] = "10"
            header['resultMsg'] = 'Unable to get kindergarten information'
            response['header'] = header
            return response
        elif (self.resultCode == 20):
            response = dict(header="")
            header['resultCode'] = "20"
            header['resultMsg'] = 'Unable to get festival information'
            response['header'] = header
            return response
        elif (self.resultCode == 30):
            response = dict(header="")
            header['resultCode'] = "30"
            header['resultMsg'] = 'Unable to get hospital information'
            response['header'] = header
            return response
        elif (self.resultCode == 400):
            print(400)
            response = dict(header="")
            header['resultCode'] = "400"
            header['resultMsg'] = 'Incorrect parameter'
            response['header'] = header
            return response



