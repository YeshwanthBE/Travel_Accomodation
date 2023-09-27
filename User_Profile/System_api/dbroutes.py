import os
from flask import Flask, request,make_response,jsonify
from Database import User
from functools import wraps
import jwt
import time
app=Flask(__name__) 
app.config['SECRET_KEY']='a'
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            mailid = data['mailid']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.DecodeError:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(mailid, *args, **kwargs)
    return decorated

@app.route('/dbprofile/<int:ap>/Signup/',methods=['POST'])
def signup(ap):
    obj=User(os.getcwd()+"\\User_Profile\\System_api\\config.yaml",ap)
    if obj.add_user(request.get_json(),ap) is not False:
        return jsonify({"message": "User Registered Successfully"}), 201
    else:
        return jsonify({"message": "Mailid already exist"}), 401

@app.route('/dbprofile/<int:ap>/',methods=['GET','POST','DELETE','PATCH'])
@token_required
def profile(mailid,ap):
    obj=User(os.getcwd()+"\\User_Profile\\System_api\\config.yaml",ap)
    if request.method=='GET':
        return jsonify(obj.show_user(mailid,ap))
    elif request.method=='DELETE':
        obj.del_user(mailid,ap)
        return jsonify({"message": "User Deleted Successfully"}), 200
    elif request.method=='POST':
        data=request.get_json()
        obj.reset_pass(mailid,data['pwd'],ap)
        return jsonify({"message": "Password Resetted Successfully"}), 200
    else:
        data=request.get_json()
        obj.update_user(mailid,data,ap)
        return jsonify({"message": "Profile Updated Successfully"}), 200  
    
@app.route('/dbprofile/<int:ap>/auth/',methods=['POST'])
def auth(ap):
    data=request.get_json()
    obj=User(os.getcwd()+"\\User_Profile\\System_api\\config.yaml",ap)
    if obj.Auth(data['mailid'],data['pwd'],ap):
        payload={"mailid": data['mailid'],
         "exp": int(time.time())+86400
        }
        token=jwt.encode(payload,app.config['SECRET_KEY'],algorithm="HS256")
        return jsonify({"token":token}),200
    return jsonify({"message":"Invalid Mailid or password"}),401

@app.route('/dbprofile/<int:ap>/tk/',methods=['GET','POST'])
def tokenauth(ap):
    obj=User(os.getcwd()+"\\User_Profile\\System_api\\config.yaml",ap)
    if request.method=='GET':
        mailid=request.args.get('mailid')
        payload={"mailid": mailid,
         "exp": int(time.time())+300
        }
        token=jwt.encode(payload,app.config['SECRET_KEY'],algorithm="HS256")
        return jsonify({"token": obj.token(mailid),
                        "jwt": token})
    else:
        data=request.get_json()
        obj.token(data['mailid'],data['token'])
        return jsonify({}),200

if __name__ == '__main__':
   app.run(debug = True)  