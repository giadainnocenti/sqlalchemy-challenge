import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request


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
def home():
    """List all available api routes."""
    return  f'''
            <!DOCTYPE HTML>
            <html>
            <body style = "background-color:#F4FFB4;">
            <h1 style="color:#F4FFB4; font-size:60px;text-align: center; background:blue;">Hawaii Climate API</h1>
            <h2 style="color:black; font-size:20px;">The following information can be found at the reported urls:</h2>
            <ul>
            <li>Precipitation per day: <a href="{root_name}precipitation"> {root_name}precipitation</a></li>
            <li>Station details: <a href="{root_name}stations"> {root_name}stations</a></li>
            <li>Temperature observation for the previous year: <a href="{root_name}tobs">{root_name}tobs</a></li>
            <li>Max, min and average temperature from a certain date: {root_name}yyyy-mm-dd</li>
            <li>Max, min and average temperature for a certain period of time: {root_name}yyyy-mm-dd/yyyy-mm-dd</li>
            </ul>
            </body>
            </html>'''

@app.route(root_name+'precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the JSON representation of your dictionary."""
    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    prcp = []
    for row in session.query(measurement.date, measurement.prcp).all():
        dic = {}
        dic[row[0]] = row[1]
        prcp.append(dic)

    session.close()

    # Convert list of tuples into normal list
    prcp = list(np.ravel(prcp))

    return jsonify(prcp)

@app.route(root_name+'stations')
def stations():
    # Return a JSON list of the stations from the dataset
    session = Session(engine)
    st_list= []
    for row in session.query(station.id, station.station, station.name, station.latitude, station.longitude, station.elevation):
             s_dictionary = {}
             s_dictionary['id'] = row[0]
             s_dictionary['station'] = row[1]
             s_dictionary['name'] = row[2]
             s_dictionary['latitude'] = row[3]
             s_dictionary['longitude'] = row[4]
             s_dictionary['elevation'] = row[5]
             st_list.append(s_dictionary)
    session.close()
    return(jsonify(st_list))

@app.route(root_name+'tobs')
def tobs():
    '''Query the dates and temperature observations of the most
     active station for the last year of data.'''
    session = Session(engine)
    # Get the last date contained in the dataset and date from one year ago
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    previous_year_date = (dt.datetime.strptime(recent_date[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    # Query for the dates and temperature values
    results =   session.query(measurement.date, measurement.tobs).\
                filter(measurement.date >= previous_year_date).\
                order_by(measurement.date).all()

    # Convert to list of dictionaries to jsonify
    tobs_list = []

    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)
    session.close()
    return (jsonify(tobs_list))

sel_temp = [func.min(measurement.tobs),
           func.max(measurement.tobs),
           func.avg(measurement.tobs)]

@app.route(root_name+'<start>')
def start_tobs(start):
    '''Return a JSON list of the minimum temperature, 
    the average temperature, and the max temperature for a given start'''
    session = Session(engine)
    '''When given the start only, calculate `TMIN`, `TAVG`,
        and `TMAX` for all dates greater than and equal to the start date.'''  
        
    for minimum, maximum, average in session.query(*sel_temp).\
          filter(measurement.date >= start).all():
        dic = {
            'Max_Temp': maximum,
            'Min_Temp': minimum,
            'Avg_Temp': average
            }
    session.close()
    return(dic)

@app.route(root_name+'<start>/<end>')
def start_end_tobs(start=None,end=None):
    '''Return a JSON list of the minimum temperature, the average temperature, 
    and the max temperature for a given start or start-end range.'''
    
    session = Session(engine)
    '''When given the start only, calculate `TMIN`, `TAVG`,
        and `TMAX` for all dates greater than and equal to the start date.'''  
    result = session.query(*sel_temp).\
            filter(measurement.date >= start).\
            filter(measurement.date <= end).all()

    for minimum, maximum, average in result:
        dic = {
            'Max_Temp': maximum,
            'Min_Temp': minimum,
            'Avg_Temp': average
            }
    session.close()
    return(dic)
if __name__ == '__main__':
    app.run(debug=True)

