import os
from flask import Flask,request,make_response,jsonify
from User import Profile
app=Flask(__name__)

@app.route('/profile/<int:ap>/register',methods=['POST'])
def SignUp(ap):
    obj=Profile(os.getcwd()+'\\User_Profile\\Process_api\\config.yaml',ap)
    if obj.isexist(request.get_json()['mailid']):
        return jsonify({"message": "Mailid already exists"}),400
    return obj.register(request.get_json()),200

@app.route('/profile/<int:ap>/<mailid>',methods=['GET','POST','DELETE','PATCH'])
def profile(ap,mailid):
    obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
    if obj.isexist(request.get_json()['mailid']) is False:
        return jsonify({"message": "User Not exist"}),400
    elif request.method=='GET':
        return jsonify(obj.showprofile(mailid)),200
    elif request.method=='DELETE':
        pwd=request.get_json()['password']
        return jsonify(obj.deluser(mailid,pwd))
    else:
        data=request.get_json()
        return jsonify(obj.modifyuser(mailid,data)), 200  

@app.route('/profile/<int:ap>/<mailid>/auth',methods=['POST'])
def authentication(ap,mailid):
    obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
    if obj.isexist(mailid) is False:
        return jsonify({"message": "Invalid Mailid or password"}),401
    pwd=request.get_json()['password']
    return jsonify(obj.auth(mailid,pwd)),200

if __name__ == '__main__':
   app.run(debug = True)  