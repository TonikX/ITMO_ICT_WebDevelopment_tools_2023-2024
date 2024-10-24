import mysql.connector

def get_engine():
    try:
        # Replace these values with your actual MySQL credentials
        cnx = mysql.connector.connect( user='root', password='12345',
                                 host='127.0.0.1',
                                 database='new_schema',
            port=3306  # Default MySQL port
        )
        return cnx
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None