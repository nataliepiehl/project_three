import sqlalchemy
from datetime import date
from sqlalchemy import Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Sequence, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.orm.exc import NoResultFound,MultipleResultsFound
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import ColumnClause
from sqlalchemy.sql import compiler
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///movies.db", echo=False)

connection = engine.connect()

Base = declarative_base()

class movies(Base):
    __tablename__ = 'movies'
    ID = Column(Integer, primary_key=True)
    TITLE = Column(String)
    YEAR = Column(Integer)

class ratings(Base):
    __tablename__ = 'ratings'
    MOVIE_ID = Column(Integer)
    RATING = Column(Float)
    VOTES = Column(Integer)

Session = sessionmaker(bind=connection)
session = Session()

query = session.query(movies).join(ratings, movies.ID==ratings.MOVIE_ID)

print(query)



    