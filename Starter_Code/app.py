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
    return(
    """List all available api routes."""
    f"Welcome to the Hawaii Climate Analysis API!<br/>"
    f"Available routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
    f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Find the most recent date in the data set.
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    # Calculate the date one year from the last date in data set.
    last_12_months = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)   

    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_12_months).all()

    #convert query results into a dictionary with the date as the key and prcp as the value
    precipitation_dict = {}
    for date, prcp in precipitation_data:
        precipitation_dict[date] = prcp

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # find the most active station
    station_activity = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()
    most_active_station_id = station_activity[0]
    
    # find the last 12 months of temperatures for the most active station
    recent_date = session.query(Measurement.date).\
        filter(Measurement.station == most_active_station_id).\
        order_by(Measurement.date.desc()).first()[0]
    recent_date = dt.datetime.strptime("2017-08-18", '%Y-%m-%d')
    last_12_months = recent_date - dt.timedelta(days=365)

    last_12months_temps = session.query(Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= last_12_months).all()

    #create list of temperatures
    temps_list = [temp[0] for temp in last_12months_temps]

    return jsonify(temps_list)

@app.route("/api/v1.0/<start>")
def start(start):
    temp_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),  func.avg(Measurement.tobs)).\
        filter(Measurement.date >=start).all()
    session.close()

temps = []
for min_temp, max_temp, avg_temp in temp_results:
    temps_dict = {}
    temps_dict['Minimum Temperature'] = min_temp
    temps_dict['Maximum Temperature'] = max_temp
    temps_dict['Average Temperature'] = avg_temp
    temps.append(temps_dict)

    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    temp_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),  func.avg(Measurement.tobs)).\
        filter(Measurement.date >=start).\
        filter(Measurement.date <=end).all()
    session.close()

temps = []
for min_temp, max_temp, avg_temp in temp_results:
    temps_dict = {}
    temps_dict['Minimum Temperature'] = min_temp
    temps_dict['Maximum Temperature'] = max_temp
    temps_dict['Average Temperature'] = avg_temp
    temps.append(temps_dict)

return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)