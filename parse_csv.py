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
    
    # fahrraddiebstahl=pd.read_csv(test)

    # print(fahrraddiebstahl.head(7))


    # print(fahrraddiebstahl.columns[7])
    # map= {"Ja":True, "Nein": False}


    # print(fahrraddiebstahl["VERSUCH"][0])
    # print(len(fahrraddiebstahl["VERSUCH"][0]))


    # fahrraddiebstahl=fahrraddiebstahl.replace({"VERSUCH":map})
    #   # fahrraddiebstahl.mask(
    # #)
    # print(type(fahrraddiebstahl["TATZEIT_ENDE_DATUM"][0]))
    # print(fahrraddiebstahl.head(7))

    # # fahrraddiebstahl.mask
    # # )


    schema=str(test.readline())
    sql = '''CREATE TABLE Fahrraddiebstahl
    (ANGELEGT_AM date,\
    TATZEIT_ANFANG_DATUM date,\
    TATZEIT_ANFANG_STUNDE int check (TATZEIT_ANFANG_STUNDE between 0 and 23), 
    TATZEIT_ENDE date, 
    LOR int,
    SCHADENSHOEHE int,
    VERSUCH bool,
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