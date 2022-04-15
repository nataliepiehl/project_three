# ------------------------------------------------------------
# Import modules
import json
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
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