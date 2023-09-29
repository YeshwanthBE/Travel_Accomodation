from flask import Flask,render_template,url_for,request,flash,redirect,make_response
import requests
import json
import yaml
import os 
import uuid
app=Flask(__name__)
with open(os.getcwd()+'\\Accomodations\\Experience_api\\config.yaml', 'r') as file:
    global baseurl
    config=yaml.safe_load(file)
    baseurl= config['url']['domainurl']
    app.secret_key=config['app']['key']
    upload_path=os.path.join(os.path.join(os.getcwd(), "images","Accomodations"))
@app.route('/acm/register/',methods=['GET','POST'])
def register():
    if request.method=="GET":
        render_template("reg.html")
    else:
        cred=json.loads(request.cookies.get("usr"))
        if "image" in request.files:
            image_file = request.files["image"]
            unique_filename = str(uuid.uuid4()) + os.path.splitext(image_file.filename)[-1]
            full_path =os.path.join(upload_path , unique_filename)
            image_file.save(full_path)
            image_url = baseurl+url_for("uploaded_file", filename=unique_filename)
        else:
            image_url="Not Found"
        data={
        "mailid": request.form["mailid"],
        "name": request.form["name"],
        "description": request.form["description"],
        "location": request.form["location"],
        "phno": request.form["phno"],
        "price": request.form["price"],
        "imgurl": image_url
        }
        response=requests.post(baseurl+"/register",json=data,headers={"Authorization": cred['jwt']})
        flash(response.json)
        if response.status_code ==200:
            redirect(url_for("show"))

@app.route("/acm/mod",methods=['GET','DELETE','PATCH'])
def acm():
    cred=json.loads(request.cookies.get("usr"))
    if request.method=='GET':
        data=requests.get(f'{baseurl}/acm/op/',headers={"Authorization": cred['jwt']})
        render_template("singleacm.html")
    elif request.method=='DELETE':
        requests.delete(f'{baseurl}/acm/op/',headers={"Authorization": cred['jwt']})
        return redirect(url_for("showall"))
    else:
        data={
        "description": request.form["description"],
        "phno": request.form["phno"],
        "price": request.form["price"]
        }
        requests.patch(f'{baseurl}/acm/op/',headers={"Authorization": cred['jwt']},json=data)
        return redirect(url_for("acm"))

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return url_for("static", filename=os.path.join(upload_path , filename))

@app.route("/searchall/")
def showall():
    data=requests.get(f"{baseurl}/acm/searchall",params=request.args)
    render_template("display.html",json=data)
    
if __name__ == '__main__':
   app.run(debug = True,port=8083)  