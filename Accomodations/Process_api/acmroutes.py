import os
from flask import Flask,request,make_response,jsonify,render_template,url_for
from acmpro import acm
app=Flask(__name__)

@app.route('/register/',methods=['POST'])
def reg():
    try:
        obj=acm(os.getcwd()+'\\User_Profile\\Process_api\\config.yaml')
        data=request.get_json()
        #obj.sendmail(app,data['mailid'],"Welcome to Oneyes Explora",render_template('registration.txt',username=data['mailid'].split('@')[0],loginlink="www.abc.com"))
        jwt=request.headers.get('Authorization')
        response=obj.register(data,jwt)
        return jsonify(response.json()),response.status_code
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
@app.route('/acm/op/',methods=['GET','POST','DELETE','PATCH'])
def acmop():
    try:
        obj=acm(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml")
        jwt=request.headers.get('Authorization')
        if request.method=='GET':
            response=obj.showacm(jwt)
            return jsonify(response.json()),response.status_code
        elif request.method=='DELETE':
            response=obj.delacm(jwt)
            return jsonify(response.json()),response.status_code
        elif request.method=='POST':
            data=request.get_json()
            response=obj.register(data,jwt)
            #obj.sendmail(app,data['mailid'],"Welcome to Oneyes Explora",render_template('registration.txt',username=data['mailid'].split('@')[0],loginlink="www.abc.com"))
            return jsonify(response.json()),response.status_code
        else:
            data=request.get_json()
            response=obj.modifyacm(data,jwt)  
            return jsonify(response.json()),response.status_code
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
@app.route("/acm/searchall/")
def srchall():
    try:
         obj=acm(os.getcwd()+"\\User_Profile\\Process_api\\config.yaml")
         response=obj.searchacm(request.args)
         return jsonify(response.json()),response.statuscode
    except Exception as e:
         return jsonify({"Exception": str(e)}),500

if __name__ == '__main__':
   app.run(debug = True,port=8084)  