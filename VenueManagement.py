import mysql.connector
from mysql.connector import Error

class VenueManagement:
    def __init__(self):
        """
        Initializes the VenueManagement object with a connection to the MySQL database.
        """
        # MySQL database connection details
        database = 'VenueScope'
        self.db_config = {
            'user': 'root',
            'password': 'Karaikudi-630002',
            'host': 'localhost',
            'database': database,
        }

    def getDBConnection(self):
        """Establishes and returns a MySQL database connection using the db_config."""
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
        Retrieves booking details from the booked_venue table, including venue_name and club_name.

        Returns:
            list[dict]: A list of dictionaries containing booking details.
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