class SQLGenerator:
    def __init__(self) -> None:
        self.sqls={"select": ['"PLR_ID"','"PLR_NAME"','"Gemeinde_name"'],
                "from": ['"lor_pl"', '"fahrraddiebstahl"', '"bezirksgrenzen"'],
                "joins":['"LOR" = "PLR_ID"', '"Gemeinde_schluessel" = "BEZ"'],
                "cond": {"bezirke":set(), "types":set(), "showVersuch":True, "ShowSuccess":True, "starttime":None, "endtime": None}}
        

    def update_handler(self, Bezirk,ArtdesFahrrads, Tageszeit, Versuch):
        self.sqls["cond"]["bezirke"]=set(Bezirk)

        self.sqls["cond"]["types"]=set(ArtdesFahrrads)

        self.versuch("Versuchter Diebstahl"in Versuch, "Erfolgreicher Diebstahl" in Versuch)        
        
        self.tageszeit("Tag"in Tageszeit, "Nacht"in Tageszeit)

        return self.construct_sql()
     



    def construct_sql(self):
        strq=""
        strq+=("SELECT ")
        strq+=' , '.join(self.sqls["select"])
        strq+=("\nFROM ")
        strq+=' , '.join(self.sqls["from"])
        strq+=("\nWHERE ")
        strq+='\n AND '.join(self.sqls["joins"])
        if self.sqls["cond"]["bezirke"]!=set():
            strq+="\n AND "
            for i in self.sqls["cond"]["bezirke"]:
                strq+=f'"Gemeinde_name"= \'{i}\' OR'
            strq+=f'"Gemeinde_name"= \'DUMMY VALUE\''
        if self.sqls["cond"]["types"]!=set():
            strq+="\n AND "
            for i in self.sqls["cond"]["types"]:
                strq+=f'"ART_DES_FAHRRADS"= \'{i}\' OR'
            strq+=f'"ART_DES_FAHRRADS"= \'DUMMY VALUE\''

        print(strq)
        return strq


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