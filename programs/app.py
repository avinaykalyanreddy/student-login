from pymongo import MongoClient
from flask import *

client = MongoClient("mongodb://localhost:27017/")
col1 = client.project1.staffs
col2 = client.student.ise_a

app = Flask(__name__)

@app.route("/")
def login_page():
    return render_template("index.html")

@app.route("/server_form",methods=["POST"])
def login_data():
    
    username = request.form["unsername"]
    password = request.form["password"]
    su = request.form["su"]

    
    


    if su == "Staff":
        staff = col1.find_one({"name":username},{"_id":0})

        if (staff and staff["name"] == username) and ( staff["password"]==password ):

            return render_template("info.html",staff=staff)
        
        else:

            return "Username or Password is incorrect, get back to login page<a href='/'> Click here</a>"
        

    elif su == "Student":

        student = col2.find_one({"name":username},{"_id":0})
        if (student and student["name"] == username) and ( student["password"]==password ):

            return render_template("info_s.html",student=student)
        else:

            return "Username or Password is incorrect, get back to login page<a href='/'> Click here</a>"
        
@app.route("/sign_up",methods=["POST"])

def sign_up():

    su = request.form["su"]

    if su == "Student":
    
        if not(col2.find_one({"usn":request.form["usn"]})):

            col2.insert_one({

            "name":request.form["name"],
            "password":request.form["password"],
            "usn":request.form["usn"],
            "phno":request.form["phno"],
            "branch":request.form["branch"],
            "section":request.form["section"],
            "sem":request.form["sem"],
            "email":request.form["email"]



            })
            return redirect(url_for("login_page"))
        
        else:
            return "Profile is already exists, get back to login page<a href='/'> Click here</a>"

        
        
    
    return redirect(url_for("sign_up_html"))

      
    


@app.route("/sign_up_html")
def sign_up_html():

    return render_template("signup.html")

@app.route("/students",methods=["POST"])
def students():
    if request.form["select"] == "ISE-1":
        data  = col2.find({},{"_id":0})
        return render_template("students.html",data=data)
    
    return "No data"
    
@app.route("/profile/<usn>")
def profile(usn):

    
    student = col2.find_one({"usn": usn}, {"_id": 0})
    return render_template("info_s.html", student=student)
    
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
