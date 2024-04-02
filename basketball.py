import json
import os
import urllib
import requests
import sqlite3

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'players.db')
cur = conn.cursor()
cur.execute(''' CREATE TABLE IF NOT EXISTS players (name TEXT PRIMARY KEY, birthCity TEXT, birthState TEXT, salary INTEGER)''')
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
        cur.execute(''' INSERT OR IGNORE INTO players (name, 
        birthCity, birthState, salary) VALUES (?,?,?,?)''', 
        (name,city,state,salary))
        conn.commit()
cur.close()
