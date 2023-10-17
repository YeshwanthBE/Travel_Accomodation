from flask import Flask,render_template,url_for,request,flash,redirect,make_response,jsonify
import requests
import json
import yaml
import os 
import uuid
from datetime import date, timedelta,datetime
import stripe
app=Flask(__name__)
app.static_folder = 'static'
with open(os.getcwd()+'\\SrcCode\\Booking\\Experience_api\\config.yaml', 'r') as file:
    global baseurl,config
    config=yaml.safe_load(file)
    baseurl= config['url']['domainurl']
    app.secret_key=config['app']['key']
    stripe.api_key = config['stripe']['skey']
@app.route('/booking/')
def register():
    if request.method=="GET":
         cred=json.loads(request.cookies.get("usr"))
         acm=requests.get(config['url']['acmurl']+"/acm/mod/",params=request.args).json()
         reviews=requests.get(config['url']['revurl']+"/reviews/",params=request.args).json()
         min_date=str(date.today()+timedelta(days=1))
         max_date=str(date.today()+timedelta(days=365))
         blockeddates=json.loads(requests.get(baseurl+'/allacmbks',params=request.args).json())
         bdates=list()
         for i in blockeddates:
             checkin = datetime.strptime(i['checkin'], "%Y-%m-%d")
             checkout = datetime.strptime(i['checkout'], "%Y-%m-%d")
             while checkin <= checkout:
                bdates.append(checkin.strftime("%Y-%m-%d"))
                checkin += timedelta(days=1)
         return render_template("booking.html",acm=acm,admin=cred['ap'],reviews=reviews,bdates=bdates,min_date=min_date,max_date=max_date,blockeddates=blockeddates)
def addbooking(acmid,checkin,checkout):
    cred=json.loads(request.cookies.get("usr"))
    data={
    "acmid": acmid,
    "checkin": checkin,
    "checkout": checkout
    }
    response=requests.post(baseurl+"/pr/booking/",json=data,headers={"Authorization": cred['jwt']})
    if response.status_code ==201:
        return redirect(config['url']['homepage']+"/Dashboard/")
    else:
        return redirect(url_for("register",acmid=acmid))   
@app.route("/completedpayment/")
def cp():
    payment_intent_id = request.args.get('payment_intent')
    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    qp=request.args
    if payment_intent.status == 'succeeded':
        response=addbooking(qp.get('acmid'),qp.get('checkin'),qp.get('checkout'))
        response.delete_cookie('acmid')
        return response
    else:
        return redirect(url_for('/booking/',acmid=request.args.get('acmid')))

@app.route("/prevbooking/")
def bkg():
    if request.method=='GET':
        cred=json.loads(request.cookies.get("usr"))
        data=requests.get(f'{baseurl}/pr/booking/',headers={"Authorization": cred['jwt']},params=request.args)
        render_template("booking.html")

@app.route("/searchall/")
def showall():
    cred=json.loads(request.cookies.get("usr"))
    data=requests.get(f"{baseurl}/pr/searchall/",headers={"Authorization": cred['jwt']})
    render_template("display.html",json=data)
    
@app.route("/reviews/",methods=['POST'])
def addreviews():
    cred=json.loads(request.cookies.get("usr"))
    qp=request.args
    data={
        "acmid": qp.get('acmid'),
        "review": request.form["userreview"],
        "rating": request.form["rating"],
        }
    requests.post(config['url']['addrev']+"/reviews/",headers={"Authorization": cred['jwt']},json=data)
    return redirect(url_for("register",acmid=qp.get('acmid')))

@app.route("/proceedtopay/",methods=['POST'])
def ptp():
    data={
        "checkin":request.form.get("checkin"),
        "checkout":request.form.get("checkout")
    }
    response=make_response(render_template("payment.html",price=calp(data,request.args),acmid=request.args.get('acmid'),checkin=data['checkin'],checkout=data['checkout']))
    response.set_cookie("acmid",request.args.get('acmid'))
    return response
@app.route('/payment/',methods=['POST'])
def payment():
        try:
            data = json.loads(request.data)
            price=float(data.get("price"))*100
            print(price)
            intent = stripe.PaymentIntent.create(
                amount=int(price),
                currency='inr',
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return jsonify({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return jsonify(error=str(e)), 403

def calp(data:json,params:json):
    date1 = datetime.strptime(data['checkin'], "%Y-%m-%d")
    date2 = datetime.strptime(data['checkout'], "%Y-%m-%d")
    delta = date2 - date1
    num_days = delta.days
    acm=requests.get(config['url']['acmurl']+"/acm/mod/",params=params).json()
    amount=float(acm['price'])*num_days
    totalprice=amount+2*amount*0.18
    return totalprice

@app.route('/home/<int:v>')
def home(v):
    url=config['url']['homepage']+('/Dashboard/' if v else '/')
    return redirect(url)
if __name__ == '__main__':
   app.run(debug = True,port=8093)  