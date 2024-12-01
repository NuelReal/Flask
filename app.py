import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__, template_folder='template')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get("USER")
app.config["MAIL_PASSWORD"] = os.environ.get("PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = "mbaguemmanuel2002@gmail.com"


db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.phone}', '{self.address}')"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/venue")
def venue():
    return render_template("venue.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Error: This email is already registered!"

        new_name = User(name=name, email=email, phone=phone, address=address)
        db.session.add(new_name)
        db.session.commit()

        msg = Message("Confirm Email", sender="mbaguemmanuel2002@gmail.com", recipients=[email])

        msg.body = f"Subject: Welcome to the Design and Tech Workshop Event!\n\n" f"Dear {name},\n\n" "Thank you for registering for the Design and Tech Workshop event in Nigeria! " "We're thrilled to have you join us for this exciting event where innovation meets creativity.\n\n\n" "EVENT DETAILS\n\n" "*   Date: 20th December, 2024\n\n" "*   Time: 9:00am\n\n" "*   Venue: Rockview Hotel\n\n" "At the workshop, you’ll have the opportunity to connect with industry experts, participate in hands-on sessions and explore groundbreaking trends in design and technology.\n\n" "We look forward to seeing you at the event!\n\n" "Best regards,\n" "Design and Tech Workshop Team"

        mail.send(msg)

        return "Thank you, " + name + "! Your registration is complete. A confirmation has been sent to " + email + "."

    return render_template("register.html") 

if __name__ == '__main__':
    app.run(debug=True)