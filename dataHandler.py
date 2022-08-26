"""
Created by: Alvin Hartanto
Version   : 0.1.1
Date      : 26/08/2022

A general data handler.
Feel free to reuse this source code.
"""
## Import libraries
import json

## Define the filename here
jsonName = "data.json"
history = "history.json"

## A function that reads the database for a dataset
def readData(variableName):
  with open(jsonName, "r") as database:
    data = json.load(database)

    if not (variableName in data):
      return 'No Entry Found'
    else:
      return data[variableName]



## A function that attempts to add an integer value to a data based on the input
def addIntToData(variableName, value):
  if not ((type(variableName) == str) and (type(value) == int)):
    ## return error for unexpected input type
    return 'Error: Mismatched input type'

  
  check = readData(variableName)

  if check == 'No Entry Found':
    ## create a new variable entry
    with open(jsonName, "r") as database:
      data = json.load(database)

    data[variableName] = value
    with open(jsonName, "w") as database:
      json.dump(data, database)

    return 'Success'
      
  elif not (type(check) in (int, float)):
    ## inapplicable, return error message
    return 'Error: Data object does not contain numbers'
    
  else:
    ##perform addition
    with open(jsonName, "r") as database:
      data = json.load(database)

    data[variableName] += value
    with open(jsonName, "w") as database:
      json.dump(data, database)

    return 'Success'


    
## A function to pass the current data to the history
def passHistory():
  ## Opens both database and history files
  with open(jsonName, "r") as database:
    newData = json.load(database)
  with open(history, "r") as records:
    oldData = json.load(records)

  ## Rewrites history with new data and reset the database
  oldData["history"] = newData
  newData = {"SampleViewCount":1}

  ## Save both files
  with open(history, "w") as records:
    json.dump(oldData, records)
  with open(jsonName, "w") as database:
    json.dump(newData, database)