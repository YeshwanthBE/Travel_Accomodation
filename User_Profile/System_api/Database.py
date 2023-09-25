from datetime import datetime as dt,timedelta as td
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
        self.cursor.execute(f"delete from tverify where mailid=%s",(mailid,))
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
    
    def token(self,mailid,token=None):
        if token is not None:
            self.cursor.execute("Create table if not exists tverify (mailid varchar(255) primary key,token varchar(255),expiry datetime);")
            self.cursor.execute("select * from tverify where mailid=%s",(mailid,))
            expiry=dt.now()+td(hours=1)
            if self.cursor.fetchone() is None:
                self.cursor.execute("insert into tverify values(%s,%s,%s)",(mailid,token,expiry))
            else:
                self.cursor.execute("update tverify set token=%s,expiry=%s where mailid=%s",(token,expiry,mailid,))
            self.db.commit()
        else:
            self.cursor.execute("select token,expiry from tverify where mailid=%s",(mailid,))
            response=self.cursor.fetchone()
            if response is None:
                return response
            return json.dumps({"tk":response[0],"expiry":str(response[1])},indent=4)
        