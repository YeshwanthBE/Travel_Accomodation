import mysql.connector as mc
import hashlib
import yaml 
class User:
    def __init__(self,filepath):
        with open(filepath, 'r') as file:
            db_config= yaml.safe_load(file)    
            self.db = mc.connect(host=db_config['host'],user=dbconfig['user'],password=db_config['pwd'],database=db_config['db'])
        self.cursor=self.db.cursor()
        self.cursor.execute("""
                            Create Table if not exist userdata(mailid varchar(255) primary key,password varchar(10) not null
                            ,name varchar(255)),address varchar(255),phno varchar(255)""")
        
    def adduser(self,user_json):
        pwd=hashlib.sha256(user_json['pwd'].encode()).hexdigest()
        self.cursor.execute("Insert into Users values (%s,%s,%s,%s,%s,)",user_json['mailid'],pwd,user_json['name'],user_json['address'],user_json['phno'])
        self.db.commit()