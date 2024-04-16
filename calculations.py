import json
import os
import urllib
import requests
import sqlite3
def get_average_median_household_income(cur):
    cur.execute('SELECT birthCity FROM players')
    rows = cur.fetchall()
    MedianIncomeTotal = 0
    count = 0
    for row in rows:
        cur.execute('SELECT countyID FROM cityToCountyKey WHERE city =' + str(row[0]))
        result=cur.fetchone()
        if result != None:
            #print(result[0])
            cur.execute('SELECT medianHouseholdIncome FROM incomePerCounty WHERE countyID =' + str(result[0]))
            income = cur.fetchone()
            if income != None:
                MedianIncomeTotal += int(income[0])
                count+=1
    AvgMedianIncome = MedianIncomeTotal/count
    return AvgMedianIncome
def get_average_salary(cur):
    cur.execute('SELECT salary FROM players')
    rows = cur.fetchall()
    salaryTotal = 0
    count = 0
    for row in rows:
        if row[0] != None:
            salaryTotal += row[0]
            count += 1
    return(salaryTotal/count)
def get_median_salary(cur):
    cur.execute('SELECT salary FROM players')
    rows = cur.fetchall()
    incomes = []
    for row in rows:
        if row[0] != None:
            incomes.append(row[0])
    incomes.sort()
    if(len(incomes) % 2 == 0):
        return ((incomes[len(incomes)//2] + incomes[len(incomes)//2 + 1]) / 2)
    else:
        return incomes[len(incomes) // 2]
def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'players.db')
    cur = conn.cursor()
    fp = open("output.txt",'w')
    fp.write("\nCalculations: \n")
    AMHI = get_average_median_household_income(cur)
    fp.write("Average median household income of birth counties of active NBA players in the 2023 season: " + str(AMHI) + '\n')
    AS = get_average_salary(cur)
    fp.write("Average salary of active NBA players in the 2023 season: " + str(AS) + '\n')
    MS = get_median_salary(cur)
    fp.write("Median salary of active NBA players in the 2023 season: " + str(MS) + '\n')
    cur.close()

main()
        
