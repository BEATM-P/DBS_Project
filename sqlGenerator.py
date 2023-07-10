class SQLGenerator:
    def __init__(self) -> None:
        self.sqls={"select": ['"PLR_ID"','"PLR_NAME"','"Gemeinde_name"'],
                "from": ['"lor_pl"', '"fahrraddiebstahl"', '"bezirksgrenzen"'],
                "joins":['"LOR" = "PLR_ID"', '"Gemeinde_schluessel" = "BEZ"'],
                "cond": {"bezirke":[], "types":[], "showVersuch":True, "showVersuch":None, "starttime":None, "endtime": None}}
        
    def construct_sql(self):
        strq=""
        strq+=("SELECT ")
        strq+=' , '.join(self.sqls["select"])
        strq+=("\nFROM ")
        strq+=' , '.join(self.sqls["from"])
        strq+=("\nWHERE ")
        strq+='\n AND '.join(self.sqls["joins"])
        for i in self.sqls["cond"]["bezirke"]:
           strq+=f'\n AND "Gemeinde_name"= {i}'
        for i in self.sqls["cond"]["types"]:
           strq+=f'\n AND "ART_DES_FAHRRADS"= {i}'
        print(strq)

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
    G.construct_sql()