from flask import Flask, render_template, request,make_response,session,flash,jsonify
from Database import User
app=Flask(__name__) 
obj=User("C:\\Users\\Yeshwanth B E\\Desktop\\Project\\Travel_Accomodation\\User_Profile\\System_api\\config.yaml")
@app.route('/profile/Signup',methods=['POST'])
def signup():
    obj.add_user(request.get_json())
    response_data = {"message": "User Registered Successfully"}
    return jsonify(response_data), 201
@app.route('/profile/<mailid>',methods=['GET','POST','DELETE','PATCH'])
def profile(mailid):
    if request.method=='GET':
        return jsonify(obj.show_user(mailid))
    elif request.method=='DELETE':
        obj.del_user(mailid)
        response_data = {"message": "User Deleted Successfully"}
        return jsonify(response_data), 204
    elif request.method=='POST':
        data=request.get_json()
        obj.reset_pass(mailid,data['newpwd'])
        response_data = {"message": "Password Resetted Successfully"}
        return jsonify(response_data), 200
    else:
        data=request.get_json()
        obj.update_user(mailid,data)
        response_data = {"message": "Profile Updated Successfully"}
        return jsonify(response_data), 200
if __name__ == '__main__':
   app.run(debug = True)    
