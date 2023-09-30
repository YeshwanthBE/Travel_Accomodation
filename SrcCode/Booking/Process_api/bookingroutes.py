import os
from flask import Flask,request,make_response,jsonify,render_template,url_for
import requests
from booking import bking
app=Flask(__name__)

@app.route('/pr/booking/',methods=['GET','POST','DELETE'])
def bkop():
    try:
        obj=bking(os.getcwd()+"\\SrcCode\\Booking\\Process_api\\config.yaml")
        jwt=request.headers.get('Authorization')
        if request.method=='GET':
            response=obj.showbk(jwt,request.args)
            return jsonify(response.json()),response.status_code
        elif request.method=='DELETE':
            response=obj.delbk(jwt,request.args)
            return jsonify(response.json()),response.status_code
        else:
            data=request.get_json()
            response=obj.booking(data,jwt)
            #obj.sendmail(app,data['mailid'],"Welcome to Oneyes Explora",render_template('registration.txt',username=data['mailid'].split('@')[0],loginlink="www.abc.com"))
            return jsonify(response[0]),response[1]
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
@app.route("/pr/searchall/")
def srchall():
    try:
         obj=bking(os.getcwd()+"\\SrcCode\\Booking\\Process_api\\config.yaml")
         jwt=request.headers.get('Authorization')
         response=obj.searchbk(request.args,jwt)
         return jsonify(response.json()),response.status_code
    except Exception as e:
         return jsonify({"Exception": str(e)}),500

if __name__ == '__main__':
   app.run(debug = True,port=8085)  