import mysql.connector

def create_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="321",
            database="db_traffic"
        )
        cursor = conn.cursor()
        print("db connected..")

        #cursor.execute("CREATE DATABASE IF NOT EXISTS db_traffic")
        cursor.execute("SHOW TABLES")
        for x in cursor:
            print(x[0])
        #_route="polyline_1"
        #_origin="Jambi"
        #_destination="Palembang"
        cursor.execute("INSERT INTO routes(route, origin, destination) VALUES('polyline_1', 'Jambi', 'Palembang')")
        conn.commit()

        cursor.close()
        conn.close()
    except Exception as err:
        print("Erro {}".format(err))


mydb=create_db()
print(mydb) 