import mysql.connector as mc
import yaml 
import json
import os
class acm:
    def connect(self,filepath):
        try:
            with open(filepath, 'r') as file:
                db_config= yaml.safe_load(file)['database']    
                self.db = mc.connect(host=db_config['host'],user=db_config['username'],password=db_config['password'],database=db_config['dbname'])
            self.db.start_transaction()
            self.cursor=self.db.cursor()
            self.cursor.execute("CREATE TABLE if not exists accommodations (mailid varchar(20) PRIMARY KEY, name VARCHAR(255) NOT NULL, description TEXT, location VARCHAR(255), phno varchar(20), price DECIMAL(10, 2), rating FLOAT, image_url VARCHAR(255));")
            self.db.commit()
        except Exception as e:
            if self.db:
                self.db.rollback()
            raise e
    
    def add_acm(self,Inn_json:json):
        try:
            self.db.start_transaction()
            self.cursor.execute("select mailid from accommodations where mailid=%s",(Inn_json['mailid'],))
            if self.cursor.fetchone() is not None:
                return False
            self.cursor.execute("Insert into accommodations values (%s,%s,%s,%s,%s,%s,%s,%s)",(Inn_json['mailid'],Inn_json['name'],Inn_json['description'],Inn_json['location'],Inn_json['phno'],Inn_json['price'],None,Inn_json['imgurl']))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def show_acm(self,mailid:str) -> json:
        try:
            self.cursor.execute("Select * from accommodations where mailid=%s",(mailid,))
            acm=self.cursor.fetchone() 
            if acm is None:
                return json.dumps({"Message" : "accommodations Not found"})
            result_dict = {
                "mailid": acm[0],
                "name": acm[1],
                "description": acm[2],
                "location": acm[3],
                "phno": acm[4],
                "price": acm[5],
                "rating": acm[6],
                "imgurl": acm[7]
                }
            return result_dict
        except Exception as e:
            raise e
    
    def del_acm(self,mailid:str):
        try:
            self.db.start_transaction()
            self.cursor.execute(f'select * from accommodations where mailid=%s for update',(mailid,))
            self.cursor.fetchone()
            self.cursor.execute(f"delete from accommodations where mailid=%s;",(mailid,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def update_acm(self,mailid,Inn_json):
        try:
            self.db.start_transaction()
            self.cursor.execute(f'select * from accommodations where mailid=%s for update',(mailid,))
            self.cursor.fetchone()
            for i in Inn_json:
                self.cursor.execute(f"update accommodations set {i}=%s where mailid=%s",(Inn_json[i],mailid))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
    
    def searchacm(self,location,minp,maxp,sort,desc):
        try:
            query=f"select name,description from accommodations where price>{minp}"
            if maxp:
                query+=f' and price<{maxp}'
            if location:
                query+=f' and location="{location}"'
            if sort:
                query+=f' order by {sort}'
            if desc:
                query+=' desc;'
            else:
                query+=';'
            self.cursor.execute(query)
            lst=[]
            for i in self.cursor.fetchall():
                lst.append({i[0]:i[1]})
            return(json.dumps(lst))
        except Exception as e:
            raise e

