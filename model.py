from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import correlation

engine = None
session = None

engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))
Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

    def similarity (user1, user2):
        user1_dict = {}
        pair_list = []
        for r in user1.ratings:
            user1_dict[r.movie_id] = r
        for r in user2.ratings:
            user1_rating = user1_dict.get(r.movie_id)
            if user1_rating:
                pair_list.append( (r.rating, user1_rating.rating) )
        if pair_list:
            return correlation.pearson(pair_list)
        else:
            return 0.0

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable=False)
    release_date = Column(DateTime(30), nullable=True)
    imdb_url = Column(String(300), nullable=True)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable=False)

    user = relationship("User", 
            backref=backref("ratings", order_by=id))
    movie = relationship("Movie",
            backref=backref("ratings", order_by=id))

### End class declarations

# def connect():
#     global ENGINE
#     global Session

#     return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
    Base.metadata.create_all(engine)