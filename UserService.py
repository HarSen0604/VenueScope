import re

class UserService:
    """
    A class to handle user authentication and password validation.
    """

    def __init__(self):
        """
        Initializes the UserService object with predefined user credentials.
        """
        self.userCredentials = {
            'student': 'Root@630002',
            'member': 'Root@630002'
        }

    def authenticate(self, username, password):
        """
        Authenticates a user by checking if the provided username and password match the stored credentials 
        and if the password meets the strong password criteria.

        Args:
            username (str): The username to authenticate.
            password (str): The password to validate and match with the stored credentials.

        Returns:
            bool: True if the username exists and the password matches the stored credentials and meets the strong password criteria, False otherwise.
        """
        if self.validatePassword(password):
            return self.userCredentials.get(username) == password
        return False

    def validatePassword(self, password):
        """
        Validates a password against a strong password policy.

        Args:
            password (str): The password to be validated.

        Returns:
            bool: True if the password meets the strong password criteria, False otherwise.
        """
        pattern = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&\-])[A-Za-z\d@$!%*?&\-]{8,}$')
        return pattern.match(password) is not None
