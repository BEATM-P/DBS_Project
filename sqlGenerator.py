class SQLGenerator:
    def __init__(self) -> None:
        self.sqls={"select": ['count("LOR") as z','"PLR_ID"','"PLR_NAME"','"Gemeinde_name"'],
                "from": ['"lor_pl"', '"fahrraddiebstahl"'],
                "joins":['"LOR" = "PLR_ID"'],
                "cond": {"bezirke":set(), "types":set(), "showVersuch":True, "showSuccess":True, "time":None},
                "order": 'z DESC'}


    def update_handler(self, Bezirk,ArtdesFahrrads, Tageszeit, Versuch, startDatum, endDatum, Schadenshoehe):
        
        if Bezirk!=None:
            self.sqls["cond"]["bezirke"]=set(Bezirk)
        if ArtdesFahrrads!=None:
            self.sqls["cond"]["types"]=set(ArtdesFahrrads)

        if Versuch!=None:
            self.versuch("Versuchter Diebstahl"in Versuch, "Erfolgreicher Diebstahl" in Versuch)        
        if Tageszeit!=None:
            self.tageszeit("Tag"in Tageszeit, "Nacht"in Tageszeit)
        if startDatum!=None:
            self.sqls["cond"]["startDatum"]=startDatum+ " 00:00:00"#datetime.combine(date(startDatum), time(0))
        if endDatum!=None:
            self.sqls["cond"]["endDatum"]=endDatum + " 23:59:59"#datetime.combine(date(endDatum), time(0))       #Maybe make take the next day so specified endDatum is included in results
        if Schadenshoehe=="Schadenshöhe":
            self.sqls["select"][0]='sum("SCHADENSHOEHE") as z'
        elif Schadenshoehe=="Anzahl Diebstähle":
            self.sqls["select"][0]='count("LOR") as z'

        return self.construct_sql()
     



    def construct_sql(self):
        strq=""
        strq+=("SELECT ")
        strq+=' , '.join(self.sqls["select"])
        strq+=("\nFROM ")
        strq+=' , '.join(self.sqls["from"])
        strq+=("\nWHERE ")
        strq+='\n AND '.join(self.sqls["joins"])
        

        #BEZIRKE
        if self.sqls["cond"]["bezirke"]!=set():
            strq+="\n AND ("
            for i in self.sqls["cond"]["bezirke"]:
                strq+=f'"Gemeinde_name"= \'{i}\' OR '
            strq+=f'"Gemeinde_name"= \'DUMMY VALUE\')'

        #ARTDESFAHRRADS
        if self.sqls["cond"]["types"]!=set():
            strq+="\n AND ("
            for i in self.sqls["cond"]["types"]:
                strq+=f'"ART_DES_FAHRRADS"= \'{i}\' OR '
            strq+=f'"ART_DES_FAHRRADS"= \'DUMMY VALUE\')'
        
        #Datum
        if self.sqls["cond"]["startDatum"]!=None:
            strq+= f'\n AND \"TATZEIT_ANFANG_DATUM\" >= \'{self.sqls["cond"]["startDatum"]}\''
        if self.sqls["cond"]["endDatum"]!=None:
            strq+= f'\n AND \"TATZEIT_ENDE_DATUM\" <= \'{self.sqls["cond"]["endDatum"]}\''            
        
        #VERSUCH
        if not self.sqls["cond"]["showVersuch"]==self.sqls["cond"]["showSuccess"]:
            if self.sqls["cond"]["showVersuch"]==False:
                strq+=f'\n AND \"VERSUCH\"=\'false\''
            if self.sqls["cond"]["showSuccess"]==False:
                strq+=f'\n AND \"VERSUCH\"=\'true\''

        #TIME
        if self.sqls["cond"]["time"]=="tag":
            strq+=f'\n AND (\"TATZEIT_ANFANG_STUNDE\" >= \'06:00\' AND \"TATZEIT_ANFANG_STUNDE\" <= \'22:00\')'
        elif self.sqls["cond"]["time"]=="nacht":
            strq+=f'\n AND (\"TATZEIT_ANFANG_STUNDE\" <= \'06:00\' OR \"TATZEIT_ANFANG_STUNDE\" >= \'22:00\')'


        strq+="\n GROUP BY "
        strq+=" , ".join(self.sqls["select"][1:])
        strq+="\n ORDER BY "
        strq+="".join(self.sqls["order"])

        print(strq)
        return strq+";"


    def tageszeit(self, tag=None, nacht=None):
        if tag == nacht:
            self.sqls["cond"]["time"]=None
        if tag==True and nacht==False:
            self.sqls["cond"]["time"]="tag"

        if tag==False and nacht==True:
            self.sqls["cond"]["time"]="nacht"



    
    def versuch(self, showVersuch=None, showSuccess=None):
        print(showSuccess,showVersuch)
        if showVersuch==None and showSuccess==None:
            print("Who called this function without input?")
            return
        if showVersuch!=None:
            self.sqls["cond"]["showVersuch"]=showVersuch
        if showSuccess!=None:
            self.sqls["cond"]["showSuccess"]=showSuccess


if __name__=="__main__":
    print("UNIT TESTING SQL GENERATION OR SMTH")
    G=SQLGenerator()
    G.update_handler(['Mitte'],['Fahrrad'], ['Tag', 'Nacht'],['Versuchter Diebstahl'])