import os
from flask import Flask, request,make_response,jsonify
from Database import User

app=Flask(__name__) 

@app.route('/dbprofile/<int:ap>/Signup',methods=['POST'])
def signup(ap):
    obj=User(os.getcwd()+"\\User_Profile\\System_api\\config.yaml",ap)
    obj.add_user(request.get_json(),ap) 
    return jsonify({"message": "User Registered Successfully"}), 201

@app.route('/dbprofile/<int:ap>/<mailid>',methods=['GET','POST','DELETE','PATCH'])
def profile(mailid,ap):
    obj=User(os.getcwd()+"\\User_Profile\\System_api\\config.yaml",ap)
    if request.method=='GET':
        return jsonify(obj.show_user(mailid,ap))
    elif request.method=='DELETE':
        obj.del_user(mailid,ap)
        return jsonify({"message": "User Deleted Successfully"}), 200
    elif request.method=='POST':
        data=request.get_json()
        obj.reset_pass(mailid,data['newpwd'],ap)
        return jsonify({"message": "Password Resetted Successfully"}), 200
    else:
        data=request.get_json()
        obj.update_user(mailid,data,ap)
        return jsonify({"message": "Profile Updated Successfully"}), 200  
    
@app.route('/dbprofile/<int:ap>/<mailid>/exists')
def exists(mailid,ap):
    obj=User(os.getcwd()+"\\User_Profile\\System_api\\config.yaml",ap)
    if obj.isexists(mailid,ap) is True:
        return jsonify({'message':'mailid exists'}),200
    else:
        return jsonify({"message":'mailid not exists'}),404
    
@app.route('/dbprofile/<int:ap>/<mailid>/auth',methods=['POST'])
def auth(mailid,ap):
    obj=User(os.getcwd()+"\\User_Profile\\System_api\\config.yaml",ap)
    pwd=request.get_json().get('password')
    if obj.Auth(mailid,pwd,ap):
        return jsonify({"message":"Authentication Successful"}),200
    return jsonify({"message":"Invalid Mailid or password"}),401

@app.route('/dbprofile/<int:ap>/<mailid>/tk',methods=['GET','POST'])
def tokenauth(ap,mailid):
    obj=User(os.getcwd()+"\\User_Profile\\System_api\\config.yaml",ap)
    if request.method=='GET':
        return jsonify(obj.token(mailid))
    else:
        obj.token(mailid,request.args.get('token'))
        return jsonify({}),200

if __name__ == '__main__':
   app.run(debug = True)  