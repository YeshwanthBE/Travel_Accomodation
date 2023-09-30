from datetime import datetime as dt,timedelta as td
import mysql.connector as mc
import hashlib
import yaml 
import json
import os
class rr:
    def connect(self,filepath):
        try:
            with open(filepath, 'r') as file:
                db_config= yaml.safe_load(file)['database']    
                self.db = mc.connect(host=db_config['host'],user=db_config['username'],password=db_config['password'],database=db_config['dbname'])
            self.db.start_transaction()
            self.cursor=self.db.cursor()
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS reviews (review_id INT AUTO_INCREMENT PRIMARY KEY, userid VARCHAR(255), acmid VARCHAR(255), rating DECIMAL(3, 2), review TEXT, datetime DATETIME, FOREIGN KEY (userid) REFERENCES users(mailid), FOREIGN KEY (acmid) REFERENCES accommodations(mailid));")
            self.db.commit()
        except Exception as e:
            if self.db:
                self.db.rollback()
            raise e
    
    def add(self,mailid,rr_json:json):
        try:
            self.db.start_transaction()
            current_datetime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(f"Insert into reviews (acmid, userid, rating, review, datetime) values(%s,%s,%s,%s,%s)",(rr_json['acmid'],mailid,rr_json['rating'],rr_json['review'],current_datetime))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def mod(self,rr_json:json) :
        try:
            self.db.start_transaction()
            self.cursor.execute(f"update reviews set rating=%s,review=%s where review_id=%s",(rr_json['rating'],rr_json['review'],rr_json['rid']))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
    
    def delete(self,rid):
        try:
            self.db.start_transaction()
            self.cursor.execute(f"Select * from reviews where review_id=%s for update",(rid,))
            self.cursor.fetchone() 
            self.cursor.execute(f"delete from reviews where review_id=%s",(rid,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def showall(self,rr_json):
        try:
            query=f'select * from reviews where acmid=%s order by {rr_json["sort"]}'
            if not rr_json.get('asc'):
                query+=" desc;"
            self.cursor.execute(query,(rr_json['acmid'],))
            lst=[]
            for i in self.cursor.fetchall():
                result_dict = {
                "reviewid": i[0],
                "userid": i[1],
                "acmid": i[2],
                "rating": float(i[3]),
                "review": i[4],
                "datetime": str(i[5])
                }
                lst.append(result_dict)
            print(lst)
            return(json.dumps(lst))
        except Exception as e:
            print(e)
            raise e
