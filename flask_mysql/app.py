from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_mysqldb import MySQL
app = Flask(__name__)
app.secret_key="abc@123"

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='familylove@26'
app.config['MYSQL_DB']='student_list'

mysql= MySQL(app)

def loggedin():
    return "username" in session

@app.route("/")
def home():
    cur=mysql.connection.cursor()
    cur.execute("select * from student")
    data=cur.fetchall()
    cur.close()
    return render_template("index.html",std=data)

      
 

@app.route("/insert",methods=["GET","POST"])
def insert():
    if request.method=="POST":
        
        name=request.form.get("name")
        age=request.form.get("age")
        roll_no=request.form.get("roll_no")
        marks1=request.form.get("marks1")
        marks2=request.form.get("marks2")
        marks3=request.form.get("marks3")
        marks4=request.form.get("marks4")
        marks5=request.form.get("marks5")
        cur=mysql.connection.cursor()
        cur.execute("insert into student (Name,Age,Roll_NO,Mark1,Mark2,Mark3,Mark4,Mark5) values(%s,%s,%s,%s,%s,%s,%s,%s)",(name,age,roll_no,marks1,marks2,marks3,marks4,marks5))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for("home"))
    return render_template("form.html")

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    if request.method=="POST":
        name=request.form.get("name")
        age=request.form.get("age")
        roll_no=request.form.get("rollno")
        marks1=request.form.get("marks1")
        marks2=request.form.get("marks2")
        marks3=request.form.get("marks3")
        marks4=request.form.get("marks4")
        marks5=request.form.get("marks5")
        cur=mysql.connection.cursor()
        cur.execute("update student set Name=%s, Age=%s, Roll_No=%s, Mark1=%s, Mark2=%s, Mark3=%s, Mark4=%s, Mark5=%s where id=%s",
                    (name,age,roll_no,marks1,marks2,marks3,marks4,marks5,id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("home"))
    cur=mysql.connection.cursor()
    cur.execute("select * from student where id=%s",(id,))
    data=cur.fetchone()
    cur.close()
    return render_template("edit.html",students=data)

@app.route("/delete/<int:id>",methods=["GET","POST"])
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute("delete from student where id=%s",(id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("home"))

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        cur=mysql.connection.cursor()
        cur.execute("insert into login_details  (username,password) values(%s,%s)", (username,password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        cur=mysql.connection.cursor()
        cur.execute("select * from login_details where username=%s and password=%s",(username,password))
        data=cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if data:
            
            session["username"]=username
            flash("login successful")

            return redirect(url_for("display"))
        else:
            flash ("invalid credentials")
        
    return render_template("login.html")

single_data=[]
@app.route("/display",methods=["GET","POST"])
def display():
    if loggedin():
      username=session["username"]
      cur=mysql.connection.cursor()
      cur.execute("select * from student where name=%s",(username,))
      data=cur.fetchone()
      cur.close()
      single_data.extend(data)
    return render_template("display.html",student=single_data)
   
   

    



@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("login"))



        
        

   

        

if __name__=="__main__":
    app.run(debug=True)
