from flask import json
import pytest
import requests


from stock_api import *

# default url for api testing
apiUrl = "http://127.0.0.1:5000/StockData"

#Test data for UTC
test_data_UTC = {
    'timezone' : 'UTC',
    'startDate' : '2021-08-3T15:36',
    'endDate' : '2021-08-5T15:36'
}

#Test data for toronto, incoperates daylight savings
test_data_Toronto = {
    'timezone' : 'Toronto',
    'startDate' : '2021-03-3T15:36',
    'endDate' : '2021-03-15T15:36'
}

#Test data for tokyo
test_data_Tokyo = {
    'timezone' : 'Tokyo',
    'startDate' : '2021-05-3T15:36',
    'endDate' : '2021-05-10T15:36'
}

utc_timezone = pytz.timezone("UTC")
jst = pytz.timezone('Japan')
est = pytz.timezone('US/Eastern')

def test_hour_rounder():
    date = datetime.datetime.strptime('2021-05-3T15:36', '%Y-%m-%dT%H:%M')
    date_hour_rounded = hour_rounder(date)
    assert(date_hour_rounded.strftime('%Y-%m-%d %H:%M') == "2021-05-03 15:00")

# test that the date and data array are the same length
# they need to be the same in order for data to graph properly
# Verify this with the 3 different test datas and time zones for 
# better coverage of the function
def test_date_and_data_same_length():
    response_data = requests.post(apiUrl, json = test_data_UTC)
    data = json.loads(response_data.text)
    assert(len(data["data_axis"]) == len(data["date_axis"]))

    response_data = requests.post(apiUrl, json = test_data_Toronto)
    data = json.loads(response_data.text)
    assert(len(data["data_axis"]) == len(data["date_axis"]))

    response_data = requests.post(apiUrl, json = test_data_Tokyo)
    data = json.loads(response_data.text)
    assert(len(data["data_axis"]) == len(data["date_axis"]))


# Test that the user provided dates are the start and end range of the data array 
# that is returned in the utc timezone, and checks the timezone is correct as well
def test_dates_in_range_of_entry_UTC():
    # get the data from post request as json type for UTC
    response_data = requests.post(apiUrl, json = test_data_UTC)
    data = json.loads(response_data.text)
    # format real start and end date using hour rounder
    date_s = datetime.datetime.strptime('2021-08-3T15:36', '%Y-%m-%dT%H:%M')
    date_e = datetime.datetime.strptime('2021-08-5T15:36', '%Y-%m-%dT%H:%M')
    date_hour_rounded_s = hour_rounder(date_s)
    date_hour_rounded_e = hour_rounder(date_e)
    # localize timezone to utc
    s_date = utc_timezone.localize(date_hour_rounded_s)
    e_date = utc_timezone.localize(date_hour_rounded_e)
    # Check start and end date of data
    assert(data["date_axis"][0] == s_date.strftime('%Y-%m-%d %H:%M %Z%z'))
    assert(data["date_axis"][len(data["date_axis"])-1] == e_date.strftime('%Y-%m-%d %H:%M %Z%z'))

# Test that the user provided dates are the start and end range of the data array 
# that is returned in the toronto timezone, and checks the timezone is correct as well
# dates also check that the daylight savings was taken into effect
def test_dates_in_range_of_entry_Toronto():
    # get the data from post request as json type for EST this also checks daylight savings
    response_data = requests.post(apiUrl, json = test_data_Toronto)
    data = json.loads(response_data.text)
    # format real start and end date using hour rounder
    date_s = datetime.datetime.strptime('2021-03-3T15:36', '%Y-%m-%dT%H:%M')
    date_e = datetime.datetime.strptime('2021-03-15T15:36', '%Y-%m-%dT%H:%M')
    date_hour_rounded_s = hour_rounder(date_s)
    date_hour_rounded_e = hour_rounder(date_e)
    # localize timezone to utc
    s_date = utc_timezone.localize(date_hour_rounded_s)
    e_date = utc_timezone.localize(date_hour_rounded_e)
    # Check start and end date of data
    assert(data["date_axis"][0] == (s_date.astimezone(est)).strftime('%Y-%m-%d %H:%M %Z%z'))
    assert(data["date_axis"][len(data["date_axis"])-1] == (e_date.astimezone(est)).strftime('%Y-%m-%d %H:%M %Z%z'))

# Test that the user provided dates are the start and end range of the data array 
# that is returned in the tokyo timezone, and checks the timezone is correct as well
def test_dates_in_range_of_entry_Tokyo():
    # get the data from post request as json type for JST
    response_data = requests.post(apiUrl, json = test_data_Tokyo)
    data = json.loads(response_data.text)
    # format real start and end date using hour rounder
    date_s = datetime.datetime.strptime('2021-05-3T15:36', '%Y-%m-%dT%H:%M')
    date_e = datetime.datetime.strptime('2021-05-10T15:36', '%Y-%m-%dT%H:%M')
    date_hour_rounded_s = hour_rounder(date_s)
    date_hour_rounded_e = hour_rounder(date_e)
    # localize timezone to utc
    s_date = utc_timezone.localize(date_hour_rounded_s)
    e_date = utc_timezone.localize(date_hour_rounded_e)
    # Check start and end date of data
    assert(data["date_axis"][0] == (s_date.astimezone(jst)).strftime('%Y-%m-%d %H:%M %Z%z'))
    assert(data["date_axis"][len(data["date_axis"])-1] == (e_date.astimezone(jst)).strftime('%Y-%m-%d %H:%M %Z%z'))

# Test that an error message and status 400 is returned when their are missing fields in the post data
# Note: this means that x data was not in the json not that the data was set to "" or null
def test_missing_content_fields():
    test_data_missing = {
        'startDate' : '2021-05-3T15:36',
        'endDate' : '2021-05-10T15:36'
    }
    response_data = requests.post(apiUrl, json = test_data_missing)
    assert '{"error":"Missing field please make sure startDate, endDate and timezone are included"}\n' ==  response_data.text
    assert 400 == response_data.status_code 

# Test that an error message and status 400 is returned when their are empty fields in the post data
def test_empty_content_fields():
    test_data_missing = {
        'timezone' : '',
        'startDate' : '',
        'endDate' : '2021-05-10T15:36'
    }
    response_data = requests.post(apiUrl, json = test_data_missing)
    assert '{"error":"Please ensure all fields are filled"}\n' ==  response_data.text
    assert 400 == response_data.status_code 

# Test that an error message and status 400 is returned when a non-valid timezone is entered
def test_valid_time_zone():
    test_data_missing = {
        'timezone' : 'not-valid',
        'startDate' : '2021-05-3T15:36',
        'endDate' : '2021-05-10T15:36'
    }
    response_data = requests.post(apiUrl, json = test_data_missing)
    assert '{"error":"Please check you have a correct timezone"}\n' ==  response_data.text
    assert 400 == response_data.status_code 

# Test that an error message and status 400 is returned when the start date is after the end date
def test_valid_start_date():
    test_data_missing = {
        'timezone' : 'UTC',
        'startDate' : '2021-05-15T15:36',
        'endDate' : '2021-05-10T15:36'
    }
    response_data = requests.post(apiUrl, json = test_data_missing)
    assert '{"error":"Make sure start date is less then end date"}\n' ==  response_data.text
    assert 400 == response_data.status_code 
