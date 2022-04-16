import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.automap import automap_base

engine = create_engine("sqlite:///movies.db", echo=False)

session = Session(engine)

inspector = inspect(engine)

Base = automap_base()
Base.prepare(engine, reflect=True)

# columns = inspector.get_columns('movies')
# for c in columns:
#     print(c['name'], c["type"])


peopletable = Base.classes.people
starstable = Base.classes.stars


same_person = session.query(peopletable, starstable).filter(peopletable.id == starstable.person_id).limit(10).all()

for person in same_person:
    (peopletable, starstable) = person
    print(peopletable.id)
    print(starstable.movie_id)

# combo = [ratingtable.movie_id, ratingtable.person_id, movietable.title, movietable.year]
# mergeone = session.query(*combo).filter(movietable.id == ratingtable.movie_id).limit(10).all()

# print(mergeone)


    