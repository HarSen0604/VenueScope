import mysql.connector
from mysql.connector import Error
from datetime import datetime

class VenueManagement:
    """
    A class to handle venue management operations, such as retrieving booked venues from the database.
    """

    def __init__(self):
        """
        Initializes the VenueManagement object with the MySQL database configuration.

        Attributes:
            db_config (dict): A dictionary containing database connection parameters (user, password, host, database).
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
        Establishes a connection to the MySQL database using the stored configuration.

        Returns:
            mysql.connector.connection_cext.CMySQLConnection or None: 
            The MySQL connection object if the connection is successful, or None if the connection fails.
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
        Retrieves details of all booked venues from the database, including the venue name and club name.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary contains booking details such as 
                        date, from_time, end_time, venue link, venue name, and club name.
        """

        connection = self.getDBConnection()
        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for dict output
        query = """
            SELECT 
                DATE_FORMAT(bv.date, '%d-%m-%Y') AS date, 
                DATE_FORMAT(bv.from_time, '%r') AS from_time, 
                DATE_FORMAT(bv.end_time, '%r') AS end_time, 
                bv.venue_link, 
                vl.venue_name, 
                cl.club_name
            FROM 
                booked_venue bv 
            JOIN 
                venue_list vl ON bv.venue_id = vl.venue_id 
            JOIN 
                club_list cl ON bv.club_id = cl.club_id;
        """

        cursor.execute(query)
        bookings = cursor.fetchall()

        cursor.close()
        connection.close()

        return bookings
    
    def fetchVenues(self):
        """
        Fetches the list of all available venues from the venue_list table.

        Returns:
            list[dict]: A list of dictionaries where each dictionary contains 'venue_name'.
        """

        connection = self.getDBConnection()
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT venue_name FROM venue_list"
        cursor.execute(query)
        
        venues = cursor.fetchall()
        
        cursor.close()
        connection.close()

        return venues

    def fetchClubs(self):
        """
        Fetches the list of all clubs from the club_list table.

        Returns:
            list[dict]: A list of dictionaries where each dictionary contains 'club_name'.
        """

        connection = self.getDBConnection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT club_name FROM club_list"
        cursor.execute(query)

        clubs = cursor.fetchall()

        cursor.close()
        connection.close()

        return clubs

    
    def isVenueBooked(self, date, from_time, end_time, venue_name):
        """
        Checks if a venue is already booked for the given date and time range.

        Args:
            date (str): The date of the booking (in 'YYYY-MM-DD' format).
            from_time (str): The start time of the booking (in 'HH:MM:SS' format).
            end_time (str): The end time of the booking (in 'HH:MM:SS' format).
            venue_name (str): The name of the venue being checked.

        Returns:
            bool: True if the venue is already booked for the specified time range, False otherwise.
        """

        connection = self.getDBConnection()
        cursor = connection.cursor()

        query = """
        SELECT 1
        FROM booked_venue bv
        JOIN venue_list vl ON bv.venue_id = vl.venue_id
        WHERE bv.date = %s AND vl.venue_name = %s
        AND ((bv.from_time <= %s AND bv.end_time > %s) 
            OR (bv.from_time < %s AND bv.end_time >= %s));
        """

        cursor.execute(query, (date, venue_name, from_time, from_time, end_time, end_time))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result is not None

    def bookVenue(self, date, from_time, end_time, venue_name, club_name, venue_link):
        """
        Inserts a new venue booking into the database if no time conflicts exist.

        Args:
            date (str): The booking date (in 'YYYY-MM-DD' format).
            from_time (str): The start time of the booking (in 'HH:MM:SS' format).
            end_time (str): The end time of the booking (in 'HH:MM:SS' format).
            venue_name (str): The name of the venue being booked.
            club_name (str): The name of the club making the booking.
            venue_link (str): A link related to the booking (e.g., for event registration).
        """

        connection = self.getDBConnection()
        cursor = connection.cursor()

        # Insert the new booking into the database
        query = """
        INSERT INTO booked_venue (venue_id, club_id, date, from_time, end_time, venue_link)
        VALUES ((SELECT venue_id FROM venue_list WHERE venue_name = %s), 
                (SELECT club_id FROM club_list WHERE club_name = %s), %s, %s, %s, %s);
        """

        cursor.execute(query, (venue_name, club_name, date, from_time, end_time, venue_link))
        connection.commit()

        cursor.close()
        connection.close()

    def getClubNameByEmail(self, email):
        """
        Retrieves the club name associated with a logged-in user based on their email address.

        Args:
            email (str): The email address of the logged-in member.

        Returns:
            str or None: The club name if found, or None if no club is associated with the given email.
        """

        connection = self.getDBConnection()
        if connection is None:
            return None

        cursor = connection.cursor()
        query = """
            SELECT cl.club_name 
            FROM club_head_details chd
            JOIN club_head ch ON chd.head_id = ch.head_id
            JOIN club_list cl ON ch.club_id = cl.club_id
            WHERE chd.email = %s
        """
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            return result[0]
        return None
    
    def deleteBooking(self, date, from_time, end_time, venue_name, club_name):
        """
        Deletes a booking for the given date, time, and venue.

        Args:
            date (str): The date of the booking.
            from_time (str): The starting time of the booking.
            venue_name (str): The name of the venue.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """

        connection = self.getDBConnection()
        if connection is None:
            return False

        cursor = connection.cursor()

        query = """
        DELETE FROM booked_venue 
        WHERE date = %s AND from_time = %s AND end_time = %s AND venue_id = (
            SELECT venue_id FROM venue_list WHERE venue_name = %s
        ) AND club_id = (SELECT club_id FROM club_list WHERE club_name = %s);
        """
        try:
            from_time = datetime.strptime(from_time, '%I:%M:%S %p').time() 
            end_time = datetime.strptime(end_time, '%I:%M:%S %p').time()
            print(date, from_time, end_time, venue_name, club_name)
            cursor.execute(query, (date, from_time, end_time, venue_name, club_name))
            connection.commit()
            result = cursor.rowcount > 0  # Check if rows were affected
        except Error as e:
            print(f"Error deleting booking: {e}")
            result = False
        finally:
            cursor.close()
            connection.close()

        return result

    def fetchClubNameForBooking(self, date, from_time, venue_name):
        """
        Retrieves the club name associated with a specific booking.

        Args:
            date (str): The date of the booking.
            from_time (str): The start time of the booking.
            venue_name (str): The name of the venue.

        Returns:
            str or None: The club name if found, otherwise None.
        """

        connection = self.getDBConnection()
        if connection is None:
            return None
        
        cursor = connection.cursor()

        query = """
        SELECT cl.club_name
        FROM booked_venue bv
        JOIN venue_list vl ON bv.venue_id = vl.venue_id
        JOIN club_list cl ON bv.club_id = cl.club_id
        WHERE bv.date = %s AND bv.from_time = %s AND vl.venue_name = %s;
        """
        
        from_time = from_time.split(' ')[0]
        cursor.execute(query, (date, from_time, venue_name))
        result = cursor.fetchone()
        # print(date, from_time, venue_name)
        cursor.close()
        connection.close()

        if result:
            return result[0]
        return None