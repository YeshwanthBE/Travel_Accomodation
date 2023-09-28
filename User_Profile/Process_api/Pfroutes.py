import os
from flask import Flask,request,make_response,jsonify,render_template,url_for
from User import Profile
import uuid
app=Flask(__name__)

@app.route('/profile/<int:ap>/register',methods=['POST'])
def SignUp(ap=0):
    try:
        obj=Profile(os.getcwd()+'\\User_Profile\\Process_api\\config.yaml',ap)
        data=request.get_json()
        #obj.sendmail(app,data['mailid'],"Welcome to Oneyes Explora",render_template('registration.txt',username=data['mailid'].split('@')[0],loginlink="www.abc.com"))
        response=obj.register(data)
        return jsonify(response.json()),response.status_code
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
@app.route('/profile/<int:ap>/',methods=['GET','POST','DELETE','PATCH'])
def profile(ap):
    try:
        obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
        jwt=request.headers.get('Authorization')
        if request.method=='GET':
            response=obj.showprofile(jwt)
            return jsonify(response.json()),response.status_code
        elif request.method=='DELETE':
            pwd=request.get_json()
            jwt=request.headers.get('Authorization')
            response=obj.deluser(jwt,pwd)
            return jsonify(response.json()),response.status_code
        elif request.method=='POST':
            token=str(uuid.uuid4())
            data=request.get_json()
            url=data['url']+f'?ap={ap}&mailid={data["mailid"]}&token={token}'
            obj.settoken(data['mailid'],token)
            #obj.sendmail(app,mailid,"password reset mail",render_template("resetmail.txt",username=str(mailid).split('@')[0],url=url))
            return jsonify({"message":"Password Reset Mail Sent"})
        else:
            data=request.get_json()
            response=obj.modifyuser(data,jwt)  
            return jsonify(response.json()),response.status_code
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
@app.route('/profile/<int:ap>/auth/',methods=['POST'])
def authentication(ap) ->make_response:
    try:
        obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
        response=obj.auth(request.get_json())
        return jsonify(response.json()),response.status_code
    except Exception as e:
        return jsonify({"Exception": str(e)}),500

@app.route('/profile/<int:ap>/tk/')
def tkauth(ap)-> make_response:
    try:
        obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
        data=request.args
        jwt=obj.verifytk(data.get("mailid"),data.get("token"))
        if jwt is False:
            return jsonify({"message": "Link Expired"}),401
        else:
            return jsonify({"jwt": jwt}),200
    except Exception as e:
        return jsonify({"Exception": str(e)}),500

@app.route('/profile/<int:ap>/rp/',methods=['POST'])
def rp(ap):
    try:
        obj=Profile(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml",ap)
        jwt=request.headers.get('Authorization')
        response=obj.rstpwd(request.get_json(),jwt)
        return jsonify(response.json()),response.status_code
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
if __name__ == '__main__':
   app.run(debug = True,port=8080)  