import socket
#import struct
import time
import json
from datetime import datetime, timedelta

from pymongo import MongoClient


today = datetime.now()
day_1 = timedelta(days=1)
yesterday_date = today - day_1
yesterday_date=yesterday_date.strftime("%Y_%m_%d")
date_create=datetime.now()


table_archive = f"sensor_not_{yesterday_date}"


# Adresse IP et port du Raspberry Pi récepteur
receiver_ip = '0.0.0.0'  # Laissez '0.0.0.0' pour écouter sur toutes les interfaces
receiver_port = 8091 # Le même numéro de port que celui utilisé sur le Raspberry Pi émetteur
# Création d'une socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Liaison de la socket à l'adresse et au port
receiver_socket.bind((receiver_ip, receiver_port))
timer= 1440


try:
    while True:
        # Recevoir la chaîne JSON du client
        donnees_recues,adresse_expediteur = receiver_socket.recvfrom(256)
        # donnees_recues= donnees_recues.received_data.decode('utf-8')
        # Si les données reçues sont vides, la connexion a été fermée
        if not donnees_recues:
            print("Connexion fermée par le client.")
            break
        # Convertir la chaîne JSON en liste
        liste_recue = json.loads(donnees_recues)
        print("Liste reçue :", liste_recue)
        uri = 'mongodb+'
        # Create a new client and connect to the server
        client = MongoClient(uri)
        # Send a ping to confirm a successful connection
        try:
            date_create=datetime.now()
            db = client['db_sensor']  # Replace 'your_database_name' with your actual database name
            collection = db['db_sensor_final']
            collection.insert_one({
            "time": liste_recue[0],
            "distance": liste_recue[1],
            "notification": liste_recue[2],
            "date_create":date_create
        })
        except Exception as e:
            print(e)

        # Afficher la liste reçue
        
                
        # CONNECTION = "postgres://tsdbadmin:m01w7odv95pecxxs@ghg7xh4dph.gekjrogvk3.tsdb.cloud.timescale.com:34785/tsdb?sslmode=require"
        # with psycopg2.connect(CONNECTION) as conn:
        #     c = conn.cursor()

          
                                        
        #     c.execute("""
        # CREATE TABLE IF NOT EXISTS sensor_not (
        #     id SERIAL PRIMARY KEY,
        #     time FLOAT,
        #     distance FLOAT,
        #     notification FLOAT,
        #     date_create TIMESTAMPTZ ,
        #     FOREIGN KEY (id) REFERENCES sensors (id)
            
        # );
        # """)
        #     conn.commit()
        #     d= {"time":liste_recue[0],"distance":liste_recue[1],"notification":liste_recue[2]}
        #     c.execute("""
        #     INSERT INTO sensor_not(time,distance,notification) VALUES (%(time)s,%(distance)s,%(notification)s)""",d)
        #     conn.commit()
        #     # conn.close()
        # print("11111111111111111")

       
except KeyboardInterrupt:
    print("Interruption manuelle")

finally:
    # Fermeture de la connexion
    receiver_socket.close()
