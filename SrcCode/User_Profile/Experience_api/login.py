from flask import Flask,render_template,url_for,request,flash,redirect,make_response
import requests
import json
import yaml
import os 
app=Flask(__name__)
with open(os.getcwd()+'\\SrcCode\\User_Profile\\Experience_api\\config.yaml', 'r') as file:
    global baseurl
    config=yaml.safe_load(file)
    baseurl= config['url']['domainurl']
    app.secret_key=config['app']['key']
@app.route('/')
def Homepage():
    if request.cookies.get('usr'):
        render_template("index.html")
    else: 
        render_template("homepage.html")

@app.route('/signup/',methods=['GET','POST'])
def signup():
    if request.method=="GET":
        render_template("Sign_up.html")
    else:
        data={
        "mailid": request.form["mailid"],
        "password": request.form["password"],
        "name": request.form["name"],
        "address": request.form["address"],
        "phno": request.form["phno"]
        }
        response=requests.post(baseurl+"/profile/0/register",json=data)
        flash(response.json)
        if response.status_code ==200:
            redirect(url_for("login"))

@app.route("/login/",methods=['GET','POST'])
def login():
   if request.method=="GET":
        render_template("Login.html")
   else:
        data={
        "mailid": request.form["mailid"],
        "password": request.form["password"]
        }
        response=requests.post(baseurl+f"/profile/{request.args['ap']}/auth/",json=data)
        if response.status_code==200:
            res=make_response(redirect(url_for("Homepage")))
            ck=json.dumps({"jwt":response.json()["jwt"],"ap":request.args['ap']})
            res.set_cookie("usr",ck)
            return res
        else:
            flash(response.json())

@app.route("/acntrec/",methods=['GET','POST'])
def rstpwd():
    if request.method==['GET']:
        render_template("forgot.html")
    else:
        data={"mailid": request.form["mailid"],
                         "url": url_for("newpwd",_external=True)}
        flash(requests.post(baseurl+f"/profile/{request.args['ap']}/",json=data))

@app.route("/newpwd/",methods=['GET','POST'])
def newpwd():
    if request.method=="GET":
        data=request.args
        response=requests.get(f'{baseurl}/profile/{data["ap"]}/tk',params={"mailid": data["mailid"],"token": data["token"]})
        if response.status_code==200:
            render_template("newpd.html")
            resp=make_response({},200)
            ck=json.dumps({"jwt":response.json()["jwt"],"ap":data['ap']})
            resp.set_cookie("usr",ck)
            return resp 
        else:
            flash(response.json())
    else:
        data=json.loads(request.cookies.get("usr"))
        pwd={"password": request.form["password"]}
        resp=requests.post(baseurl+f'/profile/{data["ap"]}/rp/',headers={"Authorization": data["jwt"]},json=pwd)
        flash(resp.json())
        return redirect(url_for("login"))

@app.route("/profile/")
def show():
    cred=json.loads(request.cookies.get("usr"))
    data=requests.get(f'{baseurl}/profile/{cred["ap"]}/',headers={"Authorization": cred['jwt']})
    render_template("profile.html")
@app.route("/modify/",methods=["PATCH"])
def mod():
    cred=json.loads(request.cookies.get("usr"))
    data={
        "name": request.form["name"],
        "address": request.form["address"],
        "phno": request.form["phno"]
        }
    requests.patch(f'{baseurl}/profile/{cred["ap"]}/',headers={"Authorization": cred['jwt']},json=data)
    return redirect(url_for("show"))

@app.route("/delete/",methods=['DELETE'])
def delete():
    data={"password": request.form["password"]}
    cred=json.loads(request.cookies.get("usr"))
    requests.delete(f'{baseurl}/profile/{cred["ap"]}/',headers={"Authorization": cred['jwt']},json=data)
    response=make_response(redirect(url_for("Homepage")))
    response.delete_cookie("usr")
    return response

if __name__ == '__main__':
   app.run(debug = True,port=8081)  