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
            config=yaml.safe_load(file)
            db=config['database']['baseurl']
            self.baseurl=f'{db}/dbprofile/{ap}' 
            self.mail=config['mail']

    def isexist(self,mailid):
        if requests.get(f'{self.baseurl}/{mailid}/exists').status_code==200:
            return True
        else:
            return False
        
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
        return requests.post(f'{self.baseurl}/Signup',json=user_json)
    
    def showprofile(self,mailid):
        return requests.get(f'{self.baseurl}/{mailid}')

    def auth(self,mailid,pwd):
        return requests.post(f'{self.baseurl}/{mailid}/auth',json={"password":pwd})
    
    def modifyuser(self,maild,user_json):
        return requests.patch(f'{self.baseurl}/{maild}',json=user_json)
    
    def deluser(self,mailid,pwd):
        response=self.auth(mailid,pwd)
        if response.status_code==200:
            return requests.delete(f'{self.baseurl}/{mailid}')
        else:
            return response
    
    def rstpwd(self,mailid,token,pwd):
        response=json.loads(requests.get(f'{self.baseurl}/{mailid}/tk').json())
        if token != response['tk'] or dt.now()>dt.strptime(response['expiry'],"%Y-%m-%d %H:%M:%S"):
            return False
        return requests.post(f'{self.baseurl}/{mailid}',json=pwd)
    
    def settoken(self,mailid,token):
        return requests.post(f'{self.baseurl}/{mailid}/tk?token={token}')