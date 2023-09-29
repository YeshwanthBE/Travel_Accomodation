import os
from flask import Flask, request,make_response,jsonify
from InnDatabase import acm
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
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS512")
            mailid = data['mailid']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.DecodeError:
            return jsonify({'message': 'Token is invalid'}), 401
        except:
            return  jsonify({'message': 'Token error'}), 500
        return f(mailid, *args, **kwargs)
    return decorated

@app.route('/acm/ad/',methods=['GET','POST','DELETE','PATCH'])
@token_required
def acmtools(mailid):
    try:
        obj=acm()
        obj.connect(os.getcwd()+"\\Accomodations\\System_api\\config.yaml")
        if request.method=='GET':
            return jsonify(obj.show_acm(mailid))
        elif request.method=='DELETE':
            obj.del_acm(mailid)
            return jsonify({"message": "Accomodation Deleted Successfully"}), 200
        elif request.method=='POST':
            if obj.add_acm(request.get_json()) is not False:
                return jsonify({"message": "accommodation Registered Successfully"}), 201
            else:
                return jsonify({"message": "accommodation already exist"}), 401
        else:
            data=request.get_json()
            obj.update_acm(mailid,data)
            return jsonify({"message": "Accomodation Updated Successfully"}), 200  
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
@app.route('/acm/')
def srch():
    try:
        obj=acm()
        obj.connect(os.getcwd()+"\\Accomodations\\System_api\\config.yaml")
        data=request.args
        return jsonify(obj.searchacm(data.get("location"),data.get('minp'),data.get('maxp'),data.get('sort'),data.get('desc'))),200
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
if __name__ == '__main__':
   app.run(debug = True,port=8082)  