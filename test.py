import django
import psycopg2

print(django.get_version())

def create_database():
  
    conn = psycopg2.connect(database="EMPLOYEE_DATABASE",
                        user='postgres', password='pass', 
                        host='127.0.0.1', port='8080')
  
    conn.autocommit = True
    cursor = conn.cursor()
  
  
    sql = '''CREATE TABLE Fahrraddiebstahl
    (ANGELEGT_AM date,\
    TATZEIT_ANFANG_DATUM date,\
    TATZEIT_ANFANG_STUNDE int check (TATZEIT_ANFANG_STUNDE between 0 and 23), 
    TATZEIT_ENDE_DATUM date,
    TATZEIT_ENDE_STUNDE int check (TATZEIT_ENDE_STUNDE between 0 and 23), 
    LOR int,
    SCHADENSHOEHE int,
    VERSUCH string,
    ART_DES_FAHRRADS string,
    DELIKT string,
    ERFASSUNGSGRUND string
);'''
  
  
    cursor.execute(sql)
  
    sql2 = '''COPY Fahraddiebstahl(ANGELEGT_AM,TATZEIT_ANFANG_DATUM)
    FROM '/home/pm/Uni/DBS/dbs-abgabe/src/Fahrraddiebstahl.csv'
    DELIMITER ','
    CSV HEADER;'''
  
    cursor.execute(sql2)
    
    sql3 = '''select * from details;'''
    cursor.execute(sql3)
    for i in cursor.fetchall():
        print(i)
    
    conn.commit()
    conn.close()





if __name__=="__main__":
    create_database()