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
            movie = Movie(id = row[0], name = row[1].decode("latin-1"), release_date = datetime.strptime(row[2].strip(),"%d-%b-%Y"), imdb_url = row[3])
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
    
    with open('seed_data/u.data', 'rb') as f:
        # reader = csv.reader(f)
        # for row in reader:
        #     print row
        #     row2= []
        #     i = 0
        #     row = row.split(" ")
        #     for i in row:
        #         if row[i] != "":
        #             row2.append(row[i])
        #         i+=1
        #     rating = Rating(id = row2[0], movie_id =row2[1], user_id = row2[2], rating = row2[3])
        #     print rating 
        for row in f:
            row = row.split()
            rating = Rating(id = row[0], movie_id = row[1], user_id = row[2], rating = row[3])
            print rating
            session.add(rating)
        session.commit()




def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session) 

if __name__ == "__main__":
    s= connect()
    main(s)

