import datetime as dt
from datetime import datetime
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station



# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation data"""
    cdate = dt.datetime.now()
    beginDate = cdate.replace(cdate.year - 1)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= beginDate).group_by(Measurement.date).all()
    #results = session.query(Measurement).all()

        # Create a dictionary from the row data and append to a list of all_measurement
    all_measurement = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["date"] = measurement.date
        measurement_dict["prcp"] = measurement.prcp

        all_measurement.append(measurement_dict)

    return jsonify(all_measurement)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of station data"""

    results = session.query(Station).all()

        # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of tobs data"""
    cdate = dt.datetime.now()
    beginDate = cdate.replace(cdate.year - 1)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= beginDate).group_by(Measurement.date).all()
    #results = session.query(Measurement).all()

        # Create a dictionary from the row data and append to a list of all_measurement
    all_measurement = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["date"] = measurement.date
        measurement_dict["tobs"] = measurement.tobs

        all_measurement.append(measurement_dict)

    return jsonify(all_measurement)  


@app.route("/api/v1.0/<start>")
def start(start):
    """Return a list of tobs data"""

    start_date = datetime.strptime(start, '%Y-%m-%d')

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_date).all()    
    

        # Create a dictionary from the row data and append to a list of all_measurement
    all_measurement = []
    
    for measurement in results:
        measurement_dict = {}
        measurement_dict["date"] = measurement.date
        measurement_dict["tobs"] = measurement.tobs

        all_measurement.append(measurement_dict)
    all_measurement_df = pd.DataFrame(all_measurement)  
    aggregate = []  
    aggregate_dict = {}
    aggregate_dict["TMIN"] = all_measurement_df['tobs'].min()
    aggregate_dict["TMAX"] = all_measurement_df['tobs'].max()
    aggregate_dict["TAVG"] = all_measurement_df['tobs'].mean()

    aggregate.append(aggregate_dict)

    return jsonify(aggregate)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return a list of tobs data"""
    start_date = datetime.strptime(start, '%Y-%m-%d')
 
    end_date = datetime.strptime(end, '%Y-%m-%d')
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
  
    

        # Create a dictionary from the row data and append to a list of all_measurement
    all_measurement = []
    
    for measurement in results:
        measurement_dict = {}
        measurement_dict["date"] = measurement.date
        measurement_dict["tobs"] = measurement.tobs

        all_measurement.append(measurement_dict)
    all_measurement_df = pd.DataFrame(all_measurement)  
    aggregate = []  
    aggregate_dict = {}
    aggregate_dict["TMIN"] = all_measurement_df['tobs'].min()
    aggregate_dict["TMAX"] = all_measurement_df['tobs'].max()
    aggregate_dict["TAVG"] = all_measurement_df['tobs'].mean()

    aggregate.append(aggregate_dict)

    return jsonify(aggregate)



if __name__ == '__main__':
    app.run(debug=True)    