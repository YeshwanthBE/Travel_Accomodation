from flask import Flask,render_template,url_for,request,flash,redirect,make_response
import requests
import json
import yaml
import os 
import uuid
app=Flask(__name__)
with open(os.getcwd()+'\\SrcCode\\Booking\\Experience_api\\config.yaml', 'r') as file:
    global baseurl,config
    config=yaml.safe_load(file)
    baseurl= config['url']['domainurl']
    app.secret_key=config['app']['key']

@app.route('/booking/',methods=['GET','POST'])
def register():
    if request.method=="GET":
         acm=requests.get(config['url']['acmurl']+"/acm/mod/",params=request.args).json()
         reviews=requests.get(config['url']['revurl']+"/reviews/",params=request.args).json()
         return render_template("booking.html",acm=acm,reviews=reviews)
    else:
        cred=json.loads(request.cookies.get("usr"))
        qp=request.args
        data={
        "acmid": qp.get('acmid'),
        "checkin": request.form["checkin"],
        "checkout": request.form["checkout"],
        }
        response=requests.post(baseurl+"/pr/booking/",json=data,headers={"Authorization": cred['jwt']})
        flash(response.json())
        if response.status_code ==200:
            redirect(url_for("show"))

@app.route("/prevbooking/",methods=['GET','DELETE'])
def bkg():
    cred=json.loads(request.cookies.get("usr"))
    if request.method=='GET':
        data=requests.get(f'{baseurl}/pr/booking/',headers={"Authorization": cred['jwt']},params=request.args)
        render_template("booking.html")
    else:
        requests.delete(f'{baseurl}/pr/booking/',headers={"Authorization": cred['jwt']},params=request.args)
        return redirect(url_for("showall"))

@app.route("/searchall/")
def showall():
    cred=json.loads(request.cookies.get("usr"))
    data=requests.get(f"{baseurl}/pr/searchall/",headers={"Authorization": cred['jwt']})
    render_template("display.html",json=data)
    
if __name__ == '__main__':
   app.run(debug = True,port=8093)  