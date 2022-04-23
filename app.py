# ------------------------------------------------------------
# Import modules
import json
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
        f"/api/ratings_load/<br/>"
        f"/api/popular_people_load/<br/>"
        f"/api/person_load/<person><br/>"
    )

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


@app.route("/api/popular_people_load/")
def popular_people_load():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all movies
    movie_results = session.query(ratingmix.id, ratingmix.title, ratingmix.year,
                                  ratingmix.movie_id, ratingmix.rating, ratingmix.votes).all()

    # Sort by vote count
    movie_results = sorted(movie_results, key=itemgetter('votes'), reverse=True)

    # Select for top 1000 movies
    movie_results = movie_results[0:1000]

    # Move Harrison Ford to front
    movie_results.insert(0, movie_results.pop(29))

    # Query for stars in these movies
    stars_results = session.query(starsmix.id, starsmix.title, starsmix.year,
                                  starsmix.movie_id, starsmix.person_id).filter(starsmix.movie_id.in_([row[3] for row in movie_results])).all()

    # Query for these people
    results = session.query(people.id, people.name, people.birth).filter(people.id.in_([row[4] for row in stars_results])).all()

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

    return json.dumps({'popular_people': results_jsonifiable})

@app.route("/api/person_load/<person>")
def person_load(person):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Format person
    person = person.replace("&", " ").title()

    # Query for person ID
    person_id = session.query(people.id, people.name, people.birth).filter(people.name == person).all()

    # Query for stars in these movies
    results = session.query(starsmix.id, starsmix.title, starsmix.year,
                            starsmix.movie_id, starsmix.person_id, ratingmix.votes, ratingmix.rating).\
                filter(starsmix.person_id == person_id[0][0]).\
                join(ratingmix, starsmix.movie_id == ratingmix.movie_id).all()

    # Close the session
    session.close()

    # Convert "rows" to a normal list
    results_jsonifiable = []
    for count, row in enumerate(results):
        row_list = []
        for element in row:
            if element is None:
                pass
            elif not (isinstance(element, int) | isinstance(element, str)):
                row_list.append(float(element))
            else:
                row_list.append(element)
        row_dict = dict(zip(["id", "title", "year", "movie_id", "person_id", "votes", "rating"], row_list))
        # results_jsonifiable.append({f"r{count}": row_dict})
        results_jsonifiable.append(row_dict)

    return json.dumps({'person_movies': results_jsonifiable})

if __name__ == '__main__':
    app.run(debug=True)