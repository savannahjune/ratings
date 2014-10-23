from model import User, Movie, Rating, connect, Session 
import csv

def load_users(session):
    # use u.user
    # consider removing b
    with open('seed_data/u.user', 'rb') as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            user = User(id =row[0], age=row[1], zipcode=row[4])
            print user
            session.add(user)
            session.commit()


def load_movies(session):
    # use u.item
    pass

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    pass

if __name__ == "__main__":
    s= connect()
    main(s)

