import os
from flask import Flask, request,make_response,jsonify
from Database import User

app=Flask(__name__) 
obj=User(os.getcwd()+"\\User_Profile\\System_api\\config.yaml")

@app.route('/profile/Signup/<int:ap>',methods=['POST'])
def signup(ap):
    obj.add_user(request.get_json(),ap)
    response_data = {"message": "User Registered Successfully"}
    return jsonify(response_data), 201

@app.route('/profile/<mailid>/<int:ap>',methods=['GET','POST','DELETE','PATCH'])
def profile(mailid,ap):
    if request.method=='GET':
        return jsonify(obj.show_user(mailid,ap))
    elif request.method=='DELETE':
        obj.del_user(mailid,ap)
        response_data = {"message": "User Deleted Successfully"}
        return jsonify(response_data), 204
    elif request.method=='POST':
        data=request.get_json()
        obj.reset_pass(mailid,data['newpwd'],ap)
        response_data = {"message": "Password Resetted Successfully"}
        return jsonify(response_data), 200
    else:
        data=request.get_json()
        obj.update_user(mailid,data,ap)
        response_data = {"message": "Profile Updated Successfully"}
        return jsonify(response_data), 200  
    
@app.route('/profile/<mailid>/<int:ap>/exists')
def exists(mailid,ap):
    if obj.isexists(mailid,ap) is True:
        return jsonify({'message':'mailid exists'}),200
    else:
        return jsonify({"message":'mailid not exists'}),404
    
@app.route('/profile/<mailid>/<int:ap>/auth',methods=['POST'])
def auth(mailid,ap):
    pwd=request.get_json().get('password')
    if obj.Auth(mailid,pwd,ap):
        return jsonify({"message":"Authentication Successful"}),200
    return jsonify({"message":"Invalid Mailid or password"}),401

if __name__ == '__main__':
   app.run(debug = True)  