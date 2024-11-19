from flask import Flask,render_template,session,redirect,url_for,request,flash
from flask_mysqldb import MySQL
import re
app=Flask(__name__)
app.secret_key="123qwe"

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='familylove@26'
app.config['MYSQL_DB']='ecommerce_login'

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

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        if not validate_password(password):
            flash('Password should be at least 8 characters long and contain uppercase, lowercase, digit, and special characters.', 'danger')
            return redirect(url_for("signup"))
        cur=mysql.connection.cursor()
        cur.execute("insert into login_details(Name,pwd) values(%s,%s)",(username,password))
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
        cur.execute("select * from login_details where Name=%s",(username,))
        data=cur.fetchone()

        print(data[1])
        cur.close()
        if data[1]==username and data[2]==password:
            session['username']=username
            
            flash("login successful")
            return redirect(url_for('loggedpage'))
        else:
            flash("invalid username",'danger')
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/loggedpage")
def loggedpage():
    return render_template("home.html")

@app.route("/products")
def product():
    return render_template("product.html")

@app.route("/productview")
def product_view():
    return render_template("productview.html")

@app.route("/productview1")
def product_view1():
    return render_template("productview1.html")

@app.route("/cart",methods=["GET","POST"])
def cart():
    # if request.method=="POST":
    #     quantity=request.form.get("quantity")
    #     print(quantity)
        name="HP Laptop"
        price=39999
        cur=mysql.connection.cursor()
        cur.execute("select * from login_details where Name=%s",((session.get('username'),)))
        data=cur.fetchone()

        user=data[1]
        print(user)
        cur=mysql.connection.cursor()  
        cur.execute("insert into cart_product(product,price,total_amt,user) values(%s,%s,%s,%s)",
                (name,price,price,user))
        mysql.connection.commit()
        cur.close()
        return render_template("product.html")

@app.route("/cart1",methods=["GET","POST"])
def cart1():
    name="Mi laptop"
    price=20000
    cur=mysql.connection.cursor()
    cur.execute("select * from login_details where Name=%s",((session.get('username'),)))
    data=cur.fetchone()

    user=data[1]
    print(user)
    cur=mysql.connection.cursor()  
    cur.execute("insert into cart_product(product,price,total_amt,user) values(%s,%s,%s,%s)",
                (name,price,price,user))
    mysql.connection.commit()
    cur.close()
    return render_template("product.html")


@app.route("/cart2",methods=["GET","POST"])
def cart2():
    name="Dell 3rd gen"
    price=29998
    cur=mysql.connection.cursor()
    cur.execute("select * from login_details where Name=%s",((session.get('username'),)))
    data=cur.fetchone()

    user=data[1]
    print(user)
    cur=mysql.connection.cursor()  
    cur.execute("insert into cart_product(product,price,total_amt,user) values(%s,%s,%s,%s)",
                (name,price,price,user))
    mysql.connection.commit()
    cur.close()
    return render_template("product.html")



@app.route("/shopping_cart")
def shopping_cart():
    cur=mysql.connection.cursor()
    cur.execute("select * from cart_product where user=%s",(session.get('username'),))
    all=cur.fetchall()
    print(all)
    cur.close()
    sum=0
    for i in all:
        sum=sum+i[3] 
    
    return render_template("cart.html",data=all,total=sum)

@app.route("/delete/<int:id>",methods=["GET","POST"])
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute("delete from cart_product where id=%s",(id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("shopping_cart"))


@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("home"))

if __name__=="__main__":
    app.run(debug=True)