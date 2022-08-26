"""
Created by: Alvin Hartanto
Version   : 0.1.5
Date      : 26/08/2022
-=-=-=-=-=-=-=-=-=-=-
A general API for counting web views hosted on Replit.com.
> Current code is under evaluation and testing

-=-=-=-=-=-=-=-=-=-=-
Credit on basecode (tutorial) goes to @badvillain01
"""
## Import libraries and initial module setup
from gevent import monkey
monkey.patch_all()

from flask import Flask, jsonify
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
import dataHandler
import timer

## Set up a Flask and allow CORS
APIapp = Flask("")
CORS(APIapp)






## Base API call
@APIapp.route('/')
def home():
  
  return "Alive and running"



## Primary endpoint for reset checks
@APIapp.route('/api/viewcount/check')
def checkDate():
  data = timer.checkNewMonth()
  
  return jsonify({"result":data})

  


## Sample Endpoint for GET method
@APIapp.route('/api/viewcount', methods=['GET'])
def viewCount():
  data = dataHandler.readData('SampleViewCount')

  return jsonify({"Sample":data})




## Sample Endpoint for POST method
@APIapp.route('/api/viewcount/add', methods=['POST'])
def viewCountAdd():
  data = dataHandler.addIntToData('SampleViewCount', 1)

  return jsonify({"Sample":data})




## Primary POST for adding view count
@APIapp.route('/api/viewcount/add/<Name>', methods = ['POST'])
def count(Name):
  # Define Object Name
  objName = Name + "ViewCount"

  # Attempt adding value to data
  data = dataHandler.addIntToData(objName, 1)

  # Send back result as JSON response
  return jsonify({"name":Name, "result":data})




## Primary GET for retrieving counts
@APIapp.route('/api/viewcount/retrieve/<Name>', methods = ['GET'])
def retrieve(Name):
  # Define object name and check the database
  objName = Name + "ViewCount"
  reader = dataHandler.readData(objName)

  if type(reader) == str:
    reader = 0

  # Send ressponse as JSON
  return jsonify({"name":Name, "viewCount": reader})




## Serve API on Replit production server
http_server = WSGIServer(('0.0.0.0', 8080), APIapp)
http_server.serve_forever()
