import os
import re
import random

class Captcha:
    """
    A class to handle CAPTCHA functionalities including selecting a random image and validating CAPTCHA solutions and passwords.
    """
    
    def __init__(self):
        """
        Initializes the Captcha object, setting the folder path for CAPTCHA images and initializing attributes for selected image and solution.
        """
        CAPTCHA_FOLDER = 'static/assets/CAPTCHA'
        self.folderPath = CAPTCHA_FOLDER
        self.selectedImage = None
        self.solution = None

    def selectRandomImage(self):
        """
        Selects a random JPEG image from the CAPTCHA folder and sets it as the selected image.
        
        Returns:
            str: The filename of the selected image.
        
        Raises:
            FileNotFoundError: If no JPEG files are found in the CAPTCHA folder.
        """
        # Initialize an empty list to store valid jpg files
        jpg_files = []

        # Iterate over the files and collect only jpg files
        for file in os.listdir(self.folderPath):
            if file.endswith('.jpg'):
                jpg_files.append(file)
        
        # Check if any jpg files are found and pick a random one
        if jpg_files:
            self.selectedImage = random.choice(jpg_files)
            self.solution = os.path.splitext(self.selectedImage)[0]
            return self.selectedImage
        else:
            raise FileNotFoundError("No valid CAPTCHA images found in the folder")

    def validateCaptcha(self, userInput):
        """
        Validates the user's CAPTCHA input against the solution.
        
        Args:
            userInput (str): The CAPTCHA input provided by the user.
        
        Returns:
            bool: True if the user input matches the solution, False otherwise.
        """
        print(userInput, self.solution)
        return userInput == self.solution
    
    def validatePassword(self, newPassword, reEnterPassword):
        """
        Validates a new password against a strong password policy and checks if it matches the re-entered password.
        
        Args:
            newPassword (str): The new password to be validated.
            reEnterPassword (str): The re-entered password to be compared with the new password.
        
        Returns:
            bool: True if the passwords match and the new password meets the strong password criteria, False otherwise.
        """
        print(newPassword, reEnterPassword)
        if newPassword != reEnterPassword:
            return False

        pattern = re.compile(r'^(?=.*\d)'          # At least one digit
                            r'(?=.*[a-z])'        # At least one lowercase letter
                            r'(?=.*[A-Z])'        # At least one uppercase letter
                            r'(?=.*[@$!%*?&\-\_])'  # At least one special character (escaped hyphen)
                            r'[A-Za-z\d@$!%*?&\-\_]{8,}$')  # Minimum 8 characters, escape hyphen
        
        if pattern.match(newPassword):
            print("Password meets the policy.")
            return True
        else:
            print("Password does not meet the policy.")
            return False
