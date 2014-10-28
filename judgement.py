from flask import Flask, render_template, g, redirect, request, session
from model import User, Movie, Rating, session as dbsession 


app = Flask(__name__)

@app.route("/")
def sign_up():
    return render_template("sign_up.html")

@app.route("/", methods=["POST"])
def process():
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    print email, password, age, zipcode 
    user = User(email = email, password=password, age=age, zipcode=zipcode)
    dbsession.add(user)
    dbsession.commit()
    return redirect("/login")

@app.route("/login")
def log_in():
    return render_template("login.html")

# @app.route("/login", methods=["POST"])
# def index():
#     email = request.form.get("email")
#     password = request.form.get("password")
#     u = session.query(User).filter_by(email = email)
#     if u.password == password:
#         session["login"] = u.id
#         redirect("/main")
#     else:
#         redirect("/login")

@app.route("/main")
def main():
    return render_template("main.html")


if __name__ == "__main__":
    app.run(debug = True)
