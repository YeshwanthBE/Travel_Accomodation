import os
from flask import Flask,request,make_response,jsonify,render_template,url_for
from User import Profile
import uuid
app=Flask(__name__)

@app.route('/profile/<int:ap>/register',methods=['POST'])
def SignUp(ap):
    obj=Profile(os.getcwd()+'\\User_Profile\\Process_api\\config.yaml',ap)
    data=request.get_json()
    if obj.isexist(data['mailid']):
        return jsonify({"message": "Mailid already exists"}),400
    #obj.sendmail(app,data['mailid'],"Welcome to Oneyes Explora",render_template('registration.txt',username=data['mailid'].split('@')[0],loginlink="www.abc.com"))
    return obj.register(data).json(),201
    
@app.route('/profile/<int:ap>/<mailid>',methods=['GET','POST','DELETE','PATCH'])
def profile(ap,mailid):
    obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
    if obj.isexist(mailid) is False:
        return jsonify({"message": "User Not exist"}),400
    elif request.method=='GET':
        response=obj.showprofile(mailid)
        return response.json(),response.status_code
    elif request.method=='DELETE':
        pwd=request.get_json()['password']
        response=obj.deluser(mailid,pwd)
        return response.json(),response.status_code
    elif request.method=='POST':
        token=str(uuid.uuid4())
        url = url_for('tkauth', ap=ap, mailid=mailid, token=token)
        obj.settoken(mailid,token)
        #obj.sendmail(app,mailid,"password reset mail",render_template("resetmail.txt",username=str(mailid).split('@')[0],))
        return jsonify({"message":"Verification Mail sent"})
    else:
        data=request.get_json()
        response=obj.modifyuser(mailid,data)  
        return response.json(),response.status_code

@app.route('/profile/<int:ap>/<mailid>/auth',methods=['POST'])
def authentication(ap,mailid):
    obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
    if obj.isexist(mailid) is False:
        return jsonify({"message": "Invalid Mailid or password"}),401
    pwd=request.get_json()['password']
    response=obj.auth(mailid,pwd)
    return response.json(),response.status_code

@app.route('/profile/<int:ap>/<mailid>/<token>',methods=['POST'])
def tkauth(ap,mailid,token):
    obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
    resp=obj.rstpwd(mailid,token,request.get_json())
    if resp is False:
        return jsonify({"message": "Link Expired"}),401
    else:
        return resp.json(),resp.status_code
if __name__ == '__main__':
   app.run(debug = True,port=8080)  