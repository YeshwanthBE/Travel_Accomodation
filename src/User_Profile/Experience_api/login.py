from flask import Flask,render_template,url_for,request,flash,redirect,make_response,session
import requests
import json
import yaml
import os 
from datetime import date, timedelta,datetime
app=Flask(__name__)
app.static_folder = 'static'
with open(os.getcwd()+'\\src\\User_Profile\\Experience_api\\config.yaml', 'r') as file:
    global baseurl,config
    config=yaml.safe_load(file)
    baseurl= config['url']['domainurl']
    app.secret_key=config['app']['key']
@app.route('/')
def Homepage():
    query=request.args.get('Name')
    min_date=str(date.today()+timedelta(days=1))
    max_date=str(date.today()+timedelta(days=365))
    accommodation=json.loads(requests.get(baseurl+f'/showacms/',params=request.args).json())
    spb='usr' in request.cookies
    ap=json.loads(request.cookies.get("usr"))['ap'] if spb else None
    return render_template("homepage.html",admin=ap,show_profile_button=spb,accommodations=accommodation,query=query,length=len(accommodation),min_date=min_date,max_date=max_date)
@app.route('/signup/',methods=['GET','POST'])
def signup():
    if request.method=="GET":
        with open(app.static_folder+"\\json\\\states-and-districts.json", 'r') as file:
            data=json.loads(file.read())
        with open(app.static_folder + "\\json\\countries.json", 'r') as file:
            countries_data = json.loads(file.read())
        with open(app.static_folder + "\\json\\pincode.json", 'r', encoding='utf-8-sig') as file:
                pincode_data = json.loads(file.read())
        return render_template("signup.html",sdjson=data,cdjson=countries_data,pdjson=pincode_data)
    else:
        data={
        "mailid": request.form["mailid"],
        "password": request.form["password"],
        "name": request.form["name"],
        "address": request.form["address"]+","+request.form["district"]+"."+request.form["state"],
        "phno": request.form["phno"]
        }

        response=requests.post(baseurl+"/profile/0/register",json=data)
        flash(response.json())
        if response.status_code ==201:
            return redirect(url_for("login"))

@app.route("/login/",methods=['GET','POST'])
def login():
   if request.method=="GET":
        return render_template("login.html")
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
            return render_template("login.html",invalid=1)

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
@app.route("/modify/",methods=["POST"])
def mod():
    cred=json.loads(request.cookies.get("usr"))
    response=requests.patch(f'{baseurl}/profile/{cred["ap"]}/',headers={"Authorization": cred['jwt']},json=request.get_json())
    return response.json(),response.status_code

@app.route("/delete/",methods=['GET','POST'])
def delete():
    if request.method=="GET":
        return render_template("deleteaccount.html",user=request.args)
    else:
        data={"password": request.form["password"]}
        cred=json.loads(request.cookies.get("usr"))
        response=requests.delete(f'{baseurl}/profile/{cred["ap"]}/',headers={"Authorization": cred['jwt']},json=data)
        if response.status_code!=200:
            return render_template("deleteaccount.html",invalid=1,user=request.args)
        else:
            return logout()

@app.route('/adminprev/',methods=['POST'])
def promote():
    data={"mailid":request.form['mailid']}
    cred=json.loads(request.cookies.get("usr"))
    requests.post(f'{baseurl}/adminpriv/{cred["ap"]}/',headers={"Authorization": cred['jwt']},json=data)
    return redirect(url_for("admin"))

@app.route('/showusers/')
def showal():
    qp=request.args
    cred=json.loads(request.cookies.get("usr"))
    requests.get(f'{baseurl}/showusers/',headers={"Authorization": cred['jwt']},params=qp)
    render_template("showusers.html")

@app.route("/logout",methods=['POST'])
def logout():
    response=make_response(redirect(url_for("Homepage")))
    response.delete_cookie("usr")
    return response

@app.route("/booking/")
def booking():
    if 'usr' not in request.cookies:
        return redirect(url_for("login"))
    else:
        return redirect(config['url']['bookingurl']+f"/booking/?acmid={request.args.get('acmid')}")

@app.route("/Dashboard/",methods=['GET','POST'])    
def dashboard():
    if 'usr' not in request.cookies:
        return redirect(url_for("login"))
    cred=json.loads(request.cookies.get("usr"))
    header={"Authorization": cred['jwt']}
    user=json.loads(requests.get(f'{baseurl}/profile/{cred["ap"]}/',headers=header).json())
    prevbk=json.loads(requests.get(f"{config['url']['previousbkurl']}/pr/searchall/",headers=header,params={'ap':cred['ap']}).json())
    if request.method=='GET':
        return render_template("dashboard.html",user=user,prevbk=prevbk,length=len(prevbk),admin=cred['ap'])
    else:
        requests.delete(config['url']['previousbkurl']+"/pr/booking/",headers=header,params={"bid":request.form.get('bid')})
        return redirect(url_for("dashboard"))
    
@app.route("/admindashboard/")
def admin():
    if 'usr' not in request.cookies:
        return redirect(url_for("login"))
    cred=json.loads(request.cookies.get("usr"))
    header={"Authorization": cred['jwt']}
    acms=json.loads(requests.get(baseurl+f'/showacms/',headers=header,params={"isall":1}).json())
    allusers=json.loads(requests.get(baseurl+f'/showusers/',headers=header).json())
    return render_template("admindb.html",acms=acms,users=allusers)

@app.route("/admindashboard/showuser/",methods=['GET','POST'])
def usermod():
    if request.method=='GET':
        cred=json.loads(request.cookies.get("usr"))
        header={"Authorization": cred['jwt']}
        user=json.loads(requests.get(f'{baseurl}/userdetails/',headers=header,params=request.args).json())
        params={
            'ap':cred['ap'],
            'addb':1,
            'mailid':request.args.get('mailid')
        }
        prevbk=json.loads(requests.get(f"{config['url']['previousbkurl']}/pr/searchall/",headers=header,params=params).json())
        return render_template("addbusrprofile.html",user=user,prevbk=prevbk,length=len(prevbk),admin=cred['ap'])
@app.route("/acmreg/")
def acmreg():
    return redirect(config['url']['accomurl']+'/acm/register/')
@app.route("/admindashboard/acmmod/")
def acmmod():
    return redirect(config['url']['accomurl']+'/acmmod/?acmid='+request.args.get("acmid"))
if __name__ == '__main__':  
   app.run(debug = True,port=8081)  