import pandas as pd
import psycopg2
import io
from config import config
from sqlalchemy import create_engine

with open(("src/Fahrraddiebstahl.csv"), encoding="latin-1") as test:
    fahrraddiebstahl=pd.read_csv(test)
with open(("src/lor_planungsraeume_2021.csv"), encoding="UTF-8") as test2:
    lor_planungsraeume=pd.read_csv(test2)
with open(("src/bezirksgrenzen.csv"), encoding="UTF-8") as test3:
    bezirksgrenzen=pd.read_csv(test3)

#delete unnecessary/ empty attributes
lor_planungsraeume  = lor_planungsraeume.drop(["Name","description","timestamp","begin","end","altitudeMode","tessellate","extrude","visibility","drawOrder","icon","STAND"], axis = 1)
bezirksgrenzen      = bezirksgrenzen.drop(["gml_id", "Land_name", "Land_schluessel", "Schluessel_gesamt"], axis = 1)

# Merge TATZEIT_ANFANG_DATUM + TATZEIT_ANFANG_STUNDE and TATZEIT_ENDE_DATUM + TATZEIT_ENDE_STUNDE 
# Change datatype to timestamp
# Delete column TATZEIT_ANFANG_STUNDE and TATZEIT_ENDE_STUNDE 
def StringtoDate(df, column1, column2):
    for i in range(len(df[column1])):
        df[column1][i] = pd.to_datetime((df[column1][i] + " " + str(df[column2][i]) + ":00"), format= '%d.%m.%Y %H:%M')
    del df[column2]

#Take int and return it as string with 8 digits
def PLRID_adjustDigits(num):
    return f'{num:08d}'


# Change VERSUCH column to booleans 
def VersuchToBool(df):
    map= {"Ja":True, "Nein": False}
    return df.replace({"VERSUCH":map})

StringtoDate(fahrraddiebstahl, "TATZEIT_ANFANG_DATUM", "TATZEIT_ANFANG_STUNDE")
StringtoDate(fahrraddiebstahl, "TATZEIT_ENDE_DATUM", "TATZEIT_ENDE_STUNDE")
fahrraddiebstahl=VersuchToBool(fahrraddiebstahl)


#adjust PLR_ID so all of them have 8 digits
#lor_planungsraeume["PLR_ID"]=lor_planungsraeume["PLR_ID"].map(PLRID_adjustDigits)
# Create table in postgres with dataframe 
engine = create_engine(
    'postgresql+psycopg2://pm:admindb@localhost:5432/bikes')

# We dont need to put the dataframes into the database manually lol
#df.to_sql does everything
fahrraddiebstahl.to_sql('fahrraddiebstahl', engine, if_exists='replace',index=False)    
lor_planungsraeume.to_sql('lor_pl', engine, if_exists='replace',index=False)
bezirksgrenzen.to_sql('bezirksgrenzen', engine, if_exists='replace',index=False)


#DEPRECIATED
# params = config('database.ini')
# conn = engine.raw_connection()
# cur = conn.cursor()
# output = io.StringIO()
# fahrraddiebstahl.to_csv(output, sep='\t', header=False, index=False)
# output.seek(0)
# contents = output.getvalue()
# cur.copy_from(output, 'Fahrraddiebstahl', null="") # null values become ''

# output = io.StringIO()
# lor_planungsraeume.to_csv(output, sep='\t', header=False, index=False)
# output.seek(0)
# cur.copy_from(output, 'lor_pl', null="") # null values become ''

# conn.commit()
# cur.close()
# conn.close()
