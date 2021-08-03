#API made using flask with the below libraies used to integreate the features
import flask 
from flask import request, jsonify
from flask_cors import CORS, cross_origin
import math
import numpy as np
import pytz
import datetime

#Create flask app and enable CORS so their is no CORS issues
app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

    
# Stock Data route is a post method that when called requies 3 items in the content
# timezone: timezone for the dates to be parsed in
# startdate: the date to start the data
# enddate: the end date for the data 
# The function takes the 3 inputs provided through the post method, sets the dates to
# UTC and rounds down to the nearest hour. It then calls the build_date_and_data_array function
# which will return stock data (randomly generated) as an array and an array of dates, by hour.
# The function then returns a JSON response of the data
@app.route('/StockData', methods=['POST'])
@cross_origin(origin='*')   #cross_orgin for CORS
def return_stock_data():
    # parse the content from the post into variables if any of the fields are missing 
    # in the context then return an error response with status 500 
    content = request.json
    timezone = ""
    start_date = ""
    end_date = ""
    try:
        timezone = content["timezone"]
        start_date = content["startDate"]
        end_date = content["endDate"]
    except:
        response = jsonify(
            error = "Missing field please make sure startDate, endDate and timezone are included"
        )
        return response, 400

    #if any of the content is null return error 400, and json message
    if(timezone == "" or start_date == "" or end_date == ""):
        response = jsonify(
            error = "Please ensure all fields are filled"
        )
        return response, 400

    # Check that the time zone is valid
    if(timezone != "UTC" and timezone != "Toronto" and timezone != "Tokyo"):
        response = jsonify(
            error = "Please check you have a correct timezone"
        )
        return response, 400

    #localize dates to UTC to keep other conversions simple
    utc_timezone = pytz.timezone("UTC")
    s_date = utc_timezone.localize(hour_rounder(datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M'))) 
    e_date = utc_timezone.localize(hour_rounder(datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M')))

    #Check start date is less then end date
    if(s_date > e_date):
        response = jsonify(
            error = "Make sure start date is less then end date"
        )
        return response, 400
    
    #Call the build_date_and_data_array function to generate dates and data
    rand_stock_prices , date_hour_arr = build_date_and_data_array(s_date, e_date, timezone)
    #Try to return the response as json, if it doesnt work return empty array back.
    response = jsonify(
        date_axis = date_hour_arr,
        data_axis = rand_stock_prices.tolist()
    )
    return(response)

# Function to round down to the nearest hour, takes a date as input and uses the repace function 
# with the date rounded to the nearest hour
def hour_rounder(date):
    return (date.replace(second=0, microsecond=0, minute=0, hour=date.hour)
               +datetime.timedelta(hours=date.minute//59))

# Function to build a data array of random numbers to mimic stock prices and date array from
# user definded start and end dates. The fucntion takes in the start date, end date and timezone 
# the user definded. The function looks for the timezone the user definded, and updates the dates 
# to the correct timezone while the array is built. This does take into account daylight savings
# as well
def build_date_and_data_array(start_date, end_date, timezone):
    #Define utc from pytz libray and the format for the dates
    utc = pytz.utc
    fmt = '%Y-%m-%d %H:%M %Z%z'
    # if the timezone is UTC, find the time delta, then the total hours based off the delta, then
    # create two arrays both of the size of the number of hours, one array called rand_stock_prices
    # which uses numpy to generate random numbers between 300,500 (no importance just selected this
    # range) and the other array of the date array also the size of the total hours with one hour added
    # to the start date every iteration
    if(timezone == "UTC"):
        date_delta = end_date - start_date
        total_hours = math.floor(((date_delta.total_seconds())/60)/60)
        rand_stock_prices = np.random.randint(300,500,total_hours + 1)
        date_hour_arr = [((start_date + datetime.timedelta(hours=i))).strftime(fmt) for i in range(total_hours + 1)]
        return(rand_stock_prices, date_hour_arr)

    # if the timezone is Tokyo, replace the timezone in the start and end dates, then follow the same steps
    # as the UTC using the new dates. When creating the date array however, apply the function astimezone then use 
    # the defined timezone from japan according the pytz libray
    elif(timezone == "Tokyo"):
        jst = pytz.timezone('Japan')
        start_date_1 = start_date.replace(tzinfo=utc)
        end_date_1 = end_date.replace(tzinfo=utc)
        date_delta = end_date_1 - start_date_1
        total_hours = math.floor(((date_delta.total_seconds())/60)/60)
        rand_stock_prices = np.random.randint(300,500,total_hours + 1)
        date_hour_arr = [((start_date_1 + datetime.timedelta(hours=i)).astimezone(jst)).strftime(fmt) for i in range(total_hours + 1)]
        return(rand_stock_prices, date_hour_arr)

    # if the timezone is Toronto, replace the timezone in the start and end dates, then follow the same steps
    # as the UTC using the new dates. When creating the date array however, apply the function astimezone then use 
    # the defined timezone from toronto according the pytz libray, this does factor daylight savings (EST -> EDT & EDT -> EST)
    elif(timezone == "Toronto"):
        est = pytz.timezone('US/Eastern')
        start_date_1 = start_date.replace(tzinfo=utc)
        end_date_1 = end_date.replace(tzinfo=utc)
        date_delta = end_date_1 - start_date_1
        total_hours = math.floor(((date_delta.total_seconds())/60)/60)
        rand_stock_prices = np.random.randint(300,500,total_hours + 1)
        date_hour_arr = [((start_date_1 + datetime.timedelta(hours=i)).astimezone(est)).strftime(fmt) for i in range(total_hours + 1)]
        return(rand_stock_prices, date_hour_arr)

    # if the timezone is not one of the above then return two empty arrays
    else:
        return ([],[])

app.run(host="0.0.0.0", port=80,debug=True)
