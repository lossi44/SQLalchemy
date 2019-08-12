# From Lesson 10, activity #10 code
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.inspection import inspect

import datetime as dt

from flask import Flask, request, jsonify

from flask import flask-moment


#####################################################
# Database Setup
#####################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
#Measurements = Base.classes.measurements

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask setup
app = Flask(__name__)

# 3. Index list of available routes, use Day 3 Activity #8 code
#@app.route("/")

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Avalable Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations"
        f"<br/>"
        f"/api/v1.0/tobs"
        f"<br/>"
        f"/api/v1.0/calc_temps/<start>"
        f"<br/>"
        f"- When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"
    )

    ##################################################    
    @app.route("/api/v1.0/precipitation")
    def precipitation():
        """Return a list of rainfall data for the past 12 months"""
        last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
        last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        rain = session.query(Measurements.date, Measurements.prcp).\
            filter(Measurements.date > last_year).\
            order_by(Measurements.date).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    honolulu_precip = []
    for result in rain:
        row = {"date":"prcp"}
        row ["date"] = results[0]
        row ["prcp"] = float
        honolulu_precip.append(row)
        
    return jsonify(honolulu_precip)

    ##################################################
@app.route("/api/v1.0/stations")
def stations():
   
# Return a JSON list of stations from the dataset
    station_results = session.query(Station.station, Station.station_name).group_by(Station.station).all()
    return jsonify(stations.to_dict())

    ##################################################
    # Query for the dates & temperature observations a year from from the last data point
    @app.route("/api/v1.0/tobs")
    def tobs():
        last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
        last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        temperature = session.query(Measurements.date, Measurements.tobs).\
            filter(Measurements.date > last_year).\
            order_by(Measurements.date).all()

    # Create a list of dicts with `date` and `tobs` as the keys and values
    tobs_totals = []
    for result in temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        temperature_totals.append(row)

    # Return a JSON list of TOBS for the previous year    
    return jsonify(tobs_totals)

######################################################
@app.route("/api/v1.0/<start>")
def trip1(start):

 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

# End
@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):

  # go back one year from start/end date and get Min/Avg/Max temp     
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)    

###################################################### 

if __name__ == "__main__":
    app.run(debug=True)


