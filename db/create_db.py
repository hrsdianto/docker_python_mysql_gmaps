from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'db_traffic'

TABLES = {}
TABLES['routes'] = (
    "CREATE TABLE `routes` ("
    "  `id_route` int(11) NOT NULL AUTO_INCREMENT,"
    "  `route` varchar(100) NOT NULL,"
    "  `origin` varchar(500) NOT NULL,"
    "  `destination` varchar(500) NOT NULL,"
    "  PRIMARY KEY (`id_route`)"
    ") ENGINE=InnoDB")

TABLES['traffic'] = (
    "CREATE TABLE `traffic` ("
    "  `id_traffic` int(11) NOT NULL AUTO_INCREMENT,"
    "  `id_route` int(11) NOT NULL,"
    "  `distance` varchar(100) NOT NULL,"
    "  `duration` varchar(100) NOT NULL,"
    "  `duration_in_traffic` varchar(100) NOT NULL,"
    "  `status` varchar(100) NOT NULL,"
    "  `date_created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
    "  PRIMARY KEY (`id_traffic`,`id_route`), KEY `id_route` (`id_route`),"
    "  CONSTRAINT `traffic_ibfk_1` FOREIGN KEY (`id_route`) "
    "     REFERENCES `routes` (`id_route`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="321",
)
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()