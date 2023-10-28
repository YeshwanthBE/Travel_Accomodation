from flask import Flask,render_template,url_for,request,flash,redirect,make_response,send_from_directory
import requests
import json
import yaml
import os 
import uuid
app=Flask(__name__)
app.static_folder = 'static'
with open(os.getcwd()+'\\src\\Accomodations\\Experience_api\\config.yaml', 'r') as file:
    global baseurl
    config=yaml.safe_load(file)
    baseurl= config['url']['domainurl']
    app.secret_key=config['app']['key']
    upload_path=os.path.join(os.getcwd(), 'src','Accomodations','Experience_api','static', 'images')
@app.route('/acm/register/',methods=['GET','POST'])
def register():
    if request.method=="GET":
        admindburl="http://127.0.0.1:8081/admindashboard/"
        dashboardurl="http://127.0.0.1:8081/Dashboard/"
        with open(app.static_folder+"\\json\\\states-and-districts.json", 'r') as file:
            data=json.loads(file.read())
            return render_template("reg.html",db=dashboardurl,addb=admindburl,sdjson=data)
    else:
        cred=json.loads(request.cookies.get("usr"))
        if "image" in request.files:
            image_file = request.files["image"]
            unique_filename = str(uuid.uuid4()) + os.path.splitext(image_file.filename)[-1]
            full_path =os.path.join(upload_path , unique_filename)
            image_file.save(full_path)
            image_url = url_for("uploaded_file", filename=unique_filename, _external=True)
        else:
            image_url="Not Found"
        data={
        "mailid": request.form["mailid"],
        "name": request.form["name"],
        "description": request.form["description"],
        "location": request.form["address"]+","+request.form["district"]+"."+request.form["state"],
        "phno": request.form["phno"],
        "price": request.form["price"],
        "imgurl": image_url
        }
        response=requests.post(baseurl+"/register",json=data,headers={"Authorization": cred['jwt']})
        return redirect(config['url']['homepage']+'/admindashboard/')
        flash(response.json())
        if response.status_code ==200:
            redirect(url_for("show"))

@app.route("/acm/mod/",methods=['GET','DELETE','POST'])
def acm():

    if request.method=='GET':
        data=requests.get(f'{baseurl}/acm/op/',params=request.args)
        return data.json()
    elif request.method=='DELETE':
        cred=json.loads(request.cookies.get("usr"))
        requests.delete(f'{baseurl}/acm/op/',headers={"Authorization": cred['jwt']},params=request.args)
        return redirect(url_for("showall"))
    else:
        cred=json.loads(request.cookies.get("usr"))
        data=request.get_json()
        requests.patch(f'{baseurl}/acm/op/',headers={"Authorization": cred['jwt']},json=data,params=request.args)
        return redirect(url_for("acm"))

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory('static/images', filename)

@app.route("/searchall/")
def showall():
    data=requests.get(f"{baseurl}/acm/searchall",params=request.args)
    return data.json()
    #render_template("display.html",accomodations=data)

@app.route("/acmmod/")
def acmmod():
    acm=requests.get(f'{baseurl}/acm/op/',params=request.args).json()
    prevbk=json.loads(requests.get(f'{config["url"]["prevbkurl"]}/allacmbks',params={"acmid":request.args.get("acmid")}).json())
    return render_template("mod.html",acm=acm,prevbk=prevbk,length=len(prevbk))

@app.route('/home/<int:v>')
def home(v):
    url=config['url']['homepage']+('/admindashboard/' if v==1 else '/')
    return redirect(url)

if __name__ == '__main__':
   app.run(debug = True,port=8083)  