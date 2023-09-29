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
            self.cursor.execute("CREATE TABLE accommodations (mailid varchar(20) PRIMARY KEY, name VARCHAR(255) NOT NULL, description TEXT, location VARCHAR(255), phno varchar(20), price DECIMAL(10, 2), rating FLOAT, image_url VARCHAR(255));")
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
            self.cursor.execute("Insert into accommodations values (%s,%s,%s,%s,%s,%s,%s,%s)",(Inn_json['mailid'],Inn_json['name'],Inn_json['decription'],Inn_json['location'],Inn_json['phno'],Inn_json['price'],None,Inn_json['imgurl']))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def show_acm(self,mailid:str) -> json:
        try:
            self.cursor.execute("Select * from accommodations where mailid=%s",(mailid,))
            acm=self.cursor.fetchone() 
            result_dict = {
                "mailid": acm[0],
                "name": acm[1],
                "decription": acm[2],
                "location": acm[3],
                "phno": acm[4],
                "price": acm[5],
                "rating": acm[6],
                "imgurl": acm[7]
                }
            return json.dumps(result_dict, indent=4)
        except Exception as e:
            raise e
    
    def del_acm(self,mailid:str):
        try:
            self.db.start_transaction()
            self.cursor.execute(f'select * from accomodations where mailid=%s for update',(mailid,))
            self.cursor.execute(f"delete from accomotaions where mailid=%s;",(mailid,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def update_acm(self,mailid,Inn_json):
        try:
            self.db.start_transaction()
            self.cursor.execute(f'select * from accomotaions where mailid=%s for update',(mailid,))
            for i in Inn_json:
                self.cursor.execute(f"update accomotaions set {i}={Inn_json[i]} where mailid=%s",(mailid,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
    
    def searchacm(self,location=None,minp=None,maxp=None,sort=None,desc=False):
        try:
            query=f"select name,description from accomotaions where location={location},price>{minp}"
            if maxp is not None:
                query+=f' and price<{maxp}'
            if sort is not None:
                query+=f' order by {sort}'
            if desc:
                query+=' desc'
            else:
                query+=';'
            self.cursor.execute(query)
            lst=[]
            for i in self.cursor.fetchall():
                lst.append({i[0]:i[1]})
            return(json.dumps(lst))
        except Exception as e:
            raise e

