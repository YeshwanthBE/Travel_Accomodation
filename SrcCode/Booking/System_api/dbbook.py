from datetime import datetime as dt,timedelta as td
import mysql.connector as mc
import hashlib
import yaml 
import json
import os
class bk:
    def connect(self,filepath):
        try:
            with open(filepath, 'r') as file:
                db_config= yaml.safe_load(file)['database']    
                self.db = mc.connect(host=db_config['host'],user=db_config['username'],password=db_config['password'],database=db_config['dbname'])
            self.db.start_transaction()
            self.cursor=self.db.cursor()
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS bookings (booking_id INT AUTO_INCREMENT PRIMARY KEY, acmid VARCHAR(255), userid VARCHAR(255), booking_date DATETIME, price DECIMAL(10, 2),checkin date,checkout date, FOREIGN KEY (acmid) REFERENCES accommodations(mailid), FOREIGN KEY (userid) REFERENCES users(mailid));")
            self.db.commit()
        except Exception as e:
            if self.db:
                self.db.rollback()
            raise e
    
    def booking(self,mailid,bk_json:json):
        try:
            self.db.start_transaction()
            self.cursor.execute(f"select * from bookings where ((%s between checkin and checkout) or (%s between checkin and checkout)) and acmid=%s",(bk_json['checkin'],bk_json['checkout'],bk_json['acmid']))
            if self.cursor.fetchone() is not None:
                return False
            current_datetime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(f"Insert into bookings (acmid, userid, booking_date, price, checkin, checkout) values(%s,%s,%s,%s,%s,%s)",(bk_json['acmid'],mailid,current_datetime,bk_json['price'],bk_json['checkin'],bk_json['checkout']))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def show_bk(self,bid:str) -> json:
        try:
            self.cursor.execute(f"Select * from bookings where booking_id=%s",(bid,))
            bk=self.cursor.fetchone() 
            result_dict = {
                "bookingid": bk[0],
                "acmid": bk[1],
                "userid": bk[2],
                "booking_date": str(bk[3]),
                "price": float(bk[4]),
                "checkin": str(bk[5]),
                "checkout": str(bk[6])
                }
            return json.dumps(result_dict, indent=4)
        except Exception as e:
            raise e
    
    def del_bk(self,bid:str):
        try:
            self.db.start_transaction()
            self.cursor.execute(f'select * from bookings where booking_id=%s for update',(bid,))
            self.cursor.fetchall()
            self.cursor.execute(f"delete from bookings where booking_id=%s",(bid,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def showallbk(self,userid):
        try:
            self.cursor.execute(f'select * from bookings where userid=%s order by booking_date desc',(userid,))
            lst=[]
            for i in self.cursor.fetchall():
                result_dict = {
                "bookingid": i[0],
                "acmid": i[1],
                "userid": i[2],
                "booking_date": str(i[3]),
                "price": float(i[4]),
                "checkin": str(i[5]),
                "checkout": str(i[6])
                }
                lst.append(result_dict)
            return(json.dumps(lst))
        except Exception as e:
            raise e

    def showallacmbk(self,acmid):
        try:
            self.cursor.execute('select checkin,checkout from bookings where acmid=%s',(acmid,))
            lst=[]
            for i in self.cursor.fetchall():
                result_dict = {
                "checkin": str(i[0]),
                "checkout": str(i[1])
                }
                lst.append(result_dict)
            return(json.dumps(lst))
        except Exception as e:
            raise e
    
    def getacms(self,checkin,checkout):
        try:
            self.cursor.execute('select acmid from bookings where %s>checkout or %s<checkin',(checkin,checkout))
            return json.dumps({"acmid":self.cursor.fetchall()})
        except Exception as e:
            raise e