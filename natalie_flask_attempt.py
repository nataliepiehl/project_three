# ------------------------------------------------------------
# Import modules
import json
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from flask import Flask, jsonify
from flask_cors import CORS
from operator import itemgetter

# ------------------------------------------------------------
# Setup database

# Create engine
engine = create_engine("sqlite:///movies.db")

# reflect an existing database into a new model
Base = automap_base()

# Reflest the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
people = Base.classes.people
ratingmix = Base.classes.ratingmix
starsmix = Base.classes.starsmix
directorsmix = Base.classes.directorsmix

# ------------------------------------------------------------
# Initialize Flask
app = Flask(__name__)
CORS(app)

# ------------------------------------------------------------
# Setup Flask routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/people_load/<br/>"
        f"/api/ratings_load/<br/>"
        f"/api/stars_load/<br/>"
        f"/api/directors_load/<br/>"
    )

@app.route("/api/people_load/")
def people_load():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(people.id, people.name, people.birth).all()

    # Close the session
    session.close()

    # Convert "rows" to a normal list
    results_jsonifiable = []
    for row in results:
        row_list = []
        for element in row:
            if element is None:
                pass
            elif not (isinstance(element, int) | isinstance(element, str)):
                row_list.append(float(element))
            else:
                row_list.append(element)
        row_dict = dict(zip(["id", "name", "birth"], row_list))
        results_jsonifiable.append(row_dict)

    return json.dumps({'people': results_jsonifiable})

@app.route("/api/ratings_load/")
def ratings_load():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(ratingmix.id, ratingmix.title, ratingmix.year,
                            ratingmix.movie_id, ratingmix.rating, ratingmix.votes).all()

    # Sort by vote count
    results = sorted(results, key=itemgetter('votes'), reverse=True)

    # Select for top 1000
    results = results[0:1000]

    # Close the session
    session.close()

    # Convert "rows" to a normal list
    results_jsonifiable = []
    for row in results:
        row_list = []
        for element in row:
            if element is None:
                pass
            elif not (isinstance(element, int) | isinstance(element, str)):
                row_list.append(float(element))
            else:
                row_list.append(element)
        row_dict = dict(zip(["id", "title", "year", "movie_id", "rating", "votes"], row_list))
        results_jsonifiable.append(row_dict)

    return json.dumps({'ratings': results_jsonifiable})

@app.route("/api/stars_load/")
def stars_load():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(starsmix.id, starsmix.title, starsmix.year,
                            starsmix.movie_id, starsmix.person_id).all()

    # Close the session
    session.close()

    # Convert "rows" to a normal list
    results_jsonifiable = []
    for row in results:
        row_list = []
        for element in row:
            if element is None:
                pass
            elif not (isinstance(element, int) | isinstance(element, str)):
                row_list.append(float(element))
            else:
                row_list.append(element)
        row_dict = dict(zip(["id", "title", "year", "movie_id", "person_id"], row_list))
        results_jsonifiable.append(row_dict)

    return json.dumps({'stars': results_jsonifiable})

@app.route("/api/directors_load/")
def directors_load():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(directorsmix.id, directorsmix.title, directorsmix.year,
                            directorsmix.movie_id, directorsmix.person_id).all()

    # Close the session
    session.close()

    # Convert "rows" to a normal list
    results_jsonifiable = []
    for row in results:
        row_list = []
        for element in row:
            if element is None:
                pass
            elif not (isinstance(element, int) | isinstance(element, str)):
                row_list.append(float(element))
            else:
                row_list.append(element)
        row_dict = dict(zip(["id", "title", "year", "movie_id", "person_id"], row_list))
        results_jsonifiable.append(row_dict)

    return json.dumps({'directors': results_jsonifiable})

if __name__ == '__main__':
    app.run(debug=True)