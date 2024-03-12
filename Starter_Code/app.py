# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Find the most recent date in the data set.
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    # Calculate the date one year from the last date in data set.
    recent_date = dt.datetime.strptime("2017-08-23", '%Y-%m-%d')
    last_12_months = recent_date - dt.timedelta(days=365)    

    #convert query results into a dictionary with the date as the key and prcp as the value
    precipitation_dict = {}
    for date, prcp in precipitation_data:
        precipitation_dict[date] = prcp

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()

    return jsonify(stations)

@app.route("/api/v1.0/stations")

if __name__ == '__main__':
    app.run(debug=True)