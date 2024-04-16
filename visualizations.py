import matplotlib
import matplotlib.pyplot as plt
import json
import os
import urllib
import requests
import sqlite3

#categories
# < 2 mil
# 2 mill - 8 mill
# 8 mil- 14 mil
# 14 mil - 20 mil
# > 40 mil
def plot_salaries(cur):
    y = [" < 2", "$2 -$7", "$7 - $12",  "$12 - $17","$17 - $22", " > 22 " ]
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    cur.execute('SELECT salary FROM players')
    rows = cur.fetchall()
    for row in rows:
        if(row[0] != None):
            if(row[0] < 2000000):
                count1 += 1
            elif(row[0] < 7000000):
                count2 += 1
            elif(row[0] < 12000000):
                count3 += 1
            elif(row[0] < 17000000):
                count4 += 1
            elif(row[0] < 22000000):
                count5 += 1
            else:
                count6 += 1
    x = [count1, count2, count3, count4, count5, count6]
    bars = plt.bar(y,x)
    plt.xlabel('Salary in Millions of Dollars',  fontsize= 13)
    plt.ylabel('Number of Players',  fontsize= 13)
    plt.title("Number of NBA Players per Salary Range",  fontsize= 18)
    bars[0].set_color('red')
    bars[1].set_color('blue')
    bars[2].set_color('red')
    bars[3].set_color('blue')
    bars[4].set_color('red')
    bars[5].set_color('blue')
    plt.show()

    
def plot_median_incomes(cur):
    y = [" 30 - 50", "50- 70", "70 - 90",  "90 - 110","110 - 130", " > 130 " ]
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    cur.execute('SELECT birthCity FROM players')
    rows = cur.fetchall()
    for row in rows:
        cur.execute('SELECT countyID FROM cityToCountyKey WHERE city =' + str(row[0]))
        result=cur.fetchone()
        if result != None:
            #print(result[0])
            cur.execute('SELECT medianHouseholdIncome FROM incomePerCounty WHERE countyID =' + str(result[0]))
            income = cur.fetchone()
            if income != None:
                if(income[0] < 50000):
                    count1 += 1
                elif(income[0] < 70000):
                    count2 += 1
                elif(income[0] < 90000):
                    count3 += 1
                elif(income[0] < 110000):
                    count4 += 1
                elif(income[0] < 130000):
                    count5 += 1
                else:
                    count6 += 1
    x = [count1, count2, count3, count4, count5, count6]
    bars = plt.bar(y,x)
    plt.xlabel('Median Household Income of Birth City in Thousands of Dollars',  fontsize= 13)
    plt.ylabel('Number of Players', fontsize= 13)
    plt.title("Number of NBA Players per Median Household Income Range of Birth City",  fontsize= 18)
    bars[0].set_color('red')
    bars[1].set_color('blue')
    bars[2].set_color('red')
    bars[3].set_color('blue')
    bars[4].set_color('red')
    bars[5].set_color('blue')
    # for i, v in enumerate(y):
    #     plt.text(v + 3, i, str(v), fontweight='bold', verticalalignment='center')
    plt.show()
    
def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'players.db')
    cur = conn.cursor()
    plot_salaries(cur)
    plot_median_incomes(cur)
    cur.close()

main()
