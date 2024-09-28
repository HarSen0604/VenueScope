import mysql.connector
from mysql.connector import Error

class VenueManagement:
    """
    A class to handle venue management operations, such as retrieving booked venues from the database.
    """

    def __init__(self):
        """
        Initializes the VenueManagement object with a connection to the MySQL database.
        """
        database = 'VenueScope'
        self.db_config = {
            'user': 'root',
            'password': 'Karaikudi-630002',
            'host': 'localhost',
            'database': database,
        }

    def getDBConnection(self):
        """
        Establishes a connection to the MySQL database using the provided configuration.

        Returns:
            mysql.connector.connection_cext.CMySQLConnection or None: 
            The MySQL database connection object if the connection is successful, None otherwise.
        """
        try:
            connection = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database']
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    def fetchBookedVenues(self):
        """
        Retrieves booking details from the `booked_venue` table, including venue name and club name by joining relevant tables.

        Returns:
            list[dict]: A list of dictionaries where each dictionary contains details about a booked venue,
                        such as date, time, venue link, venue name, and club name.
        """
        connection = self.getDBConnection()
        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for dict output
        query = """
            SELECT bv.date, bv.from_time, bv.end_time, bv.venue_link, vl.venue_name, cl.club_name
            FROM booked_venue bv
            JOIN venue_list vl ON bv.venue_id = vl.venue_id
            JOIN club_list cl ON bv.club_id = cl.club_id
        """

        cursor.execute(query)
        bookings = cursor.fetchall()

        cursor.close()
        connection.close()

        return bookings