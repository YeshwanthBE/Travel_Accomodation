import os
import requests
import yaml
import jsonify
class Profile:
    def __init__(self,filepath,mailid=''):
        with open(filepath, 'r') as file:
            config=yaml.safe_load(file)
            db=config['database']['baseurl']
            self.baseurl=f'{db}/profile' 
            self.mail=config['mail']
        self.exist=requests.get(f'{self.baseurl}/{mailid}/exists')

    def send_email(self,to, subject, text):
        url = f"https://api.mailgun.net/v3/{self.mail['MAILGUN_DOMAIN']}/messages"
        auth = ("api", self.mail['MAILGUN_API_KEY'])
        data = {
            "from": "oneyesexplora19@gmail.com",
            "to": to,
            "subject": subject,
            "text": text,
        }
        response = requests.post(url, auth=auth, data=data)
        return response
    
    def register(self,user_json):
        response=requests.get(f'{self.baseurl}/%s/exists',(user_json['mailid'],))
        if response.status_code==200:
            return jsonify({"message: Mailid already exists"}),400
        response=requests.post(f'{self.baseurl}/Signup',json=user_json)
        return response
    
    def auth(self,mailid,pwd):
        if self.exist.status_code!=200:
            return jsonify({"message":"Invalid Mailid or password"}),401
        response=requests.post(f'{self.baseurl}/%s/auth',json={"password":pwd})
        return response
    
    def resetpwd(self,mailid):
        pass
        #response=self.send_email(mailid,"Password Recovery",)

    def modifyuser(self,maild,user_json):
        if self.exist.status_code!=200:
            return jsonify({"message":"User not exists"}),400
        response=requests.patch(f'{self.baseurl}/%s',json=user_json)
        return response
    
    def deluser(self,mailid):
        pass

    def showprofile(self,mailid):
        if self.exist.status_code!=200:
            return jsonify({"message":"User not exists"}),400
        return requests.get(f'{self.baseurl}/%s',(mailid,))
