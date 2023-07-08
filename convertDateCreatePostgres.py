import pandas as pd
import psycopg2
import io
from config import config
from sqlalchemy import create_engine

with open(("src/Fahrraddiebstahl.csv"), encoding="latin-1") as test:
    fahrraddiebstahl=pd.read_csv(test)
with open(("src/lor_planungsraeume_2021.csv"), encoding="UTF-8") as testi:
    lor_planungsraeume=pd.read_csv(testi)

# Merge TATZEIT_ANFANG_DATUM + TATZEIT_ANFANG_STUNDE and TATZEIT_ENDE_DATUM + TATZEIT_ENDE_STUNDE 
# Change datatype to timestamp
# Delete column TATZEIT_ANFANG_STUNDE and TATZEIT_ENDE_STUNDE 
def StringtoDate(df, column1, column2):
    for i in range(len(df[column1])):
        df[column1][i] = pd.to_datetime((df[column1][i] + " " + str(df[column2][i]) + ":00"), format= '%d.%m.%Y %H:%M')
    del df[column2]

# Change VERSUCH column to booleans 
def VersuchToBool(df):
    map= {"Ja":True, "Nein": False}
    return df.replace({"VERSUCH":map})

StringtoDate(fahrraddiebstahl, "TATZEIT_ANFANG_DATUM", "TATZEIT_ANFANG_STUNDE")
StringtoDate(fahrraddiebstahl, "TATZEIT_ENDE_DATUM", "TATZEIT_ENDE_STUNDE")
fahrraddiebstahl=VersuchToBool(fahrraddiebstahl)


# Create table in postgres with dataframe 
engine = create_engine(
    'postgresql+psycopg2://pm:admindb@localhost:5432/bikes')

fahrraddiebstahl.head(0).to_sql('table_name', engine, if_exists='replace',index=False)
lor_planungsraeume.head(0).to_sql('lor_pl', engine, if_exists='replace',index=False)
params = config('database.ini')
conn = engine.raw_connection()
cur = conn.cursor()
output = io.StringIO()
fahrraddiebstahl.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'table_name', null="") # null values become ''

output = io.StringIO()
lor_planungsraeume.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)
cur.copy_from(output, 'lor_pl', null="") # null values become ''

conn.commit()
cur.close()
conn.close()