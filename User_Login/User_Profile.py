import mysql.connector as mc
import hashlib
import yaml 
import json
import os
class User:
    def __init__(self,filepath):
        with open(filepath, 'r') as file:
            db_config= yaml.safe_load(file)['database']    
            self.db = mc.connect(host=db_config['host'],user=db_config['username'],password=db_config['password'],database=db_config['dbname'])
        self.cursor=self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Users (mailid VARCHAR(255) PRIMARY KEY,password VARCHAR(256) NOT NULL,salt varbinary(255),name VARCHAR(255),address VARCHAR(255),phno VARCHAR(255));")
        self.db.commit()

    def add_user(self,user_json:json):
        salt=os.urandom(16)
        pwd=hashlib.sha256(user_json['password'].encode()+salt).hexdigest()
        self.cursor.execute("Insert into Users values (%s,%s,%s,%s,%s,%s)",(user_json['mailid'],pwd,salt,user_json['name'],user_json['address'],user_json['phno']))
        self.db.commit()
    def show_user(self,mailid:str) -> json:
        self.cursor.execute("Select * from Users where mailid=%s",(mailid,))
        user=self.cursor.fetchone() 
        result_dict = {
            "mailid": user[0],
            "name": user[3],
            "address": user[4],
            "phno": user[5]
            }
        return json.dumps(result_dict, indent=4)
    def del_user(self,mailid:str):
        self.cursor.execute("delete from Users where mailid=%s;",(mailid,))
        self.db.commit()
    def update_user(self,mailid,fieldname,fieldvalue):
        query="update users set {}=%s where mailid=%s;".format(fieldname)
        self.cursor.execute(query,(fieldvalue,mailid))
        self.db.commit()
    def reset_pass(self,mailid,password):
        self.cursor.execute("select salt from users where mailid=%s",(mailid,))
        salt=self.cursor.fetchone()[0]
        pwd=hashlib.sha256(password.encode()+salt).hexdigest()
        self.cursor.execute("update users set password=%s where mailid=%s;",(pwd,mailid))
        self.db.commit()
    def Auth(self,mailid,password):
        self.cursor.execute("select salt from users where mailid=%s",(mailid,))
        salt=self.cursor.fetchone()[0]
        pwd=hashlib.sha256(password.encode()+salt).hexdigest()
        self.cursor.execute("select password from users where mailid=%s;",(mailid,))
        if pwd in self.cursor.fetchone():
            return True
        else:
            return False
        
