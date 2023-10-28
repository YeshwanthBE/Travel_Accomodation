import os
import requests
import yaml
import json
from flask_mail import Mail,Message
class acm:
    def __init__(self,filepath):
        with open(filepath, 'r') as file:
            config=yaml.safe_load(file)
            db=config['database']['baseurl']
            self.baseurl=f'{db}/acm' 
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

    def register(self,inn_json,jwt):
        header={"Authorization": jwt}
        return requests.post(f'{self.baseurl}/ad',headers=header,json=inn_json)
    
    def showacm(self,params):
        return requests.get(f'{self.baseurl}/ad',params=params)
    
    def modifyacm(self,inn_json,jwt,params):
        header={"Authorization": jwt}
        return requests.patch(f'{self.baseurl}/ad',json=inn_json,headers=header,params=params)
    
    def delacm(self,jwt,params):
        header={"Authorization": jwt}
        return requests.delete(f'{self.baseurl}/ad',headers=header,params=params)

    def searchacm(self,params):
        return requests.get(f'{self.baseurl}/',params=params)