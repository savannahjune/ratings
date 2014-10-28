from flask import Flask, render_template, g, redirect, request, session, flash
from model import User, Movie, Rating, session as dbsession 
import jinja2



app = Flask(__name__)
app.secret_key ='alkjgfladjflkajdoiwelfkasdg;ljkasdfljk'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def sign_up():
    return render_template("sign_up.html")

@app.route("/", methods=["POST"])
def process():
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    user = User(email = email, password=password, age=age, zipcode=zipcode)
    if dbsession.query(User).filter_by(email = email).first():
        flash("Sorry this email is taken. Please try another.")
        return redirect("/")
    else:
        dbsession.add(user)
        dbsession.commit()
        return redirect("/login")

@app.route("/login")
def log_in():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def index():
    email = request.form.get("email")
    password = request.form.get("password")
    if dbsession.query(User).filter_by(email = email).count() > 0:
        u = dbsession.query(User).filter_by(email = email).one()
        if u.password == password:
            session["login"] = u.id
            return render_template("main.html")  
        else:
            flash("Wrong password please try again.")
            return redirect("/login")    
    else:
        flash("Email not recognized please try again. Or sign up below.")
        return redirect("/")

@app.route("/main")
def main():
    return render_template("main.html")


if __name__ == "__main__":
    app.run(debug = True)
