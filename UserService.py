import re
import bcrypt
import mysql.connector

class UserService:
    """
    A class to handle user authentication and password validation.
    """

    def __init__(self):
        """
        Initializes the UserService object with connection to MySQL database.
        """
        # MySQL database connection details
        database = 'VenueScope'
        self.db_config = {
            'user': 'root',
            'password': 'Karaikudi-630002',
            'host': 'localhost',
            'database': database,
        }

    def authenticate(self, email, password):
        """
        Authenticates a user by checking if the provided email and password match the stored credentials
        and if the password meets the strong password criteria.

        Args:
            email (str): The email to authenticate.
            password (str): The password to validate and match with the stored credentials.

        Returns:
            bool: True if the email exists and the password matches the stored credentials, False otherwise.
        """
        # First, check if the password meets the validation policy
        if not self.validatePassword(password):
            print("Password does not meet the strong password policy.")
            return False

        # Retrieve the stored hashed password from the database
        stored_password = self.getPasswordFromDB(email)

        # If no stored password is found, return False (authentication fails)
        if stored_password is None:
            print("User not found.")
            return False

        # Compare the user-entered password with the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            print("Authentication successful.")
            return True
        else:
            print("Authentication failed. Incorrect password.")
            return False

    def validatePassword(self, password):
        """
        Validates a password against a strong password policy.
        The policy ensures:
        - At least one digit
        - At least one lowercase letter
        - At least one uppercase letter
        - At least one special character from @$!%*?&-
        - Minimum length of 8 characters
        """
        print("Validating password...")

        # Corrected regex to enforce the password policy
        pattern = re.compile(r'^(?=.*\d)'          # At least one digit
                            r'(?=.*[a-z])'        # At least one lowercase letter
                            r'(?=.*[A-Z])'        # At least one uppercase letter
                            r'(?=.*[@$!%*?&\-\_])'  # At least one special character (escaped hyphen)
                            r'[A-Za-z\d@$!%*?&\-\_]{8,}$')  # Minimum 8 characters, escape hyphen
        
        # Final check using the full pattern
        if pattern.match(password):
            print("Password meets the policy.")
            return True
        else:
            print("Password does not meet the policy.")
            return False

    def getPasswordFromDB(self, email):
        """
        Retrieves the stored hashed password for the given email from the MySQL database.

        Args:
            email (str): The email whose password needs to be retrieved.

        Returns:
            str: The stored hashed password if the user exists, None otherwise.
        """
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Query to fetch the hashed password for the given email
            email = email.lower()
            query = "SELECT password FROM club_head_details WHERE email = %s"
            cursor.execute(query, (email,))

            # Fetch the result
            result = cursor.fetchone()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Return the hashed password if the user exists, otherwise return None
            if result:
                return result[0]  # The hashed password is in the first column
            else:
                return None

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None