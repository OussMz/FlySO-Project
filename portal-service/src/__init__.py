from flask import Flask, render_template, request, jsonify, make_response, current_app, g
import jwt
import os
from werkzeug.security import generate_password_hash
import getpass
from dotenv import load_dotenv
from src.models import db, migrate, User

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SHARED_SECRET_KEY"] = os.getenv("SHARED_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    @app.cli.command("create_user")
    def create_user():

        username = input("username: ").strip()
        email = input("email: ").strip().lower()
        password = getpass.getpass("password: ")
        role = input("role: ").strip().lower()

        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()

        if existing_user:
            print(f"Error: the entered email or username already exists.")
            return

        user = User(
            username= username,
            email=email,
            hashed_password= generate_password_hash(password),
            role=role
        )

        db.session.add(user)
        db.session.commit()

        print(f"{role} created successfully.")
        
    @app.before_request
    def verify_user():
        g.current_user = None
        token = request.cookies.get("user_token")
        if not token:
            return
        
        try:
            payload = jwt.decode(token, current_app.config["SHARED_SECRET_KEY"], algorithms=["HS256"])
            user = db.session.get(User, payload["id"])
            g.current_user = user
        except Exception as e:
            return

        
    from src.routes import bp
    app.register_blueprint(bp)



    return app

