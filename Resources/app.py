import datetime as dt
import numpy as np
import pandas as pd

# dependencies we need for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# dependencies that we need for Flask
from flask import Flask, jsonify

# set up database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a sessioin link from python to our database
session = Session(engine)

# create a Flask application called "app"
app = Flask(__name__)
# define the welcome route
# routes have to go after the app = Flask(__name__) line of code
@app.route("/")

# create a function welcome() with a return statement
# add the precipitation, stations, tobs, and temp routes
# use f-strings to display them
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/temp/start/end
    ''')

# create the route for precip analysis
@app.route("/api/v1.0/precipitation")

# create the precipitation() function.
# calc the date one year ago from the most recent date in the database
# query to get the date and precipitation for the previous year
# use jsonify() to format our results into a JSON structured file
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# create the route for stations
@app.route("/api/v1.0/stations")

# ceate a new function called stations()
# unraveling our results into a one-dimensional array: 
# use function np.ravel(), with results as our parameter
# convert our unraveled results into a list
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# create a route for temperature observations for past year
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# route to report on min, ave, and max temperatures
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#create function
# add start and end parameter
# query to select the min, ave, and max temps from SQLite database
# unravel the results into a one-dimensional array and convert them to a list
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)