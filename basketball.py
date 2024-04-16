import json
import os
import urllib
import requests
import sqlite3

API_KEY = "8862562ea1444e62aec5f2589947a6ab"
def get_city_state_dicts(citydict, statedict):
    state_count = 0
    city_count = 0
    url = "http://archive.sportsdata.io/v3/nba/stats/json/players/2023-11-13-15-51.json"
    bballdata = json.loads(requests.get(url,API_KEY ).content.decode('utf-8'))
    for player in bballdata:
        if player['BirthCountry'] == "USA":
            if player['BirthState'] not in statedict:
                statedict[player['BirthState']] = state_count
                state_count += 1
            if player['BirthCity'] not in citydict:
                citydict[player['BirthCity']] = city_count
                city_count += 1
    return citydict, statedict
            


def gather_bballdata(cur,conn, cityDict, stateDict):
    cur.execute(''' CREATE TABLE IF NOT EXISTS players (name TEXT PRIMARY KEY, birthCity INTEGER, birthState INTEGER, salary INTEGER)''')
    url = "http://archive.sportsdata.io/v3/nba/stats/json/players/2023-11-13-15-51.json"
    bballdata = json.loads(requests.get(url,API_KEY ).content.decode('utf-8'))
    cur.execute("SELECT COUNT(name) from players")
    result=cur.fetchone()
    count=result[0]
    # print(count)
    for player in bballdata:
        if player['BirthCountry'] == "USA":
            city = cityDict[player['BirthCity']]
            state = stateDict[player['BirthState']]
            salary = player["Salary"]
            name = player["FirstName"] + " " + player["LastName"]
            cur.execute("SELECT COUNT(name) from players")
            result=cur.fetchone()
            newCount=result[0]
            if newCount - count > 25:
                break
            cur.execute(''' INSERT OR IGNORE INTO players (name, 
            birthCity, birthState, salary) VALUES (?,?,?,?)''', 
            (name,city,state,salary))
            conn.commit()

def fill_states_table(cur,conn, statesDict):
    cur.execute(''' CREATE TABLE IF NOT EXISTS states (stateID INTEGER PRIMARY KEY, birthState TEXT UNIQUE)''')
    cur.execute("SELECT COUNT(stateID) from states")
    result=cur.fetchone()
    count=result[0]
    for entry in statesDict:
        cur.execute('SELECT * FROM players')
        cur.execute(f"INSERT OR IGNORE INTO states (stateID,birthState) VALUES (?,?)", (statesDict[entry],entry))
        cur.execute("SELECT COUNT(stateID) from states")
        result=cur.fetchone()
        newCount=result[0]
        if newCount - count > 24:
            break
    conn.commit()

def fill_cities_table(cur,conn,citiesDict):
    cur.execute(''' CREATE TABLE IF NOT EXISTS cities (cityID INTEGER PRIMARY KEY,birthCity TEXT UNIQUE, stateID INTEGER)''')
    cur.execute("SELECT COUNT(cityID) from cities")
    result=cur.fetchone()
    count=result[0]
    for entry in citiesDict:
        cur.execute(f"INSERT OR IGNORE INTO cities (cityID,birthcity) VALUES (?,?)", (citiesDict[entry],entry))
        cur.execute("SELECT COUNT(cityID) from cities")
        result=cur.fetchone()
        newCount=result[0]
        if newCount - count > 24:
            break
    conn.commit()


def main():
    cities_dict = {}
    states_dict = {}
    cities_dict, states_dict = get_city_state_dicts(cities_dict, states_dict)
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'players.db')
    cur = conn.cursor()
    gather_bballdata(cur,conn, cities_dict, states_dict)
    fill_states_table(cur,conn, states_dict)
    fill_cities_table(cur,conn, cities_dict)
    cur.close()

main()
