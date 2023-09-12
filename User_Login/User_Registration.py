import mysql.connector as mc
import yaml 
class User:
    def __init__(self,user_json):
        self.name=user_json['name']
        self.mailid=user_json['mailid']
        self.password=user_json['pws']
        self.address=user_json['address']
        self.mobile_no=user_json['phno']

def dbconnect(filepath):
    with open(filepath, 'r') as file:
        db_config= yaml.safe_load(file)    
    db = mc.connect(host="db_config['host']",user="dbconfig['user']",password="db_config['pwd']",database="db_config['db']")



obj=User()
cursor=db.cursor()
cursor.execute("Insert into Users values (%s,%s,%s,%s,%s,)",)