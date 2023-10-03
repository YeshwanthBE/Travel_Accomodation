from datetime import datetime as dt,timedelta as td
import mysql.connector as mc
import hashlib
import yaml 
import json
import os
class User:
    def connect(self,filepath):
        try:
            with open(filepath, 'r') as file:
                db_config= yaml.safe_load(file)['database']    
                self.db = mc.connect(host=db_config['host'],user=db_config['username'],password=db_config['password'],database=db_config['dbname'])
            self.db.start_transaction()
            self.cursor=self.db.cursor()
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS admin (mailid VARCHAR(255) PRIMARY KEY,password VARCHAR(256) NOT NULL,salt varbinary(255),name VARCHAR(255),address VARCHAR(255),phno VARCHAR(255));")
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS users (mailid VARCHAR(255) PRIMARY KEY,password VARCHAR(256) NOT NULL,salt varbinary(255),name VARCHAR(255),address VARCHAR(255),phno VARCHAR(255));")
            self.cursor.execute("Create table if not exists tverify (mailid varchar(255) primary key,token varchar(255),expiry datetime);")
            self.db.commit()
        except Exception as e:
            if self.db:
                self.db.rollback()
            raise e
    
    def add_user(self,user_json:json,ap=0):
        try:
            self.db.start_transaction()
            table= "admin" if ap else "users"
            self.cursor.execute(f"select mailid from {table} where mailid=%s",(user_json['mailid'],))
            if self.cursor.fetchone() is not None:
                return False
            salt=os.urandom(16)
            pwd=hashlib.sha256(user_json['password'].encode()+salt).hexdigest()
            self.cursor.execute(f"Insert into {table} values (%s,%s,%s,%s,%s,%s)",(user_json['mailid'],pwd,salt,user_json['name'],user_json['address'],user_json['phno']))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def show_user(self,mailid:str,ap=0) -> json:
        try:
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
        except Exception as e:
            raise e
    
    def del_user(self,mailid:str,ap=0):
        try:
            self.db.commit()
            self.db.start_transaction()
            table= "admin" if ap else "users"
            self.cursor.execute(f'select * from {table} where mailid=%s for update',(mailid,))
            self.cursor.fetchone()
            self.cursor.execute(f"delete from {table} where mailid=%s;",(mailid,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def update_user(self,mailid,user_json,ap=0):
        try:
            self.db.start_transaction()
            table= "admin" if ap else "users"
            query="update {} set {}=%s,{}=%s,{}=%s where mailid=%s;".format(table,'name','address','phno')
            self.cursor.execute(f'select * from {table} where mailid=%s for update',(mailid,))
            self.cursor.execute(query,(user_json['name'],user_json['address'],user_json['phno'],mailid))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        
    def reset_pass(self,mailid,password,ap=0):
        try:
            self.db.start_transaction()
            table= "admin" if ap else "users"
            self.cursor.execute(f"select salt from {table} where mailid=%s",(mailid,))
            salt=self.cursor.fetchone()[0]
            pwd=hashlib.sha256(password.encode()+salt).hexdigest()
            self.cursor.execute(f"update {table} set password=%s where mailid=%s;",(pwd,mailid))
            self.cursor.execute(f"delete from tverify where mailid=%s",(mailid,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        
    def Auth(self,mailid,password,ap=0):
        try:
            table= "admin" if ap else "users"
            self.cursor.execute(f"select salt from {table} where mailid=%s",(mailid,))
            salt=self.cursor.fetchone()[0]
            pwd=hashlib.sha256(password.encode()+salt).hexdigest()
            self.cursor.execute(f"select password from {table} where mailid=%s;",(mailid,))
            if pwd in self.cursor.fetchone():
                return True
            else:
                return False
        except Exception as e:
            raise e

    def token(self,mailid,token=None):
        try:
            if token is not None:
                self.cursor.execute("select * from tverify where mailid=%s",(mailid,))
                expiry=dt.now()+td(hours=1)
                if self.cursor.fetchone() is None:
                    self.cursor.execute("insert into tverify values(%s,%s,%s)",(mailid,token,expiry))
                else:
                    self.cursor.execute("update tverify set token=%s,expiry=%s where mailid=%s",(token,expiry,mailid,))
                self.cursor.execute("delete from tverify where expiry<%s",(dt.now(),))
                self.db.commit()
            else:
                self.cursor.execute("select token,expiry from tverify where mailid=%s",(mailid,))
                response=self.cursor.fetchone()
                if response is None:
                    return response
                return json.dumps({"tk":response[0],"expiry":str(response[1])},indent=4)
        except Exception as e:
            raise e
    
    def promote(self,mailid):
        try:
            self.db.start_transaction()
            self.cursor.execute(f'INSERT INTO admin select * from users where mailid=%s',(mailid,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
    
    def showall(self,mailid=None):
        try:
            if mailid:
                return self.show_user(mailid)
            self.cursor.execute("select mailid,name from users")
            lst=[]
            for user in self.cursor.fetchall():
                result_dict = {
                    "mailid": user[0],
                    "name": user[1],
                    }
                lst.append(result_dict)
            return json.dumps(lst, indent=4)
        except Exception as e:
            raise e