from flask import Flask,render_template,url_for,request,flash,redirect,make_response
import requests
import json
import yaml
import os 
import uuid
app=Flask(__name__)
with open(os.getcwd()+'\\src\\Reviews_Ratings\\Experience_api\\config.yaml', 'r') as file:
    global baseurl
    config=yaml.safe_load(file)
    baseurl= config['url']['domainurl']
    app.secret_key=config['app']['key']

@app.route('/reviews/',methods=['GET','POST','PATCH',"DELETE"])
def reviews():
    qp=request.args
    if request.method=="GET":
        data={
        "acmid": qp.get("acmid"),
        "sort": qp.get('sort'),
        "asc": qp.get('asc')
        }
        response=requests.get(baseurl+"/reviews/searchall/",json=data)
        return response.json()
    cred=json.loads(request.cookies.get("usr"))
    if request.method=="POST":
        data={
        "acmid": qp.get('acmid'),
        "review": request.form["review"],
        "rating": request.form["rating"],
        }
        requests.post(baseurl+"/reviews/",json=data,headers={"Authorization": cred['jwt']})
    elif request.method=="PATCH":
        data={
        "rid": qp.get('rid'),
        "review": request.form["review"],
        "rating": request.form["rating"],
        }
        requests.patch(baseurl+"/reviews/",json=data,headers={"Authorization": cred['jwt']})
    else:
        requests.delete(baseurl+"/reviews/",params=request.args,headers={"Authorization": cred['jwt']})
    redirect(url_for("show"))    

if __name__ == '__main__':
   app.run(debug = True,port=8096)  