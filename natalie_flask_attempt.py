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

# ------------------------------------------------------------
# Setup database

# Create engine
engine = create_engine("sqlite:///movies.db")

# reflect an existing database into a new model
Base = automap_base()

# Reflest the tables
Base.prepare(engine, reflect=True)

# Add primary key to ratings
with engine.connect() as con:
    con.execute('ALTER TABLE ratings ADD PRIMARY KEY (`ID_column`);')

# Save references to the tables
movies = Base.classes.movies
people = Base.classes.people
# ratings = Base.classes.ratings
# stars = Base.classes.stars
# directors = Base.classes.directors

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
        f"/api/movie_title<br/>"
    )

@app.route("/api/movies_load/")
def movies_load():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(movies.title, movies.year, movies.id).all()

    # Close the session
    session.close()

    # Convert "rows" to a normal list
    results_jsonifiable = []
    for row in results:
        row_list = []
        for element in row:
            if not (isinstance(element, int) | isinstance(element, str)):
                row_list.append(float(element))
            else:
                row_list.append(element)
        results_jsonifiable.append(row_list)

    return json.dumps(results_jsonifiable)

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
        results_jsonifiable.append(row_list)

    return json.dumps(results_jsonifiable)

# @app.route("/api/ratings_load/")
# def ratings_load():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)
#
#     # Query all passengers
#     results = session.query(ratings.movie_id, ratings.rating, ratings.votes).all()
#
#     # Close the session
#     session.close()
#
#     # Convert "rows" to a normal list
#     results_jsonifiable = []
#     for row in results:
#         row_list = []
#         for element in row:
#             if element is None:
#                 pass
#             elif not (isinstance(element, int) | isinstance(element, str)):
#                 row_list.append(float(element))
#             else:
#                 row_list.append(element)
#         results_jsonifiable.append(row_list)
#
#     return json.dumps(results_jsonifiable)


@app.route("/api/movie_title/<title>")
def movie_title(title):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Replace underscores with spaces and capitalize
    title = title.replace("&", " ").title()
    print(title)

    # Query all passengers
    results = session.query(movies.title, movies.year, movies.id).filter(movies.title == title).all()[0]

    # Close the session
    session.close()

    # Define dictionary
    movie = dict(zip(["title", "year", "id"], results))

    # Convert decimal to float
    movie['year'] = float(movie['year'])

    return jsonify(movie)

if __name__ == '__main__':
    app.run(debug=True)