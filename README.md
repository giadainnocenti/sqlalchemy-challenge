# sqlalchemy-challenge
In this repository, an [analysis of weather data](climate_starter.ipynb) for the Hawaii is performed using AQLAlchemy and Pandas and matplotlib to create the data visualization. Finally, an [API web-app](app.py) was created by using Flask.

## 1. Weather data analysis for Hawaii
SQLAlchemy was connected to the database ([hawaii.sqlite](hawaii.sqlite)) and the following results were obtained:

- A query was designed to retrieve the last 12 months of precipitation data and  the results were plotted. \
![precipitation](./output/bar_precipitation.png)\

- A query to identify the most active weather station was developed and the lowest, highest, and average temperature were evaluated.\
                        The most active satation was USC00519281: \
                        Lowest temperture recorded: 54.0\
                        Highest temperature recorded: 85.0\
                        Average temperature: 71.7\
- The data were filtered to retrieve the last 12 months of temperature observation data (TOBS) for the most active station and an histogram was created.\
 ![precipitation](./output/histogram_T.png)\

