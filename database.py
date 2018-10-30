import csv
import sys
import MySQLdb

orig = sys.stdout
with open("outp.txt", "wb") as f:
   sys.stdout = f
   try:
       execfile("ping.py", {})
   finally:
       sys.stdout = orig
new_rows = [] # a holder for our modified rows when we make them
changes = {   # a dictionary of changes to make, find 'key' substitute with 'value'
   '     ' : ',' # I assume both 'key' and 'value' are strings
   }

with open('outp.txt', 'rb') as f:
   reader = csv.reader(f) # pass the file to our csv reader
   for row in reader:     # iterate over the rows in the file
       new_row = row      # at first, just copy the row
       for key, value in changes.items(): 
       # iterate over 'changes' dictionary
           new_row = [ x.replace(key, value) for x in new_row ] 
    # make the substitutions
       new_rows.append(new_row) # add the modified rows
with open('outp.txt', 'wb') as f:
   # Overwrite the old file with the modified rows
   writer = csv.writer(f)
   writer.writerows(new_rows)

connection = MySQLdb.connect(host="x.x.x.x", # The Host 
user="root", # username
passwd="*****", # password 
db=" ") # name of the data base

cursor = connection.cursor()
Query = """ DROP TABLE ipmac """

cursor.execute(Query)
Query = """ DROP TABLE finalmac """

cursor.execute(Query)
Query = """ CREATE TABLE ipmac
(
ipaddress VARCHAR(20),
macaddress VARCHAR(40) PRIMARY KEY,
state VARCHAR(20)
) """

cursor.execute(Query)

Query = """ LOAD DATA LOCAL INFILE 'outp.txt' INTO TABLE ipmac 
FIELDS TERMINATED BY ','
 LINES TERMINATED BY '\n'
 IGNORE 6 LINES """

cursor.execute(Query)

Query = """ CREATE TABLE finalmac as
(
SELECT ipmac.ipaddress as ipaddress,
mac.vendor as vendorname,
ipmac.macaddress as macaddress,
mac.des as description 
from 
ipmac join mac
 on
 rpad(ipmac.macaddress,8,' ')=mac.macaddress
 ) """

cursor.execute(Query)
connection.commit()
cursor.close()
