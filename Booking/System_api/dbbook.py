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
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS bookings (booking_id INT AUTO_INCREMENT PRIMARY KEY, acmid VARCHAR(255), userid VARCHAR(255), booking_date DATETIME, price DECIMAL(10, 2),checkin date,checkout date, FOREIGN KEY (accommodation_mailid) REFERENCES accommodations(mailid), FOREIGN KEY (user_mailid) REFERENCES users(mailid));")
            self.db.commit()
        except Exception as e:
            if self.db:
                self.db.rollback()
            raise e
    
    def booking(self,bk_json:json):
        try:
            self.db.start_transaction()
            self.cursor.execute(f"select %s from bookings where (%s between checkin and checkout) or (%s between checkin and checkout)",(bk_json['checkin'],bk_json['checkout']))
            if self.cursor.fetchone() is not None:
                return False
            self.cursor.execute(f"Insert into bookings values (%s,%s,%s,%s,%s,%s)",(bk_json['acmid'],bk_json['userid'],dt.now(),bk_json['price'],bk_json['checkin'],bk_json['checkout']))
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
                "booking_date": bk[3],
                "price": bk[4],
                "checkin": bk[5],
                "checkout": bk[6]
                }
            return json.dumps(result_dict, indent=4)
        except Exception as e:
            raise e
    
    def del_bk(self,bid:str):
        try:
            self.db.start_transaction()
            self.cursor.execute(f'select * from booking where booking_id=%s for update',(bid,))
            self.cursor.execute(f"delete from booking_id where booking_id=%s",(bid,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def showallbk(self,userid):
        try:
            self.cursor.execute(f'select * from booking where userid=%s order by booking_date desc',(userid,))
            lst=[]
            for i in self.cursor.fetchall():
                result_dict = {
                "bookingid": i[0],
                "acmid": i[1],
                "userid": i[2],
                "booking_date": i[3],
                "price": i[4],
                "checkin": i[5],
                "checkout": i[6]
                }
                lst.append(result_dict)
            return(json.dumps(lst))
        except Exception as e:
            raise e
