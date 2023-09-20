import requests
import yaml
import jsonify
class Profile:
    def __init__(self,filepath,mailid=''):
        with open(filepath, 'r') as file:
            db= yaml.safe_load(file)['database']['baseurl']
            self.baseurl=f'{self.db}/profile' 
        self.exist=requests.get(f'{self.baseurl}/%s/exists',(mailid,))
        
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