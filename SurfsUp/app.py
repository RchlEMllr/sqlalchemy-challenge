# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///sqlalchemy-challenge\SurfsUp\Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#I just need to put this up here so it's done for all the routes, don't mind me
recent  = dt.date(2017,8,23)
year_ago = recent - dt.timedelta(days=365)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """All available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    """Most recent precipitation data."""
#Query copied from my climate_starter
    results = session.query(Measurement.date, Measurement.prcp).\
    filter((func.strftime(Measurement.date) <= recent) & 
           (func.strftime(Measurement.date) >= year_ago)).all()
    session.close()

    recent_prcp = {date: prcp for date, prcp in results}
    return jsonify(recent_prcp)
  

@app.route("/api/v1.0/stations")
def stations():
    """All stations in available data."""
    results = session.query(Station.name).all()
    session.close()

    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temps():
    """Temperature observations from Waihee, the most active station."""
#Query copied from my climate_starter
    results = session.query(Measurement.date, Measurement.tobs).\
        filter((func.strftime(Measurement.date) <= recent) & 
           (func.strftime(Measurement.date) >= year_ago) &
           (Measurement.station =='USC00519281')).all()
    session.close()

    most_active = list(np.ravel(results))
    return jsonify(most_active)

@app.route("/api/v1.0/<start>")
def point_a(start):
    """Minimum, average and maximum temperatures from a specified date."""
#Query copied from my climate_starter
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter((func.strftime(Measurement.date) == start)).all()
    session.close()

    start_temps = list(np.ravel(results))
    return jsonify(start_temps)

@app.route("/api/v1.0/<start>/<end>")
def point_a_to_b(start, end):
    """Minimum, average and maximum temperatures from a specified date range."""
#Query copied from my climate_starter   
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter((func.strftime(Measurement.date) >= start) & (func.strftime(Measurement.date) <= end)).all()
    session.close()

    temp_range = list(np.ravel(results))
    return jsonify(temp_range)

if __name__ == '__main__':
    app.run(debug=True)
