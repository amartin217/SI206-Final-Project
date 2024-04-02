import json
import os
import urllib
import requests
import sqlite3

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'players.db')
cur = conn.cursor()
cur.execute(''' CREATE TABLE IF NOT EXISTS players (name TEXT PRIMARY KEY, birthCity TEXT, birthState TEXT, salary INTEGER)''')
cur.execute(''' CREATE TABLE IF NOT EXISTS geographicInfo (city TEXT PRIMARY KEY, county TEXT, medianHouseholdIncome INTEGER)''')

url = 'https://parseapi.back4app.com/classes/Uszipcode_US_Zip_Code?limit=50000&order=Primary_city&keys=Primary_city,County,State'
headers = {
    'X-Parse-Application-Id': 'dIfUjO5efCPvpT4Gy3B54F6kEsdU8l2kdHyyh9Db', # This is your app's application id
    'X-Parse-REST-API-Key': 'qHNE45amR6gIowAdzkNyHonTUswYKcaGOMIxjvLB' # This is your app's REST API key
}
zipdata = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
players = open('player_info.json', 'r')
data = players.read()
data_dict = json.loads(data)
counties = {}
for player in data_dict:
    if player['BirthCountry'] == "USA":
        city = player['BirthCity']
        state = player['BirthState']
        salary = player["Salary"]
        name = player["FirstName"] + " " + player["LastName"]
        for object in zipdata['results']:
                    if object['Primary_city'] == city and object['State'] == state:
                            if 'County' in object:
                                new = object['County'].replace(" ", "%20")
                                url2 = "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Median_Income_by_Race_and_Age_Selp_Emp_Boundaries/FeatureServer/1/query?where=NAME" + "%20" + "%3D%20'" + new + "'&outFields=NAME,State,B19049_001E&returnGeometry=false&outSR=4326&f=json"
                                censusData = json.loads(requests.get(url2).content.decode('utf-8')) 
                                if 'features' in censusData:
                                    if len(censusData['features']) != 0:
                                        print(censusData['features'][0]['attributes']['B19049_001E'])
                                        income = censusData['features'][0]['attributes']['B19049_001E']
                                        cur.execute(''' INSERT OR IGNORE INTO players (name, 
                                        birthCity, birthState, salary) VALUES (?,?,?,?)''', 
                                        (name,city,state,salary))
                                        conn.commit()
cur.close()

