import os
import requests
import yaml
import json

class reviews:
    def __init__(self,filepath):
        with open(filepath, 'r') as file:
            config=yaml.safe_load(file)
            db=config['database']['baseurl']
            self.baseurl=f'{db}' 

    def add(self,inn_json,jwt):
        header={"Authorization": jwt}
        print(f'{self.baseurl}/dbreviews/')
        return requests.post(f'{self.baseurl}/dbreviews/',headers=header,json=inn_json)

    def delete(self,jwt,params):
        header={"Authorization": jwt}
        return requests.delete(f'{self.baseurl}/dbreviews/',headers=header,params=params)
    
    def mod(self,jwt,inn_json):
        header={"Authorization": jwt}
        return requests.patch(f'{self.baseurl}/dbreviews/',headers=header,json=inn_json)

    def searchall(self,inn_json,jwt):
        return requests.get(f'{self.baseurl}/dballreviews/',json=inn_json,headers={"Authorization": jwt})