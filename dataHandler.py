"""
Created by: Alvin Hartanto
Version   : 0.1.0
Date      : 26/08/2022

A general data handler.
Feel free to reuse this source code.
"""
import json

jsonName = "data.json"

def readData(variableName):
  with open(jsonName, "r") as database:
    data = json.load(database)

    if not (variableName in data):
      return 'No Entry Found'
    else:
      return data[variableName]




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