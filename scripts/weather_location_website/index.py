from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import requests
import config

# information for openweather api
api_key = config.api_key
base_url = 'http://api.openweathermap.org/data/2.5/weather?'

# url for openaq.org
aq_url = 'https://api.openaq.org/v1/latest?coordinates='

app = Flask(__name__)

def startDatabase():

   # connection used to connect to database file
   connection = sqlite3.connect('database.db')

   # used to execute commands to database
   c = connection.cursor()

   # Create table
   c.execute('''
      CREATE TABLE IF NOT EXISTS locations(latitude INTEGER,
      longitude INTEGER,
      temperature INTEGER,
      pressure INTEGER,
      humidity INTEGER,
      min_temp INTEGER,
      max_temp INTEGER,
      ozone TEXT,
      ozone_level INTEGER,
      units TEXT)
      ''')

   # Save the changes
   connection.commit()

   return c, connection

@app.route('/')
def hello():
   c, conn = startDatabase()
   endDatabase(conn)
   return render_template('index.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/database')
def database():
   return render_template('database.html')

@app.route('/weather_data', methods = ['POST'])
def weatherData():

   # get data from client
   data = request.get_json()

   # unpack data
   lat = data['lat']
   lon = data['lon']

   # get weather through coordinates
   complete_url = base_url + 'lat=' + str(lat) + '&lon=' + str(lon) + '&appid=' + api_key + '&units=imperial'
   weather = requests.get(complete_url).json()
   weather = weather['main']

   # get air quality data
   aq = aq_url + str(lat) + ',' + str(lon)
   aq = requests.get(aq).json()
   aq = aq['results'][0]
   aq = aq['measurements'][0]

   # clean up air data
   aq.pop('sourceName')
   aq.pop('averagingPeriod')

   # combine air and weather data
   # combine two dictionaries
   final_data = {**weather, ** aq}

   # restart database
   c, conn = startDatabase()

   # Insert a row of data
   c.execute('''
      INSERT INTO locations(latitude, longitude,
      temperature,
      pressure,
      humidity,
      min_temp,
      max_temp,
      ozone,
      ozone_level,
      units)
      VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (lat, lon,
      final_data['temp'],
      final_data['pressure'],
      final_data['humidity'],
      final_data['temp_min'],
      final_data['temp_max'],
      final_data['parameter'],
      final_data['value'],
      final_data['unit'])
   )

   # save changes
   conn.commit()

   # close database
   endDatabase(conn)

   final_data = json.dumps(final_data)

   return final_data

@app.route('/database_info', methods = ['GET'])
def info():
   c, conn = startDatabase()
   data = checkDatabase(c, conn)
   endDatabase(conn)

   return jsonify(data)

def checkDatabase(c, conn):
   data = []
   for row in c.execute('SELECT * FROM locations'):
      # print(row)
      data.append(row)

   return data

def endDatabase(connection):
   connection.close()
   return