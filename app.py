import numpy as np

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
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
root_name = "/api/v1.0/"

@app.route("/")

def welcome():
    """List all available api routes."""
    return  f'''
            <!DOCTYPE HTML>
            <html>
            <body>
            <h1>Hawaii Climate API</h1>
            <h2>The available Routes are:</h2>
            <ul>
            <li><a href="{root_name}precipitation">precipitation - {root_name}precipitation</a></li>
            <li><a href="{root_name}stations">stations - {root_name}stations</a></li>
            <li><a href="{root_name}tobs">tobs - {root_name}tobs</a></li>
            <li>filter by start date - {root_name}[yyyy-mm-dd]</li>
            <li>filter by start and end date - {root_name}[yyyy-mm-dd]/[yyyy-mm-dd]</li>
            </ul>
            </body>
            </html>)'''
            
    


if __name__ == '__main__':
    app.run(debug=True)

