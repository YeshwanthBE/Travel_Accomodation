import os
import requests
import yaml
import json
from flask_mail import Mail,Message
from flask import make_response
class bking:
    def __init__(self,filepath):
        with open(filepath, 'r') as file:
            config=yaml.safe_load(file)
            db=config['database']['baseurl']
            self.baseurl=f'{db}' 
            self.mail=config['mail']
            self.accom=config['accomodation']['url']
        
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

    def booking(self,inn_json,jwt):
        header={"Authorization": jwt}
        response=requests.post(f'{self.baseurl}/dbbk/',headers=header,json=inn_json)
        data=response.json()
        data["acmid"]=requests.get(f"{self.accom}/acm/op/",params={"mailid":data['acmid']})
        return data,response.status_code

    def showbk(self,jwt,params):
        header={"Authorization": jwt}
        return requests.get(f'{self.baseurl}/dbbk/',headers=header,params=params)
    
    
    def delbk(self,jwt,params):
        header={"Authorization": jwt}
        return requests.delete(f'{self.baseurl}/dbbk/',headers=header,params=params)

    def searchbk(self,params):
        return requests.get(f'{self.baseurl}/dbbk/allbk/',params=params)