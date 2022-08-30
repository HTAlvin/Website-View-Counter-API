"""
Created by: Alvin Hartanto
Version   : 0.1.3
Date      : 27/08/2022

A handler to communicate with Google Sheets as a method of contact.
"""
## import libraries
import json
import os
from datetime import date

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

## A function to generate credentials for the user
def loadUser():
  ## load the key as JSON
  credJson = json.loads(os.environ['superSecretContact'])
  ## create credentials
  user = service_account.Credentials.from_service_account_info(
        credJson, scopes=['https://www.googleapis.com/auth/spreadsheets'])
  return user


## A function that reads the designated sheet
def readData():
  ## Loads the user with given credentials
  user = loadUser()

  
  try:
    ## attempt to build the service API
    service = build('sheets', 'v4', credentials=user, discoveryServiceUrl=os.environ['discoveryUrl'])

    ## attempt to fetch the result from designated sheets
    result = service.spreadsheets().values().get(
            spreadsheetId=os.environ['sheetID'], range=os.environ['sheetRange']).execute()
    rows = result.get('values', [])
    print(f"{len(rows)} rows retrieved")

    ## pass back the result
    return result

    
  except HttpError as error:
    ## Show error if occurs
    print(f"An error occurred: {error}")
    return "NA"

## A function that attempts to overwrite and update the Google Sheet
def writeData(newDataJson):
  ## attempt to read the sheet
  currentData = readData()

  ## if error in reading the sheet callback error
  if currentData == "NA":
    return "NA"
  
  else:
    ## build the new set
    newSet = [newDataJson['timestamp'], newDataJson['cName'], newDataJson['cEmail'], newDataJson['cSubject'], newDataJson['cContent']]
    
    
    updatedData = currentData['values']
    updatedData.append(newSet)

    
    ## Load the user credentials
    user = loadUser()

    try:
      ## attempt to build the service
      services = build('sheets', 'v4', credentials=user, discoveryServiceUrl=os.environ['discoveryUrl'])
      
      ## attempt to build the body content
      body = {
            'values': updatedData
        }

      ## attempt to update the sheets
      result = services.spreadsheets().values().update(
            spreadsheetId=os.environ['sheetID'], range=os.environ['sheetRange'],
            valueInputOption='RAW', body=body).execute()
      print(f"{result.get('updatedCells')} cells updated.")
      return "success"

      
    except HttpError as error:
      ## show error if occurs
      print(f"An error occurred: {error}")
      return "NA"


## A function to pass visit reports
def reportVisit(fileName):
  with open(fileName, "r") as database:
    data = json.load(database)

  thisMonthVisits = data["htalvingithubViewCount"]

  user = loadUser()

  try:
    service = build('sheets', 'v4', credentials=user, discoveryServiceUrl=os.environ['discoveryUrl'])
    result = service.spreadsheets().values().get(
            spreadsheetId=os.environ['sheetID'], range=os.environ['sheetRange2']).execute()
    rows = result.get('values', [])
    print(f"{len(rows)} rows retrieved")

  except HttpError as error:
    print(f"Error in reporting visits: {error}")
    return "NA"


  try:
    reportTime = str(date.today().month) + "/" + str(date.today().year)

    
    addData = [reportTime, thisMonthVisits]
    updatedData = result['values']
    updatedData.append(addData)

    body = {
      'values':updatedData
    }
    report = service.spreadsheets().values().update(  spreadsheetId=os.environ['sheetID'], range=os.environ['sheetRange2'], valueInputOption='RAW', body=body).execute()
    print(f"{report.get('updatedCells')} cells updated.")
    return "success"

  except HttpError as error:
    print(f"Error in reporting visits: {error}")
    return "NA"