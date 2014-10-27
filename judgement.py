from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/")
def signup():
    return render_template("sign_up.html")

@app.route("/signin")
def index():
    user_list =  model.session.query(model.User).limit(5).all()
    return render_template("login.html", users=user_list)

if __name__ == "__main__":
    app.run(debug = True)