from model import User, Movie, Rating, connect 
from datetime import datetime
import csv

def load_users(session):
    # use u.user
    # consider removing b
    with open('seed_data/u.user', 'rb') as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            user = User(id =row[0], age=row[1], zipcode=row[4])
            # print user
            session.add(user)
        session.commit()


def load_movies(session):
    # use u.item
    with open('seed_data/u.item', 'rb') as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            if row[2] == "":
                row[2] = "01-Jan-1970"
            movie = Movie(id = row[0], name = row[1].encode('utf-8'), release_date = datetime.strptime(row[2].strip(),"%d-%b-%Y"), imdb_url = row[3])
            # movie = Movie()
            # movie.id =row[0]
            # movie.name =row[1]
            # movie.release_date = datetime.strptime(row[2].strip(),"%d-%b-%Y")
            # movie.imdb_url=row[3]
            print movie
            session.add(movie)
        session.commit()
            

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    pass

if __name__ == "__main__":
    s= connect()
    main(s)

