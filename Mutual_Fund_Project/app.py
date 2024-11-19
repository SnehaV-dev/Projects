from flask import Flask,render_template,session,redirect,url_for,request,flash
from flask_mysqldb import MySQL
import re
import requests
app=Flask(__name__)
app.secret_key="123qwe"

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='familylove@26'
app.config['MYSQL_DB']='login_details'

mysql= MySQL(app)

    
def validate_password(password):
    if len(password)<8:
        return False
    elif not re.search (r"[a-z]",password):
        return False
    elif not re.search(r"[A-Z]",password):
        return False
    elif not re.search(r"[0-9]",password):
        return False
    elif not re.search(r"[!@#$%^&*+=]",password):
        return False
    return True

def loggedin():
    return "username" in session

url="https://api.mfapi.in/mf/"

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        if not validate_password(password):
            flash('Password should be at least 8 characters long and contain uppercase, lowercase, digit, and special characters.', 'danger')
            return redirect(url_for("signup"))
        cur=mysql.connection.cursor()
        cur.execute("insert into details(username,password) values(%s,%s)",(username,password))
        mysql.connection.commit()
        cur.close()
        flash("signup successful",'success')
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        cur=mysql.connection.cursor()
        cur.execute("select * from details where username=%s",(username,))
        data=cur.fetchone()
        cur.close()
        if data[0]==username and data[1]==password:
            session["username"]=username
            flash("login successful")
            return redirect(url_for("home"))
           
        else:
            flash("invalid username",'danger')
             
    return render_template("login.html")

@app.route("/")
def home():
    
    if not loggedin():
        return render_template("index.html")
    else:
        username=session["username"]
        cur=mysql.connection.cursor()
        cur.execute( "select * from mf where Name=%s",(username,))
        data=cur.fetchall()
        cur.close()
        return render_template("index.html",mf=data)
      
    



@app.route("/insert",methods=["GET","POST"])
def insert():
    if request.method=="POST":
        name=request.form.get("name")
        Fund_code=request.form.get("fund")
        Invested_amt=float(request.form.get("investedamt"))
        Units_held=float(request.form.get("units_held"))
        completeurl=requests.get(url + str(Fund_code))
        Fund_name=completeurl.json().get("meta")["fund_house"]
        Nav=float(completeurl.json().get("data")[0]["nav"])
        current_value=Units_held*Nav
        Growth=current_value - Invested_amt
        
        cur=mysql.connection.cursor()
        cur.execute("insert into mf (Name,Fundcode,Invested_amt,Units,Fund_name,Nav,Current_value,Growth) values(%s,%s,%s,%s,%s,%s,%s,%s)",(name,Fund_code,Invested_amt,Units_held,Fund_name,Nav,current_value,Growth))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for("home"))
    return render_template("insert.html")


@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    if request.method=="POST":
        name=request.form.get("name")
        Fund_code=request.form.get("fund")
        Invested_amt=float(request.form.get("investedamt"))
        Units_held=float(request.form.get("units_held"))
        completeurl=requests.get(url + str(Fund_code))
        Fund_name=completeurl.json().get("meta")["fund_house"]
        Nav=float(completeurl.json().get("data")[0]["nav"])
        current_value=Units_held*Nav
        Growth=current_value-Invested_amt
        cur=mysql.connection.cursor()
        cur.execute("update mf set Name=%s ,Fundcode=%s,Invested_amt=%s,Units=%s,Fund_name=%s,Nav=%s,Current_value=%s,Growth=%s where id=%s",(name,Fund_code,Invested_amt,Units_held,Fund_name,Nav,current_value,Growth,id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("home"))
    cur=mysql.connection.cursor()
    cur.execute("select * from mf where id=%s",(id,))
    data=cur.fetchone()
    cur.close()
    return render_template("edit.html",data=data)

@app.route("/delete/<int:id>")
def delete(id):
    if not loggedin():
        flash("You must be logged in to delete entries", "danger")
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM mf WHERE id=%s", (id,))
    mysql.connection.commit()
    flash("Entry deleted successfully", "success")
    cur.close()
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
   session.pop("username", None)
   return redirect(url_for("login"))








if __name__=="__main__":
    app.run(debug=True)