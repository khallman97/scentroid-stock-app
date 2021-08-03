# Scentroid-stock-app
## Kyle Hallman


The goal of this application was to create a simeple API backend using python and a react front end. The front end was to send the api 
a timezone and a start and end date, which then the api would return the data with the updated timezones and stock price data.


## API
The api was done using flask in python. It takes in a POST request to the url/StockData. It requires a body
with the timezone, startdate, and enddate as json. It then calculates the time difference in hours, updates the dates
to the user definded timezone, then generates stock data (Randomly). An array of stock data and updated dates is then
returned back from the POST request.

Unit testsing was done is pytest. Feel free to use python -m pytest to run the tests.


## Front End
The front end was done in react, It is just a simple layout with some form option on the side
and a graph div on thr left hand side. The graph will not show until the user has submitted their 
options. After this a graph will appear with the data.

Unit testing was done with jest feel free to use react test to run them.

## Docker
A docker compose was created to run the application. It is located in the main folder and can be run using docker-compose up
