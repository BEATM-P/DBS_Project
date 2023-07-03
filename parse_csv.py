# Import libraries
import pandas as pd
import psycopg2
from config import config
import os
# Connect to PostgreSQL
params = config(config_db = 'database.ini')
print(params)
engine = psycopg2.connect(**params)
print('Python connected to PostgreSQL!')
cur=engine.cursor()

#read csv into pandas


with open(("src/Fahrraddiebstahl.csv"), encoding="latin-1") as test:
    
    fahrraddiebstahl=pd.read_csv(test)

    fahrraddiebstahl.mask(inplac)


    schema=str(test.readline())
    sql = '''CREATE TABLE Fahrraddiebstahl
    (ANGELEGT_AM date,\
    TATZEIT_ANFANG_DATUM date,\
    TATZEIT_ANFANG_STUNDE int check (TATZEIT_ANFANG_STUNDE between 0 and 23), 
    TATZEIT_ENDE_DATUM date,
    TATZEIT_ENDE_STUNDE int check (TATZEIT_ENDE_STUNDE between 0 and 23), 
    LOR int,
    SCHADENSHOEHE int,
    VERSUCH char(5),
    ART_DES_FAHRRADS char(32),
    DELIKT char(32),
    ERFASSUNGSGRUND char(32)
);'''



    cur.execute(sql)   # 
    # print(fahrraddiebstahl)



#print(fahrraddiebstahl)

# Close the connection
engine.commit()
engine.close()