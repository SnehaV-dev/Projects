from flask import Flask,request,render_template,url_for,redirect,session,flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash,check_password_hash
import re
from datetime import datetime
app=Flask(__name__)
app.secret_key="miniproject"



mongo_url="mongodb+srv://vsharlinssneha:6AX6fMtBgwlQMvdQ@cluster0.sgtrx.mongodb.net/"
client=MongoClient(mongo_url)
db=client.employee_details
collection=db.details
collection_signup=db.password
employee_collection=db.employee



def pwd(password):
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

@app.route("/",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        # data=collection_signup.find_one({"username":name})l
        # if data["username"]==name:
        if collection_signup.find_one({"username":username}):
            return "username already exist"
        else:
            if not pwd(password):
                return "check password"
            else:
                hashed_password=generate_password_hash(password)
                user={}
                user.update({"username":username})
                user.update({"password":hashed_password})
                collection_signup.insert_one(user)
                flash("Signup successful! Please log in.", 'success')
                return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        login_data=collection_signup.find_one({"username":username})
        if login_data and check_password_hash(login_data["password"],password):
            session['username'] = username  # Save username in session
            flash("Login successful!", 'success')
            return redirect(url_for("home"))
        else:
            return "check login credentials"
    return render_template("login.html")



@app.route("/logout")

def logout():

    session.pop("session",None)
    flash("You have been logged out.", 'success')

    return redirect(url_for('login'))

@app.route("/insert", methods=["GET", "POST"])
def insert():
    if 'username' not in session:  # Ensure the user is logged in
        flash("Please log in to add an entry.", 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        
        name = request.form.get("name")
        position = request.form.get("position")
        department = request.form.get("department")
        date = request.form.get("date")
        hours_worked = request.form.get("hours_worked")

        timesheet_entry = {
            "Name": name,
            "Position": position,
            "Department": department,
            "Date": date,
            "HoursWorked": hours_worked,
        }

        collection.insert_one(timesheet_entry)
        flash("Timesheet entry added successfully!", 'success')
        return redirect(url_for('home', view='timesheet'))

    return render_template("insert.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if 'username' in session:
        current_date = datetime.now()  # Get the current date
        user = collection_signup.find_one({"username": session['username']})
        view = request.args.get('view', 'default')

        # Fetch employee details for the logged-in user
        employees = employee_collection.find_one({"username": session['username']})

        timesheet_entries = []  # Initialize empty list for timesheet entries

        if view == 'timesheet':
            # Fetch all timesheet entries from the database
            timesheet_entries = collection.find()

        return render_template(
            "home.html", 
            username=session['username'], 
            current_date=current_date, 
            user=user, 
            employee=employees,  # Pass employee details to the template
            view=view, 
            timesheet_entries=timesheet_entries
        )
    else:
        flash("Please log in to access this page.", 'danger')
        return redirect(url_for('login'))
    

@app.route('/timesheet/edit/<id>', methods=['GET', 'POST'])
def edit_timesheet(id):
    # Fetch the timesheet entry by ObjectId
    entry = collection.find_one({"_id": ObjectId(id)})

    if request.method == 'POST':
        
        collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "Date": request.form['date'],
                "Name": request.form['name'],
                "Position": request.form['position'],
                "Department": request.form['department'],
                "HoursWorked": request.form['hours_worked']
            }}
        )
        flash("Timesheet entry updated successfully!", 'success')
        return redirect(url_for('home', view='timesheet'))

    return render_template('edit.html', entry=entry)


@app.route('/timesheet/delete/<id>', methods=['POST'])
def delete_timesheet(id):
    collection.delete_one({"_id": ObjectId(id)})
    flash("Timesheet entry deleted successfully!", 'success')
    return redirect(url_for('home', view='timesheet'))















    







   



if __name__=="__main__":

    app.run(debug=True)