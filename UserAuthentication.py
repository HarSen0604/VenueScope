import re
import bcrypt
import mysql.connector
import requests
from bs4 import BeautifulSoup

class UserAuthentication:
    """
    A class to handle user authentication and password validation.
    """

    def __init__(self):
        """
        Initializes the UserAuthentication object with connection details to the MySQL database.
        """

        database = 'VenueScope'
        self.db_config = {
            'user': 'root',
            'password': 'root',
            'host': 'localhost',
            'database': database,
        }

    def authenticateMember(self, email, password):
        """
        Authenticates a club member by verifying their email and password.
        
        Checks if the provided password meets strong password criteria and then verifies it
        against the stored hashed password in the database.

        Args:
            email (str): The email of the member attempting to authenticate.
            password (str): The password provided for authentication.

        Returns:
            bool: True if authentication is successful, False otherwise.
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
        Validates a password against the defined strong password policy.
        
        The policy ensures that the password contains:
        - At least one digit
        - At least one lowercase letter
        - At least one uppercase letter
        - At least one special character from @$!%*?&-
        - Minimum length of 8 characters

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password meets the policy, False otherwise.
        """

        # Corrected regex to enforce the password policy
        pattern = re.compile(r'^(?=.*\d)'          # At least one digit
                            r'(?=.*[a-z])'        # At least one lowercase letter
                            r'(?=.*[A-Z])'        # At least one uppercase letter
                            r'(?=.*[@$!%*?&\-\_])'  # At least one special character (escaped hyphen)
                            r'[A-Za-z\d@$!%*?&\-\_]{8,}$')  # Minimum 8 characters, escape hyphen
        
        # Final check using the full pattern
        if pattern.match(password):
            return True
        else:
            return False

    def getPasswordFromDB(self, email):
        """
        Retrieves the stored hashed password for a given member's email from the MySQL database.

        Args:
            email (str): The email of the user whose password needs to be retrieved.

        Returns:
            str: The stored hashed password if the email exists, None otherwise.
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
    
    def authenticateStudent(self, roll_no, password):
        """
        Authenticates a student by logging into the PSG Tech eCampus platform using the provided roll number and password.

        The method attempts to log in using the provided credentials by submitting them to the eCampus login form.
        
        Args:
            roll_no (str): The student's roll number.
            password (str): The student's password.

        Returns:
            bool: True if login is successful, False otherwise.
        """

        # URL of the login page
        url = 'https://ecampus.psgtech.ac.in/studzone2/'

        # Create a session to manage cookies
        session = requests.Session()

        # Get the login page to retrieve necessary hidden fields
        response = session.get(url)
        
        # Check if the page was retrieved successfully
        if response.status_code != 200:
            print("Failed to load the login page.")
            return False

        # Parse the required hidden fields (__VIEWSTATE, __VIEWSTATEGENERATOR, __EVENTVALIDATION)
        soup = BeautifulSoup(response.text, 'html.parser')
        viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
        viewstategen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
        eventval = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

        # Data for login
        login_data = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategen,
            '__EVENTVALIDATION': eventval,
            'txtusercheck': roll_no,
            'txtpwdcheck': password,
            'abcd3': 'Login',
        }

        # Post the login data to the server
        login_response = session.post(url, data=login_data)

        # Check if login was successful by inspecting the response
        if "Student Login" not in login_response.text:
            print("Login successful!")
            return True
        else:
            print("Login failed.")
            return False
    
    def hashPassword(self, password):
        """
        Hashes the provided password using bcrypt.

        Args:
            password (str): The plain-text password to hash.

        Returns:
            str: The hashed password.
        """
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def updatePasswordInDB(self, email, hashed_password):
        """
        Updates the password for the specified email in the database.

        Args:
            email (str): The email of the user whose password should be updated.
            hashed_password (str): The new hashed password to store.
        """
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Update the password for the given email
            query = "UPDATE club_head_details SET password = %s WHERE email = %s"
            cursor.execute(query, (hashed_password, email))
            
            # Commit the changes
            conn.commit()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            print(f"Password updated successfully for {email}.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
