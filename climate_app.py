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
    return (
        f"Welcome to Dan C's Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/'<'start'>'<br/>"
        f"/api/v1.0/'<'start'>'/'<'end'>'<br/>"
    )
  
@app.route("/precipitation")
def precipitation():   
    query = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date = dt.datetime.strptime(query.date, "%Y-%m-%d") - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > date)
    dfres = pd.read_sql(results.statement, results.session.bind)   
    jsonfiles = json.loads(dfres.to_json(orient='records'))
    return jsonify(jsonfiles)

@app.route("/stations")
def stations():
    results = session.query(Station)
    dfres = pd.read_sql(results.statement, results.session.bind)   
    jsonfiles = json.loads(dfres.to_json(orient='records'))
    return jsonify(jsonfiles)  

@app.route("/tobs")
def tobs():
    query = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date = dt.datetime.strptime(query.date, "%Y-%m-%d") - dt.timedelta(days=365)
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > date).filter(Measurement.station == 'USC00519281') 
    dfres = pd.read_sql(results.statement, results.session.bind)  
    jsonfiles = json.loads(dfres.to_json(orient='records'))
    return jsonify(jsonfiles)  

@app.route("/jsonified")
def jsonified():
    return jsonify(hello_dict)


if __name__ == "__main__":
    app.run(debug=True)

