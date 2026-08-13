from flask import Blueprint, render_template, request, jsonify, make_response, current_app, redirect, g
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import User, Application, db
import datetime
import jwt
import requests
import os
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint("bp", __name__)


@bp.route("/")
def visit_home():
    if g.current_user and g.current_user.role == "admin":
        return redirect("/dashboard")
    return render_template("home.html")


@bp.route("/details")
def visit_details():
    if g.current_user and g.current_user.role == "admin":
        return redirect("/dashboard")
    return render_template("details.html")

@bp.route("/apply")
def visit_apply():
    if not g.current_user:
        return redirect("/login")
    if g.current_user.role == "admin":
        return redirect("/dashboard")
    return render_template("apply.html")

@bp.route("/dashboard")
def visit_dashboard():
    if not g.current_user:
        return redirect("/login")

    if g.current_user.role == "admin":
            applications = Application.query.all()
            return render_template("dashboard.html", applications=applications)
    else:
        app = Application.query.filter_by(email=g.current_user.email).first()
        if app:
            return render_template("dashboard.html", application=app)
        return render_template("dashboard.html")

@bp.route("/login")
def login():
    if g.current_user:
        return redirect("/")
    return render_template("login.html")

@bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username") 
    email = data.get("email") 
    password = data.get("password") 
    repeatedPassword = data.get("repeatedPassword") 

    if password != repeatedPassword:
        return jsonify({"message": "The entered passwords don't match."}), 401
    
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "A user with the entered email exists already."}), 401
    
    user = User(username = username,
                email = email,
                hashed_password = generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": f"{username}, Your account has been successfully created. Log in with your new credentials!"}), 200

@bp.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()

    email = data.get("email") 
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "There is no user with the entered email." }), 400
    
    if not check_password_hash(user.hashed_password, password):
        return jsonify({"message": "The entered password is wrong. please try again." }), 401

    payload = {
        "id": user.id,
        "email": user.email,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
    }

    token = jwt.encode(payload, current_app.config["SHARED_SECRET_KEY"], algorithm="HS256")
    response = make_response(jsonify({"message": "The user is succeffully logged in."}), 200)
    response.set_cookie("user_token", token, httponly=True, secure=False, samesite="Lax")

    return response

@bp.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "the user has successfully logged out."}))
    response.delete_cookie("user_token")
    return response

@bp.route("/api/apply", methods=["POST"])
def newApplication():
    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    age = data.get("age")
    medical_certificate= data.get("medical_certificate")
    gpa = data.get("gpa")
    flight_hours= data.get("flight_hours")

    if email != g.current_user.email:
        return jsonify({"message": "THe application email and account email don't match. Please log in with email you would like to apply with."}), 401

    if Application.query.filter_by(email=email).first():
        return jsonify({"message": "An application with this email has already been submitted."}), 400
    
    newApplication = Application(
        full_name=full_name,
        email=email,
        age=age,
        medical_certificate=medical_certificate,
        gpa=gpa,
        flight_hours=flight_hours
    )

    db.session.add(newApplication)
    db.session.commit()

    return jsonify({"message": f"An application with the '{email}' email has been successfully submitted."}), 200

@bp.route("/update-status", methods=["PUT"])
def update_status():
    data = request.get_json()
    application_id = data["id"]
    new_status = data["status"]

    application = Application.query.get(application_id)

    if not application:
        return jsonify({"message": "Application not found."}), 404
    
    email = application.email
    name = application.full_name

    if new_status == "accepted":
        application.status = new_status
    else:
        db.session.delete(application)

    db.session.commit()

    payload = {
        "email": email,
        "name": name,
        "status": new_status
    }

    processing_service_url = os.getenv("PROCESSING_SERVICE_URL")
    print(processing_service_url)

    try:
        response = requests.post(processing_service_url, json=payload, timeout=5)
    except Exception as e:
        return jsonify({"message": f"Error occured: {e}."}), response.status_code 

    return jsonify({"message": "Application status has been successfully updated."}), 200



    




    