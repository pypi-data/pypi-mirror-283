class openioe_apis:
    def __init__(self, *args):
        self.endpoint='http://apps.openioe.in/openioe/api/'
        self.appendpoint='http://apps.openioe.in/openioe/'
        self.APIKey=''
        self.Devices=[]
        self.response_text=[]
        self.response_status_code=[]  
        self.DeviceID=0
        self.DevicePin=0
        self.Data=[]
        self.DataJSON=''
        self.DataXML=''
        self.UserEmail=''
        self.UserPassword=''
        self.DeviceName='D'+DateNumberGeneration()
        self.CryptoName='None'
        self.DataFormat='Value'

        if len(args) == 0:
            self.a=0           
        elif len(args) == 1:
            self.a=args[0]
            
    def Developer(self, *args):
        print('Hi, Welcome to OpenIoE')
        print('Developed by Dr. Venkataswamy R')
        print('https://venkataswamy.in')
        print('venkataswamy.r@gmail.com')

    def GenerateAPIKey(self, *args):
        import requests
        import json
        if len(args) == 0:
            u=self.endpoint+'generateapikey/'+str(self.UserEmail)+'/'+str(self.UserPassword)+'/'
            resp = requests.get(u)
            self.response_text=resp.json()
            self.response_status_code=resp.status_code
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code

    def ReadAPIKey(self, *args):
        import requests
        if len(args) == 0:
            u=self.endpoint+'showapikey/'+str(self.UserEmail)+'/'+str(self.UserPassword)+'/'
            resp = requests.get(u)
            self.response_text=resp.text
            self.response_status_code=resp.status_code
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code
    
    def CreateDevice(self, *args):
        import requests
        if len(args) == 0:
            u=self.endpoint+'createuserdevice/'+str(self.APIKey)+'/'+str(self.DeviceName)+'/'+str(self.CryptoName)+'/'+str(self.DataFormat)+'/'
            print(u)
            resp = requests.get(u)
            self.response_text=resp.text
            self.response_status_code=resp.status_code
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code
        
    def Read(self, *args):
        import requests
        if len(args) == 0:
            for i in range(len(self.Devices)):
                u=self.endpoint+'showdevicevalue/'+str(self.APIKey)+'/'+str(self.Devices[i][0])+'/'+str(self.Devices[i][1])+'/'
                resp = requests.get(u)
                self.response_text.append(resp.text)
                self.response_status_code.append(resp.status_code)
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code

    def ReadValue(self, *args):
        import requests
        if len(args) == 0:
            u=self.endpoint+'showdevicevalue/'+str(self.APIKey)+'/'+str(self.DeviceID)+'/'+str(self.DevicePin)+'/'
            resp = requests.get(u)
            self.response_text=resp.text
            self.response_status_code=resp.status_code
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code
    
    def ReadJSON(self, *args):
        import requests
        import json
        if len(args) == 0:
            u=self.endpoint+'showdevicejson/'+str(self.APIKey)+'/'+str(self.DeviceID)+'/'+str(self.DevicePin)+'/'
            resp = requests.get(u)
            self.response_text=resp.text
            self.response_status_code=resp.status_code
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code

    def ReadXML(self, *args):
        import requests
        if len(args) == 0:
            u=self.endpoint+'showdevicexml/'+str(self.APIKey)+'/'+str(self.DeviceID)+'/'+str(self.DevicePin)+'/'
            resp = requests.get(u)
            self.response_text=resp.text
            self.response_status_code=resp.status_code
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code

    def WriteValue(self, *args):
        import requests
        if len(args) == 0:
            u=self.endpoint+'updatedevicevalue/'+str(self.APIKey)+'/'+str(self.DeviceID)+'/'+str(self.DevicePin)+'/'+str(self.Data)
            resp = requests.get(u)
            self.response_text=resp.text
            self.response_status_code=resp.status_code
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code
    
    def WriteJSON(self, *args):
        import requests
        import json
        headers = {'Content-type': 'application/json'}
        if len(args) == 0:
            u=self.endpoint+'updatedevicejson/'+str(self.APIKey)+'/'+str(self.DeviceID)+'/'+str(self.DevicePin)
            resp=requests.post(u, json=self.DataJSON, headers=headers)
            self.response_text=resp.text
            self.response_status_code=resp.status_code
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code


    def WriteXML(self, *args):
        import requests
        headers = {'Content-type': 'application/xml'}
        if len(args) == 0:
            u=self.endpoint+'updatedevicexml/'+str(self.APIKey)+'/'+str(self.DeviceID)+'/'+str(self.DevicePin)
            resp=requests.post(u, data=self.DataXML, headers=headers)
            self.response_text=resp.text
            self.response_status_code=resp.status_code
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code
        
            
    def Write(self, *args):
        import requests
        if len(args) == 0:
            for i in range(len(self.Devices)):
                u=self.endpoint+'updatedevicevalue/'+str(self.APIKey)+'/'+str(self.Devices[i][0])+'/'+str(self.Devices[i][1])+'/'+str(self.Data[i])
                resp = requests.get(u)
                self.response_text.append(resp.text)
                self.response_status_code.append(resp.status_code)
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code
    
    def DownloadDeviceData(self, *args):
        import requests
        import pandas as pd
        if len(args) == 0:
            u=self.appendpoint+'DownloadTimeSeriesData?device_id='+str(self.DeviceID)+'&data_format=Value'
            c=pd.read_csv(u)
            self.response_text=c
        else:
            print('Do not Pass parameters')
            self.response_text=''
        return self.response_text, self.response_status_code
    
def DateNumberGeneration():
    from datetime import datetime
    a = datetime.now()
    a = int(a.strftime('%Y%m%d%H%M%S'))
    return str(a)