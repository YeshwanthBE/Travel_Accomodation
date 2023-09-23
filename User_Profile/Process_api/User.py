import os
import requests
import yaml
import json
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
    
    def register(self,user_json):
        return requests.post(f'{self.baseurl}/Signup',json=user_json)
    
    def showprofile(self,mailid):
        return requests.get(f'{self.baseurl}/%s',(mailid,))

    def auth(self,mailid,pwd):
        return requests.post(f'{self.baseurl}/%s/auth',json={"password":pwd})
    
    def modifyuser(self,maild,user_json):
        return requests.patch(f'{self.baseurl}/%s',json=user_json)
    
    def deluser(self,mailid,pwd):
        self.auth(mailid,pwd)
        return requests.delete(f'{self.baseurl}/mailid')
    
    def resetpwd(self,mailid):
        pass

    
    