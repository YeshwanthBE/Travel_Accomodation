import os
from flask import Flask,request,make_response,jsonify,render_template,url_for
import requests
from Reviews import reviews
app=Flask(__name__)

@app.route('/reviews/',methods=['PATCH','POST','DELETE'])
def review():
    try:
        obj=reviews(os.getcwd()+"\\Reviews_Ratings\\Process_api\\config.yaml")
        jwt=request.headers.get('Authorization')
        if request.method=='PATCH':
            response=obj.mod(jwt,request.get_json())
            return jsonify(response.json()),response.status_code
        elif request.method=='DELETE':
            response=obj.delete(jwt,request.args)
            return jsonify(response.json()),response.status_code
        else:
            response=obj.add(request.get_json(),jwt)
            return jsonify(response.json()),response.status_code
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
@app.route("/reviews/searchall/")
def srchall():
    try:
         obj=reviews(os.getcwd()+"\\Reviews_Ratings\\Process_api\\config.yaml")
         jwt=request.headers.get('Authorization')
         data=request.get_json()
         if not data.get('sort'):
             data['sort']="rating"
         response=obj.searchall(data,jwt)
         return jsonify(response.json()),response.status_code
    except Exception as e:
         return jsonify({"Exception": str(e)}),500

if __name__ == '__main__':
   app.run(debug = True,port=8087)  