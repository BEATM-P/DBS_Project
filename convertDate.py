import pandas as pd

with open(("src/Fahrraddiebstahl.csv"), encoding="latin-1") as test:
    fahrraddiebstahl=pd.read_csv(test)

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


print(fahrraddiebstahl["TATZEIT_ANFANG_DATUM"])
print(fahrraddiebstahl["TATZEIT_ENDE_DATUM"])
print(fahrraddiebstahl["VERSUCH"])