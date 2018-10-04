from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

# Configure database:

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://aftypaczlaebaq:25e840e2d1820fb545ab359c9eaa1c9ce17f4d8db7df49ea50c22622f6def3ea@ec2-54-83-29-34.compute-1.amazonaws.com:5432/dcbihhqogiluuj"

heroku = Heroku(app)

db = SQLAlchemy(app)


# Create database model:

class User(db.Model):
    __tablename__ = "users"
    _id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return f"<E-mail {self.email}>"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preregister", methods=["POST"])
def preregister():
    email = None
    if request.method == "POST":
        email = request.form["email"]
        reg = User(email)
        db.session.add(reg)
        db.session.commit()
        return render_template("success.html")
    return render_template("error.html")

@app.route("/return_emails", methods=["GET"])
def return_emails():
    all_emails = db.session.query(User.email).all()
    return jsonify(all_emails)

if __name__ == "__main__":
    app.debug = True
    app.run()