import mysql.connector


try:
    connection = mysql.connector.connect(host='localhost',
                                         database='db_traffic',
                                         user='root',
                                         password='321')
    cursor = connection.cursor()
    #delete_table_query = """DROP TABLE routes"""
    #cursor.execute(delete_table_query)
    #print("Table Deleted successfully ")

    delete_database_query = """DROP DATABASE db_traffic"""
    cursor.execute(delete_database_query)
    connection.commit()
    print("Database Deleted successfully ")

except mysql.connector.Error as error:
    print("Failed to Delete table and database: {}".format(error))
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")