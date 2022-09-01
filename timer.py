"""
Created by: Alvin Hartanto
Version   : 0.1.0
Date      : 26/08/2022

A general reset handler.
Feel free to reuse this source code.
"""
## import libraries
from datetime import date
import json
import dataHandler
import contactHandler

## define filenames
history = "history.json"



## A function to check for reset timing
def checkNewMonth():
  ## opens the history file
  with open(history, "r") as records:
    data = json.load(records)

  ## Reads and check on reset status
  reset = data["reset"]
  
  if reset == "true":
    if date.today().day == 1:
      ## Reset data
      contactHandler.reportVisit("data.json")
      dataHandler.passHistory()
      data["reset"] = "false"

      with open(history, "w") as records:
        json.dump(data, records)
      return "success"

      
    else:
      ## Pass
      return


      
  else: #reset == "false"
    if date.today().day == 2:
      ## Set reset
      data["reset"] = "true"

      with open(history, "w") as records:
        json.dump(data, records)

      return "success"

      
    else:
      ## Pass
      return