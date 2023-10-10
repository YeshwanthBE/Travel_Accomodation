import os
from flask import Flask, request,make_response,jsonify
from dbbook import bk
from functools import wraps
import jwt
app=Flask(__name__) 
app.config['SECRET_KEY']='a'
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            algorithm="HS256" if request.args.get('ap') else "HS512"
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=algorithm)
            mailid = data['mailid']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.DecodeError:
            return jsonify({'message': 'Token is invalid'}), 401
        except:
            return  jsonify({'message': 'Unauthorized'}), 401
        return f(mailid,*args, **kwargs)
    return decorated

@app.route('/dbbk/',methods=['GET','POST','DELETE'])
@token_required
def booking(mailid):
    try:
        obj=bk()
        qp=request.args
        obj.connect(os.getcwd()+"\\SrcCode\\Booking\\System_api\\config.yaml")
        if request.method=='GET':
            return jsonify(obj.show_bk(qp.get('bid')))
        elif request.method=='DELETE':
            obj.del_bk(qp.get('bid'))
            return jsonify({"message": "booking Cancelled Successfully"}), 200
        else:
            if obj.booking(mailid,request.get_json()) is not False:
                return jsonify({"message": "booked Successfully"}), 201
            else:
                return jsonify({"message": "Booking Failed"}), 401 
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
@app.route('/dbbk/allbk/')
@token_required
def show(mailid):
    try:
        obj=bk()
        obj.connect(os.getcwd()+"\\SrcCode\\Booking\\System_api\\config.yaml")
        return jsonify(obj.showallbk(mailid)),200
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
@app.route('/dbbk/acmbks/')
def acmbk():
    try:
        obj=bk()
        obj.connect(os.getcwd()+"\\SrcCode\\Booking\\System_api\\config.yaml")
        return jsonify(obj.showallacmbk(request.args.get('acmid'))),200
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
@app.route('/dbbk/acms/')
def acms():
    try:
        obj=bk()
        obj.connect(os.getcwd()+"\\SrcCode\\Booking\\System_api\\config.yaml")
        return jsonify(obj.getacms(request.args.get('checkin'),request.args.get('checkout'))),200
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
if __name__ == '__main__':
   app.run(debug = True,port=8090)  