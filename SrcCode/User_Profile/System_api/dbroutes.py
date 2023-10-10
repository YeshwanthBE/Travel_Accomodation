import os
from flask import Flask, request,make_response,jsonify
from UserDatabase import User
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
            algorithm="HS512" if kwargs.get('ap')==1 else "HS256"
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=algorithm)
            mailid = data['mailid']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.DecodeError:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(mailid, *args, **kwargs)
    return decorated

@app.route('/dbprofile/<int:ap>/Signup/',methods=['POST'])
def signup(ap):
    try:
        obj=User()
        obj.connect(os.getcwd()+"\\SrcCode\\User_Profile\\System_api\\config.yaml")
        if obj.add_user(request.get_json(),ap) is not False:
            return jsonify({"message": "User Registered Successfully"}), 201
        else:
            return jsonify({"message": "Mailid already exist"}), 401
    except Exception as e:
        return jsonify({"Exception": str(e)}),500

@app.route('/dbprofile/<int:ap>/',methods=['GET','POST','DELETE','PATCH'])
@token_required
def profile(mailid,ap):
    try:
        obj=User()
        obj.connect(os.getcwd()+"\\SrcCode\\User_Profile\\System_api\\config.yaml")
        if request.method=='GET':
            return jsonify(obj.show_user(mailid,ap))
        elif request.method=='DELETE':
            pwd=request.get_json()["password"]
            if not obj.Auth(mailid,pwd,ap):
                return jsonify({"message": "Invalid Password"}),401
            obj.del_user(mailid,ap)
            return jsonify({"message": "User Deleted Successfully"}), 200
        elif request.method=='POST':
            data=request.get_json()
            obj.reset_pass(mailid,data['password'],ap)
            return jsonify({"message": "Password Resetted Successfully"}), 200
        else:
            data=request.get_json()
            obj.update_user(mailid,data,ap)
            return jsonify({"message": "Profile Updated Successfully"}), 200  
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
@app.route('/dbprofile/<int:ap>/auth/',methods=['POST'])
def auth(ap):
    try:
        data=request.get_json()
        obj=User()
        obj.connect(os.getcwd()+"\\SrcCode\\User_Profile\\System_api\\config.yaml")
        if obj.Auth(data['mailid'],data['password'],ap):
            payload={"mailid": data['mailid'],
            "exp": int(time.time())+86400
            }
            algorithm="HS512" if ap else "HS256"
            token=jwt.encode(payload,app.config['SECRET_KEY'],algorithm=algorithm)
            return jsonify({"jwt":token}),200
        return jsonify({"message":"Invalid Mailid or password"}),401
    except Exception as e:
        return jsonify({"Exception": str(e)}),500

@app.route('/dbprofile/<int:ap>/tk/',methods=['GET','POST'])
def tokenauth(ap):
    try:
        obj=User()
        obj.connect(os.getcwd()+"\\SrcCode\\User_Profile\\System_api\\config.yaml")
        if request.method=='GET':
            mailid=request.args.get('mailid')
            payload={"mailid": mailid,
            "exp": int(time.time())+300
            }
            algorithm="HS512" if ap else "HS256"
            token=jwt.encode(payload,app.config['SECRET_KEY'],algorithm=algorithm)
            return jsonify({"token": obj.token(mailid),
                            "jwt": token})
        else:
            data=request.get_json()
            obj.token(data['mailid'],data['token'])
            return jsonify({}),200
    except Exception as e:
        return jsonify({"Exception": str(e)}),500

@app.route('/dbprofile/<int:ap>/promote/',methods=['POST'])
@token_required
def promote(mailid,ap):
    try:
        data=request.get_json()
        obj=User()
        obj.connect(os.getcwd()+"\\SrcCode\\User_Profile\\System_api\\config.yaml")
        obj.promote(data['mailid'])
        return jsonify({"message":"promoted as admin"}),200
    except Exception as e:
        return jsonify({"Exception": str(e)}),500

@app.route('/dbprofile/<int:ap>/showallusers/')
@token_required
def showall(mailid,ap):
    try:
        obj=User()
        obj.connect(os.getcwd()+"\\SrcCode\\User_Profile\\System_api\\config.yaml")
        data=request.args
        return jsonify(obj.showall(data.get('mailid'))),200
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
if __name__ == '__main__':
   app.run(debug = True)  