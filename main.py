"""
Created by: Alvin Hartanto
Version   : 0.1.2
Date      : 26/08/2022
-=-=-=-=-=-=-=-=-=-=-
A general API for counting web views hosted on Replit.com.
> Current code is under evaluation and testing

-=-=-=-=-=-=-=-=-=-=-
Credit on basecode goes to @badvillain01
"""
from gevent import monkey
monkey.patch_all()

from flask import Flask, jsonify
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
#from flask_compress import Compress
#from threading import Thread
import dataHandler

APIapp = Flask("")
CORS(APIapp)

#compress = Compress()
#compress.init_app(APIapp)

@APIapp.route('/')
def home():
  return "Alive and running"



@APIapp.route('/api/viewcount/', methods=['GET'])
def viewCount():
  data = dataHandler.readData('SampleViewCount')

  return jsonify({"Sample":data})



@APIapp.route('/api/viewcount/add/', methods=['POST'])
def viewCountAdd():
  data = dataHandler.addIntToData('SampleViewCount', 1)

  return jsonify({"Sample":data})



@APIapp.route('/api/viewcount/add/<Name>', methods = ['POST'])
def count(Name):
  objName = Name + "ViewCount"
  
  data = dataHandler.addIntToData(objName, 1)
  
  return jsonify({"name":Name, "result":data})



@APIapp.route('/api/viewcount/retrieve/<Name>', methods = ['GET'])
def retrieve(Name):
  objName = Name + "ViewCount"
  reader = dataHandler.readData(objName)

  return jsonify({"name":Name, "viewCount": reader})



http_server = WSGIServer(('0.0.0.0', 8080), APIapp)
http_server.serve_forever()
