import json
import os
import urllib
import requests
import sqlite3
def get_median_income_data(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS cityToCountyKey (city INTEGER PRIMARY KEY, countyID INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS incomePerCounty (countyID INTEGER , county TEXT PRIMARY KEY, medianHouseholdIncome INTEGER)')
    url = 'https://parseapi.back4app.com/classes/Uszipcode_US_Zip_Code?limit=50000&order=Primary_city&keys=Primary_city,County,State'
    headers = {
        'X-Parse-Application-Id': 'dIfUjO5efCPvpT4Gy3B54F6kEsdU8l2kdHyyh9Db', # This is your app's application id
        'X-Parse-REST-API-Key': 'qHNE45amR6gIowAdzkNyHonTUswYKcaGOMIxjvLB' # This is your app's REST API key
    }
    zipdata = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) 
    cur.execute('SELECT * FROM players')
    rows = cur.fetchall()
    cur.execute("SELECT COUNT(city) from cityToCountyKey")
    result=cur.fetchone()
    oldCount=result[0]
    countyCount = 0
    for row in rows:
        for object in zipdata['results']:
            cur.execute('SELECT birthCity FROM cities WHERE cityID =' + str(row[1]))
            cityName=cur.fetchone()
            cur.execute('SELECT birthState FROM states WHERE stateID =' + str(row[2]))
            stateName=cur.fetchone()
            if object['Primary_city'] == cityName[0] and object['State'] == stateName[0]:
                if 'County' in object:
                    new = object['County'].replace(" ", "%20")
                    countyCount+=1
                    cur.execute(f"INSERT OR IGNORE INTO cityToCountyKey (city, countyID) VALUES (?,?)", (row[1],countyCount))
                    cur.execute("SELECT COUNT(city) from cityToCountyKey")
                    result=cur.fetchone()
                    newCount=result[0]
                    if newCount - oldCount > 24:
                        break
                    url2 = "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/ACS_Median_Income_by_Race_and_Age_Selp_Emp_Boundaries/FeatureServer/1/query?where=NAME" + "%20" + "%3D%20'" + new + "'&outFields=NAME,State,B19049_001E&returnGeometry=false&outSR=4326&f=json"
                    censusData = json.loads(requests.get(url2).content.decode('utf-8')) 
                    if 'features' in censusData:
                        if len(censusData['features']) != 0:
                            income = censusData['features'][0]['attributes']['B19049_001E']
                            cur.execute(''' INSERT OR IGNORE INTO incomePerCounty (
                            countyID, county, medianHouseholdIncome) VALUES (?,?,?)''', 
                            (countyCount, object['County'], income))
                    conn.commit()
def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'players.db', timeout= 10)
    cur = conn.cursor()
    get_median_income_data(cur, conn)
    cur.close()
main()
