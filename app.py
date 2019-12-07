import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

from flask import Flask, jsonify
import os
import csv

app = Flask(__name__)

cwd = os.getcwd()
pcrp_data = os.path.join(cwd,"pcrp_df.csv")
station_data = os.path.join(cwd,"station_df.csv")
tobs_data = os.path.join(cwd,"tobs_df.csv")

reader = csv.DictReader(open(pcrp_data, 'r'))
reader1 = csv.DictReader(open(station_data, 'r'))
reader2 = csv.DictReader(open(tobs_data, 'r'))

pcrp_list=[]
station_list=[]
tobs_list =[]

for line in reader:
    pcrp_list.append(line)

for line in reader1:
    station_list.append(line)

for line in reader2:
    tobs_list.append(line)   

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    pcrp_list
    return jsonify(pcrp_list)


@app.route("/api/v1.0/stations")
def station():
    station_list
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_list
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_temps(start):

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    for min, avg, max in results:
        starttemps = {}
        starttemps['Min Temp'] = min 
        starttemps['Avg Temp'] = avg 
        starttemps['Max Temp'] = max 

        return jsonify(starttemps)
    return jsonify({"error": f"Date {start} not found."}), 404

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end):

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    for min, avg, max in results:
        starttemps = {}
        starttemps['Min Temp'] = min 
        starttemps['Avg Temp'] = avg 
        starttemps['Max Temp'] = max 

        return jsonify(starttemps)
    return jsonify({"error": f"Date {start} not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)

