##############################################################################
##
## Dan C. Climate App - Utilizing Python, Pandas, Flask, SQLAlchemy and SQLite
##
##############################################################################
from flask import Flask, jsonify, json
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd
import datetime as dt

# Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()
# reflect an existing database into a new model
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

hello_dict = {"Hello": "World!"}

@app.route("/")
def welcome():
    # List all the available routes
    return (
        f"Welcome to Dan C's Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/'<'start'>'<br/>"
        f"/api/v1.0/'<'start'>'/'<'end'>'<br/>"
    )
  
@app.route("/api/v1.0/precipitation")
def precipitation():   
    # Open a new db session for each request
    session = Session(engine)  
    
    query = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date = dt.datetime.strptime(query.date, "%Y-%m-%d") - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > date)
    dfres = pd.read_sql(results.statement, results.session.bind)   
    jsonfiles = json.loads(dfres.to_json(orient='records'))
    
    # Flask threads are sensitive to db connections, no sharing apparently
    session.close()
    return jsonify(jsonfiles)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    results = session.query(Station)
    dfres = pd.read_sql(results.statement, results.session.bind)   
    jsonfiles = json.loads(dfres.to_json(orient='records'))
    
    session.close()
    return jsonify(jsonfiles)  

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    query = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date = dt.datetime.strptime(query.date, "%Y-%m-%d") - dt.timedelta(days=365)
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > date).filter(Measurement.station == 'USC00519281') 
    dfres = pd.read_sql(results.statement, results.session.bind)  
    jsonfiles = json.loads(dfres.to_json(orient='records'))
    
    session.close()
    return jsonify(jsonfiles)  

@app.route("/api/v1.0/<start>")
def start_(start):    
    session = Session(engine)
    
    date = start
    results_min = session.query(Measurement.station, Measurement.date,func.min(Measurement.tobs).label("TMIN")).filter(Measurement.date > date)
    dfres_min = pd.read_sql(results_min.statement, results_min.session.bind)
    results_avg = session.query(Measurement.station, Measurement.date,func.avg(Measurement.tobs).label("TAVG")).filter(Measurement.date > date)
    dfres_avg = pd.read_sql(results_avg.statement, results_avg.session.bind)
    results_max = session.query(Measurement.station, Measurement.date,func.max(Measurement.tobs).label("TMAX")).filter(Measurement.date > date)
    dfres_max = pd.read_sql(results_max.statement, results_max.session.bind)
    dfres = pd.concat([dfres_min, dfres_avg, dfres_max])
    jsonfiles = json.loads(dfres.to_json(orient='records'))
    
    session.close()
    
    return jsonify(jsonfiles)  

@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date,end_date):
    
    
    return jsonify(hello_dict)

if __name__ == "__main__":
    app.run(debug=True)

