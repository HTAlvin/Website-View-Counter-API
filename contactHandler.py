import json
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def loadUser():
  ## load the key as JSON
  credJson = json.loads(os.environ['superSecretContact'])
  ## create credentials
  user = service_account.Credentials.from_service_account_info(
        credJson, scopes=['https://www.googleapis.com/auth/spreadsheets'])
  return user


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


def writeData(newDataJson):
  currentData = readData()

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