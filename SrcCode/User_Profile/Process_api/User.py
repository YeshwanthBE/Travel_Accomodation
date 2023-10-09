import os
import requests
import yaml
import json
from flask_mail import Mail,Message
from datetime import datetime as dt
class Profile:
    def __init__(self,filepath,ap):
        self.ap=ap
        with open(filepath, 'r') as file:
            global config
            config=yaml.safe_load(file)
            db=config['database']['baseurl']
            self.baseurl=f'{db}/dbprofile/{ap}' 
            self.mail=config['mail']
        
    def sendmail(self,app,to,subject,body):
        app.config['MAIL_SERVER'] = self.mail['server']
        app.config['MAIL_PORT'] = self.mail['port']
        app.config['MAIL_USE_TLS'] = self.mail['tls']
        app.config['MAIL_USE_SSL'] = self.mail['ssl']
        app.config['MAIL_USERNAME'] = self.mail['username']
        app.config['MAIL_PASSWORD'] = self.mail['password']
        mail=Mail(app)
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
        msg.body = body
        mail.send(msg) 

    def register(self,user_json):
        return requests.post(f'{self.baseurl}/Signup/',json=user_json)
    
    def showprofile(self,jwt):
        header={"Authorization": jwt}
        return requests.get(f'{self.baseurl}/',headers=header)

    def auth(self,user_json):
        return requests.post(f'{self.baseurl}/auth/',json=user_json)
    
    def modifyuser(self,user_json,jwt):
        header={"Authorization": jwt}
        return requests.patch(f'{self.baseurl}/',json=user_json,headers=header)
    
    def deluser(self,jwt,pwd):
        header={"Authorization": jwt}
        return requests.delete(f'{self.baseurl}/',headers=header,json=pwd)
    
    def verifytk(self,mailid,token)->requests.Response:
        response=requests.get(f'{self.baseurl}/tk?mailid={mailid}').json()
        tk=json.loads(response["token"])
        if token != tk["tk"] or dt.now()>dt.strptime(tk["expiry"],"%Y-%m-%d %H:%M:%S"):
            return False
        return response["jwt"]
    
    def settoken(self,mailid,token):
        return requests.post(f'{self.baseurl}/tk/',json={"mailid":mailid,"token":token})

    def rstpwd(self,pwd,jwt):
        return requests.post(f'{self.baseurl}/',json=pwd,headers={"Authorization": jwt})

    def promote(self,mailid:json,jwt):
        return requests.post(f'{self.baseurl}/promote/',json=mailid,headers={"Authorization": jwt})
    
    def showall(self,mailid:json,jwt):
        return requests.get(f'{self.baseurl}/showallusers/',params=mailid,headers={"Authorization": jwt})
    
    def accommodations(self,params):
        acms=json.loads(requests.get(f"{config['url']['acmurl']}",params=params).json())
        bk= json.loads(requests.get(f"{config['url']['bkurl']}",params=params).json())
        acmids_to_remove = [acm_id[0] for acm_id in bk["acmid"]]
        acms_filtered = [acm for acm in acms if acm["acmid"] not in acmids_to_remove]
        return json.dumps(acms_filtered)