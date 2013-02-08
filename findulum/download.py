#To download Bhavcopy files from NSE website and populate the data into DB

import requests
import zipfile
#import StringIO
import os
import csv
import MySQLdb as mdb
from datetime import datetime
import sys

datestring = "03-01-2013"
date = datetime.strptime(datestring, "%d-%m-%Y")

#1. Download zip file and extract the csv file - Can be enhanced to read zip file into memory
filename = "cm" +date.strftime('%d%b%Y').upper()+ "bhav.csv"
url = "http://www.nseindia.com/content/historical/EQUITIES/" +date.strftime('%Y')+ "/" +date.strftime('%b').upper()+ "/" + filename + ".zip"

response = requests.get(url)
with open(filename+".zip", "wb") as code:
    code.write(response.content)

zfile = zipfile.ZipFile(filename+".zip")
for name in zfile.namelist():
	fd = open(name,"w")
	fd.write(zfile.read(name))
	fd.close()

print "Finished downloading and unzipping file."

os.remove(filename+".zip")

#2. Open file, read contents and insert into DB
csvfile = open(filename, "r")
reader = csv.DictReader(csvfile)

try:
    con = mdb.connect('54.235.116.128', 'kalyan', 'kalyan1234', 'findulum')
    counter = 0

    for row in reader:
        symbol = row['SYMBOL']
        series = row['SERIES']
        openprice = float(row['OPEN'])*100
        closeprice = float(row['CLOSE'])*100
        highprice = float(row['HIGH'])*100
        lowprice = float(row['LOW'])*100
        lastprice = float(row['LAST'])*100
        prevclose = float(row['PREVCLOSE'])*100
        tottrdqty = float(row['TOTTRDQTY'])
        tottrdval = float(row['TOTTRDVAL'])*100
        date = row['TIMESTAMP']
        tottrades = float(row['TOTALTRADES'])
        isin = row['ISIN']
        counter = counter+1

        with con:
            cur = con.cursor()
            query = "INSERT INTO PricePoints VALUES(" +str(counter)+ ",STR_TO_DATE('" +date+ "', '%d-%M-%Y'),'" +symbol+ "','" +series+ "'," +str(openprice)+ "," +str(closeprice)+ "," +str(highprice)+ "," +str(lowprice)+ "," +str(lastprice)+ "," +str(prevclose)+ "," +str(tottrdqty)+ "," +str(tottrdval)+ "," +str(tottrades)+ ",'" +isin+ "')"
            print query
            cur.execute(query)
        cur.close()

#3. Close DB connection and file
    csvfile.close()
    con.close()

except mdb.Error, e:
    print "Database exception occured. Details: [" +str(e)+ "]"

print "Done"
