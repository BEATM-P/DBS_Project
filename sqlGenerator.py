from datetime import datetime, date, time
class SQLGenerator:
    def __init__(self) -> None:
        self.sqls={"select": ['count("LOR")','"PLR_ID"','"PLR_NAME"','"Gemeinde_name"'],
                "from": ['"lor_pl"', '"fahrraddiebstahl"', '"bezirksgrenzen"'],
                "joins":['"LOR" = "PLR_ID"', '"Gemeinde_schluessel" = "BEZ"'],
                "cond": {"bezirke":set(), "types":set(), "showVersuch":True, "showSuccess":True, "starttime":None, "endtime": None}}


    def update_handler(self, Bezirk,ArtdesFahrrads, Tageszeit, Versuch, startDatum, endDatum):
        
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
        
        #VERSUCH?
        if self.sqls["cond"]["showVersuch"]==False:
            strq+=f'\n AND \"VERSUCH\"=\'TRUE\''
        if self.sqls["cond"]["showSuccess"]==False:
            strq+=f'\n AND \"VERSUCH\"=\'FALSE\''
        
        strq+="\n GROUP BY"
        strq+=" , ".join(self.sqls["select"][1:])

        print(strq)
        return strq+";"


    def tageszeit(self, tag=None, nacht=None):
        pass

    def add_time(self, starttime=None, endtime=None):
        if starttime==None and endtime==None:
            print("Who called this function without input?")
            return
        elif endtime!=None:
            self.sqls["cond"]["endtime"]=f'"TATZEIT_ENDE_STUNDE" < {endtime}'
        elif starttime!=None:
            self.sqls["cond"]["starttime"]=f'"TATZEIT_ANFANG_STUNDE" > {starttime}'

    def remove_time(self,time):
        self.sqls["cond"].remove(time)

    def show_bezirk(self, bezirk):
        if bezirk in self.sqls.cond["bezirke"]:
            self.sqls.cond["bezirke"].remove(bezirk)

    def hide_bezirk(self, bezirk):
        if not bezirk in self.sqls.cond["bezirke"]:
            self.sqls.cond["bezirke"].append(bezirk)

    def show_type(self, type):
        if type in self.sqls.cond["types"]:
            self.sqls.cond["types"].remove(type)

    def hide_type(self, type):
        if not type in self.sqls.cond["types"]:
            self.sqls.cond["types"].append(type)

    def versuch(self, showVersuch=None, showSuccess=None):
        print(showSuccess,showVersuch)
        if showVersuch==None and showSuccess==None:
            print("Who called this function without input?")
            return
        elif showVersuch!=None:
            self.sqls["cond"]["showVersuch"]=showVersuch
        elif showSuccess!=None:
            self.sqls["cond"]["showSuccess"]=showSuccess


if __name__=="__main__":
    print("UNIT TESTING SQL GENERATION OR SMTH")
    G=SQLGenerator()
    G.update_handler(['Mitte'],['Fahrrad'], ['Tag', 'Nacht'],['Versuchter Diebstahl'])