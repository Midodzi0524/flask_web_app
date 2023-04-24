from flask import Blueprint, render_template,request, flash, redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,logout_user, current_user, login_required

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        Password=request.form.get("Password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.Password, Password):
                flash("Logged in successfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect Password.Try again", category="error")
        else:
            flash("Account doesn't exist",category="error" )
                
            
            
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method=="POST":
        email=request.form.get("email")
        FirstName=request.form.get("FirstName")
        Surname=request.form.get("Surname")
        Password=request.form.get("Password")
        Password2=request.form.get("Password2")
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Account already exists.", category="error")
            return redirect(url_for("views.home"))
        
        elif len(email) < 4:
            flash(message="Email must have more than 3 characters", category="error")
        elif len(FirstName) < 2:
            flash(message="First Name must have more than 3 characters", category="error")
        elif len(Surname) < 2:
            flash(message="Surname must have more than 3 characters", category="error")
        elif Password != Password2:
            flash(message="Password don't match. Try again", category="error")
        elif len(Password) < 7:
            flash(message="Password must have more than 6 characters", category="error")    
        
        else:
            new_user=User(email=email,firstname=FirstName,Surname=Surname, Password=generate_password_hash(Password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash(message="Account Created!", category="success")
            return redirect(url_for("views.home"))
        
                
                   
             
    return render_template("sign_up.html", user=current_user)