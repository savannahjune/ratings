from flask import Flask, render_template, g, redirect, request, session, flash
from model import User, Movie, Rating, session as dbsession 
import jinja2


app = Flask(__name__)
app.secret_key ='alkjgfladjflkajdoiwelfkasdg;ljkasdfljk'
# app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def sign_up():
    return render_template("sign_up.html")

@app.route("/", methods=["POST"])
def process_new_user():
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
    
    u = dbsession.query(User).filter_by(email = email).filter_by(password=password).first()

    if u:
        session["login"] = u.id
        return redirect("/main")      
    else:
        flash("User not recognized please try again. Or sign up below.")
        return redirect("/")

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/main", methods=["POST"])
def search():
    movie = request.form.get("movie")
    # movie = dbsession.query(Movie).get(id)
    movie_info = dbsession.query(Movie).filter_by(name = movie).first()
    release_date = movie_info.release_date
    imdb_url = movie_info.imdb_url
    ratings = movie_info.ratings
    movie_ratings = movie_info.ratings
    rating_nums = []
    user_rating = None
    for r in movie_ratings:
        if r.user_id == session["login"]:
            user_rating = r
        rating_nums.append(r.rating)
    avg_rating = float(sum(rating_nums))/len(rating_nums)

    #prediction code: only predict if the user hasn't rated it
    user = dbsession.query(User).get(session['login'])
    prediction = None
    if not user_rating:
        prediction = user.predict_rating(movie_info)
    #End Prediction

    user = dbsession.query(User).get(session['login'])
    prediction = None
    if not user_rating:
        prediction = user.predict_rating(movie_info)
        effective_rating = prediction
    else:
        effective_rating = user_rating.rating 

    the_eye = dbsession.query(User).filter_by(email="theeye@ofjudgement.com").one()
    eye_rating = dbsession.query(Rating).filter_by(user_id=the_eye.id, movie_id=movie_info.id).first()

    if not eye_rating:
        eye_rating = the_eye.predict_rating(movie_info)
    else:
        eye_rating = eye_rating.rating

    difference = abs(eye_rating - effective_rating)

    messages = [ "I suppose you don't have such bad taste after all.",
                 "I regret every decision that I've ever made that has brought me to listen to your opinion",
                  "Words fail me, as your taste in movies has clearly failed you.",
                  "That movie is great. For a clown to watch. Idiot."]

    beratement = messages[int(difference)]

    return render_template("movie_info.html", beratement = beratement, user_rating = user_rating, prediction = prediction, ratings = ratings, average = avg_rating, movie = movie, release_date = release_date, imdb_url = imdb_url)


@app.route("/user_id/<int:user_id>")
def find_user_ratings(user_id):
    ratings = dbsession.query(Rating).filter_by(user_id = user_id).all()
    return render_template("/user_ratings.html", ratings = ratings, user_id = user_id)

@app.route("/my_reviews")
def my_reviews():
    user_id = session["login"]
    ratings = dbsession.query(Rating).filter_by(user_id = user_id).all()
    return render_template("my_reviews.html", user_id = user_id, ratings = ratings)

@app.route("/add_review")
def add():
    return render_template("add_review.html")

@app.route("/add_review", methods=["POST"])
def add_review():
    movie = request.form.get("movie")
    # TODO: Add a check if movie doesn't exist
    movie_id = dbsession.query(Movie).filter_by(name = movie).first().id
    rating = request.form.get("rating")
    rating = Rating(movie_id = movie_id, user_id = session["login"], rating = rating)
    dbsession.add(rating)
    dbsession.commit()
    return render_template("main.html")

# @app.route("/main/<int:id>", methods = ["GET"])
# def view_movie(id):
#     movie = dbsession.query(Movie).get(id)
#     ratings = movie.ratings
#     rating_nums = []
#     user_rating = None
#     for r in ratings:
#         if r.user_id == session["login"]:
#             user_rating = r
#         rating_nums.append(r.rating)
#     avg_rating = float(sum(rating_nums))/len(rating_nums)

#     #prediction code: only predict if the user hasn't rated it
#     user = dbsession.query(User).get(session['user_id'])
#     prediction = None
#     if not user_rating:
#         prediction = user.predict_rating(movie)
#     #End Prediction

#     return render_template("movie_info.html", movie = movie, average = avg_rating, user_rating = user_rating, prediction = prediction)

        



if __name__ == "__main__":
    app.run(debug = True)
