import json
import os
import urllib
import requests
import sqlite3

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'players.db')
cur = conn.cursor()
cur.execute(''' CREATE TABLE IF NOT EXISTS geographicInfo (city TEXT PRIMARY KEY, county TEXT, medianHouseholdIncome INTEGER)''')
cur.execute('SELECT * FROM players')
url = 'https://parseapi.back4app.com/classes/Uszipcode_US_Zip_Code?limit=50000&order=Primary_city&keys=Primary_city,County,State'
headers = {
    'X-Parse-Application-Id': 'dIfUjO5efCPvpT4Gy3B54F6kEsdU8l2kdHyyh9Db', # This is your app's application id
    'X-Parse-REST-API-Key': 'qHNE45amR6gIowAdzkNyHonTUswYKcaGOMIxjvLB' # This is your app's REST API key
}
zipdata = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
for row in cur:
    print(row)
    for object in zipdata['results']:
        if object['Primary_city'] == row[1] and object['State'] == row[2]:
            if 'County' in object:
                new = object['County'].replace(" ", "%20")
                url2 = "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Median_Income_by_Race_and_Age_Selp_Emp_Boundaries/FeatureServer/1/query?where=NAME" + "%20" + "%3D%20'" + new + "'&outFields=NAME,State,B19049_001E&returnGeometry=false&outSR=4326&f=json"
                censusData = json.loads(requests.get(url2).content.decode('utf-8')) 
                if 'features' in censusData:
                    if len(censusData['features']) != 0:
                        income = censusData['features'][0]['attributes']['B19049_001E']
                        print(object['Primary_city'])
                        print(object['County']) 
                        print(income)
                        cur.execute(''' INSERT OR IGNORE INTO geographicInfo (city, 
                        county, medianHouseholdIncome) VALUES (?,?,?)''', 
                        (object['Primary_city'], object['County'], income))
                        conn.commit()
cur.close()
