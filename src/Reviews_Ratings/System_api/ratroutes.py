import os
from flask import Flask, request,make_response,jsonify
from dbratrev import rr
from functools import wraps
import jwt
app=Flask(__name__) 
app.config['SECRET_KEY']='a'
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            mailid = data['mailid']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.DecodeError:
            return jsonify({'message': 'Token is invalid'}), 401
        except:
            return  jsonify({'message': 'Unauthorized'}), 401
        return f(mailid,*args, **kwargs)
    return decorated

@app.route('/dbreviews/',methods=['POST','DELETE','PATCH'])
@token_required
def review(mailid):
    try:
        obj=rr()
        qp=request.args
        obj.connect(os.getcwd()+"\\SrcCode\\Reviews_Ratings\\System_api\\config.yaml")
        if request.method=='PATCH':
            obj.mod(request.get_json())
            return jsonify({"message": "review updated Successfully"}), 200
        elif request.method=='DELETE':
            obj.delete(qp.get('rid'))
            return jsonify({"message": "review deleted Successfully"}), 200
        else:
            if obj.add(mailid,request.get_json()) is not False:
                return jsonify({"message": "review added Successfully"}), 201
            else:
                return jsonify({"message": "Failed"}), 401 
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
@app.route('/dballreviews/')
def show():
    try:
        obj=rr()
        obj.connect(os.getcwd()+"\\SrcCode\\Reviews_Ratings\\System_api\\config.yaml")
        return jsonify(obj.showall(request.get_json())),200
    except Exception as e:
        return jsonify({"Exception": str(e)}),500
    
if __name__ == '__main__':
   app.run(debug = True,port=8091)  