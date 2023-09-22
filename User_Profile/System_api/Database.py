import mysql.connector as mc
import hashlib
import yaml 
import json
import os
class User:
    def __init__(self,filepath,ap=0):
        table= "admin" if ap else "users"
        with open(filepath, 'r') as file:
            db_config= yaml.safe_load(file)['database']    
            self.db = mc.connect(host=db_config['host'],user=db_config['username'],password=db_config['password'],database=db_config['dbname'])
        self.cursor=self.db.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (mailid VARCHAR(255) PRIMARY KEY,password VARCHAR(256) NOT NULL,salt varbinary(255),name VARCHAR(255),address VARCHAR(255),phno VARCHAR(255));")
        self.db.commit()
        
    def isexists(self,mailid,ap=0):
        table= "admin" if ap else "users"
        self.cursor.execute(f"select mailid from {table} where mailid=%s",(mailid,))
        if self.cursor.fetchone() is None:
            return False
        return True
    
    def add_user(self,user_json:json,ap=0):
        table= "admin" if ap else "users"
        salt=os.urandom(16)
        pwd=hashlib.sha256(user_json['password'].encode()+salt).hexdigest()
        self.cursor.execute(f"Insert into {table} values (%s,%s,%s,%s,%s,%s)",(user_json['mailid'],pwd,salt,user_json['name'],user_json['address'],user_json['phno']))
        self.db.commit()

    def show_user(self,mailid:str,ap=0) -> json:
        table= "admin" if ap else "users"
        self.cursor.execute(f"Select * from {table} where mailid=%s",(mailid,))
        user=self.cursor.fetchone() 
        result_dict = {
            "mailid": user[0],
            "name": user[3],
            "address": user[4],
            "phno": user[5]
            }
        return json.dumps(result_dict, indent=4)
    
    def del_user(self,mailid:str,ap=0):
        table= "admin" if ap else "users"
        self.cursor.execute(f"delete from {table} where mailid=%s;",(mailid,))
        self.db.commit()

    def update_user(self,mailid,user_json,ap=0):
        table= "admin" if ap else "users"
        query="update {} set {}=%s,{}=%s,{}=%s where mailid=%s;".format(table,'name','address','phno')
        self.cursor.execute(query,(user_json['name'],user_json['address'],user_json['phno'],mailid))
        self.db.commit()

    def reset_pass(self,mailid,password,ap=0):
        table= "admin" if ap else "users"
        self.cursor.execute(f"select salt from {table} where mailid=%s",(mailid,))
        salt=self.cursor.fetchone()[0]
        pwd=hashlib.sha256(password.encode()+salt).hexdigest()
        self.cursor.execute(f"update {table} set password=%s where mailid=%s;",(pwd,mailid))
        self.db.commit()

    def Auth(self,mailid,password,ap=0):
        table= "admin" if ap else "users"
        self.cursor.execute(f"select salt from {table} where mailid=%s",(mailid,))
        salt=self.cursor.fetchone()[0]
        pwd=hashlib.sha256(password.encode()+salt).hexdigest()
        self.cursor.execute(f"select password from {table} where mailid=%s;",(mailid,))
        if pwd in self.cursor.fetchone():
            return True
        else:
            return False