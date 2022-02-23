import requests
import mysql.connector
from apiKey import *
import time
import schedule
import datetime

HOST_DB = "localhost"
DATABASE_DB = "db_traffic"
USER_DB = "root"
PASSWORD_DB = "321"
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/directions/json?"

def get_route():
    try:
        conn = mysql.connector.connect(
            host=HOST_DB,
            database=DATABASE_DB,
            user=USER_DB,
            password=PASSWORD_DB
            )
        cur = conn.cursor()
        
        print("db_connected!!")
        query = f"SELECT id_route, route, origin, destination FROM routes"

        cur.execute(query)
        rows = cur.fetchall()

        data=[]
        for row in rows:
            data.append({
                "id":row[0],
                "route":row[1],
                "origin":row[2],
                "destination":row[3],
            })
        return data

        cur.close()
        conn.close()
    except Exception as err:
        print("Erro {}".format(err))

def get_traffic_data_from_gmaps(data_destinasi):
    try:
        data =[]
        API_KEY = gmaps_key()
        for des in data_destinasi:
            print("connecting to gmaps api...")
            response = requests.get(f"{GMAPS_BASE_URL}origin={des['origin']}&destination={des['destination']}&departure_time=now&key={API_KEY}")
            response_json = response.json()
            #print(response_json)

            distance = response_json["routes"][0]["legs"][0]["distance"]["text"] # in metres
            duration = response_json["routes"][0]["legs"][0]["duration"]["value"] # in seconds normal
            duration_in_traffic = response_json["routes"][0]["legs"][0]["duration_in_traffic"]["value"] # in seconds current traffic
            duration_in_traffic_text = response_json["routes"][0]["legs"][0]["duration_in_traffic"]["text"] # in seconds current traffic
            duration_text = response_json["routes"][0]["legs"][0]["duration"]["text"]

            
            #cek status traffic
            status = "NORMAL"
            if (duration_in_traffic / duration) > 1.5:
                status = "TRAFFICJAM"

            print(f"{des['route']} {status} {duration_in_traffic_text}..")

            data.append({
                "id": des['id'],
                "screen_name": des['route'],
                "origin": des['origin'],
                "destination": des['destination'],
                "distance": distance,
                "duration": duration,
                "duration_text": duration_text,
                "duration_in_traffic": duration_in_traffic,
                "duration_in_traffic_text": duration_in_traffic_text,
                "status": status
            })
        return data
    except Exception as err:
        print("Erro {}".format(err))

def insert_data(traffic_data):
    try:
        connection = mysql.connector.connect(host=HOST_DB,database=DATABASE_DB,user=USER_DB,password=PASSWORD_DB)
        cursor = connection.cursor()

        distance = traffic_data["distance"]
        duration_text = traffic_data["duration_text"]
        duration_in_traffic_text = traffic_data["duration_in_traffic_text"]
        status = traffic_data["status"]
        id = traffic_data["id"]

        print(f"updating {id} status: {status}..")

        #query = f"UPDATE users SET distance='{distance}', duration='{duration}', duration_in_traffic='{duration_in_traffic}', status='{status}' WHERE id='{id}'"
        query = f"INSERT INTO traffic(id_route, distance, duration, duration_in_traffic, status) VALUES('{id}', '{distance}', '{duration_text}', '{duration_in_traffic_text}', '{status}')"
        cursor.execute(query)
        connection.commit()

        cursor.close()
        connection.close()
    except Exception as err:
        print(f"ERROR {err}")

def job():
    start = datetime.datetime.now()
    print(f"started at: {start}")
    # getting list from database
    data_destinasi = get_route()
    # getting data from gmaps
    traffic_data_list = get_traffic_data_from_gmaps(data_destinasi)
    # checking
        # if not normal then post tweet and mention
    for traffic_data in traffic_data_list:
        # update status in db
        insert_data(traffic_data)

    end =  datetime.datetime.now()
    print(f"finished in: {end - start}")

job()

schedule.every(2).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
