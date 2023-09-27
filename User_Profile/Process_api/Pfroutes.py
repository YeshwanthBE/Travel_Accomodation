import os
from flask import Flask,request,make_response,jsonify,render_template,url_for
from User import Profile
import uuid
app=Flask(__name__)

@app.route('/profile/<int:ap>/register',methods=['POST'])
def SignUp(ap):
    obj=Profile(os.getcwd()+'\\User_Profile\\Process_api\\config.yaml',ap)
    data=request.get_json()
    #obj.sendmail(app,data['mailid'],"Welcome to Oneyes Explora",render_template('registration.txt',username=data['mailid'].split('@')[0],loginlink="www.abc.com"))
    response=obj.register(data)
    return response.json(),response.status_code
    
@app.route('/profile/<int:ap>/',methods=['GET','POST','DELETE','PATCH'])
def profile(ap):
    obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
    jwt=request.headers.get('Authorization')
    if request.method=='GET':
        response=obj.showprofile(jwt)
        return response.json(),response.status_code
    elif request.method=='DELETE':
        pwd=request.get_json()['password']
        response=obj.deluser(jwt)
        return response.json(),response.status_code
    elif request.method=='POST':
        token=str(uuid.uuid4())
        data=request.get_json()
        url = url_for('tkauth',ap=ap,mailid=data['mailid'],token=token,external=True)
        obj.settoken(data['mailid'],token)
        #obj.sendmail(app,mailid,"password reset mail",render_template("resetmail.txt",username=str(mailid).split('@')[0],))
        return jsonify({"message":"Password Reset Mail Sent"})
    else:
        data=request.get_json()
        response=obj.modifyuser(data,jwt)  
        return response.json(),response.status_code

@app.route('/profile/<int:ap>/auth/',methods=['POST'])
def authentication(ap):
    obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
    response=obj.auth(request.get_json())
    return response.json(),response.status_code

@app.route('/profile/<int:ap>/tk/')
def tkauth(ap):
    obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
    data=request.args
    resp=obj.verifytk(data["mailid"],data["token"],request.get_json())
    if resp is False:
        return jsonify({"message": "Link Expired"}),401
    else:
        return resp

@app.route('/profile/<int:ap>/rp/',methods=['POST'])
def rp(ap):
    obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
    jwt=request.headers.get('Authorization')
    return obj.rstpwd(request.get_json(),jwt).json()
    
if __name__ == '__main__':
   app.run(debug = True,port=8080)  