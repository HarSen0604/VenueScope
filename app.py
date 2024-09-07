from flask import Flask, render_template, request, redirect, url_for, session, flash
from Captcha import Captcha
from UserService import UserService

app = Flask(__name__)
app.secret_key = '!@#$%^&*()-=_+[]{}\|;:\'\"/.,<>?`~'

# Initialize services
captchaService = Captcha()
userService = UserService()

# Constants
DEFAULT_ATTEMPTS = 3

@app.route('/')
def home():
    """
    Renders the home page.

    Returns:
        str: The rendered HTML of the home page.
    """
    return render_template('home.html')

@app.route('/studentLogin', methods=['GET', 'POST'])
def studentLogin():
    """
    Handles student login. Authenticates user credentials and redirects to the student main page 
    if successful. Displays an error message on failure.

    Returns:
        str: The rendered HTML of the student login page.
    """
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Use the UserService to authenticate
        if userService.authenticate(username, password):
            return redirect(url_for('mainStudent'))
        else:
            flash('Invalid credentials', 'error')
            message = 'Invalid credentials. Please try again.'
    
    return render_template('student_login.html', message=message)

@app.route('/memberLogin', methods=['GET', 'POST'])
def memberLogin():
    """
    Handles member login. Authenticates user credentials and redirects to the member main page 
    if successful. Displays an error message on failure.

    Returns:
        str: The rendered HTML of the member login page.
    """
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Use the UserService to authenticate
        if userService.authenticate(username, password):
            return redirect(url_for('mainMember'))
        else:
            flash('Invalid credentials', 'error')
            message = 'Invalid credentials. Please try again.'
    
    return render_template('member_login.html', message=message)

@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    """
    Handles the forgot password process. Manages CAPTCHA and password validation, and attempts tracking.

    Returns:
        str: The rendered HTML of the forgot password page.
    """
    if areAttemptsExhausted():
        return handleExhaustedAttempts()
    
    initializeAttemptCounter()

    if request.method == 'POST':
        if 'username' in request.form:
            return handleUsernameSubmission()
        else:
            return handleCaptchaSubmission()
    
    return renderForgotPasswordPage()

def initializeAttemptCounter():
    """
    Initializes the attempt counter for the forgot password process if not already set.
    """
    if 'currentAttempts' not in session:
        session['currentAttempts'] = DEFAULT_ATTEMPTS

def decrementAttemptCounter():
    """
    Decrements the attempt counter by one if there are remaining attempts.
    """
    if session.get('currentAttempts', 0) > 0:
        session['currentAttempts'] -= 1

def resetAttemptCounter():
    """
    Resets the attempt counter to the default number of attempts.
    """
    session['currentAttempts'] = DEFAULT_ATTEMPTS

def areAttemptsExhausted():
    """
    Checks if the number of attempts for the forgot password process is exhausted.

    Returns:
        bool: True if attempts are exhausted, False otherwise.
    """
    return session.get('currentAttempts', 0) <= 0

def handleExhaustedAttempts():
    """
    Handles the case when the number of attempts is exhausted by resetting the counter and redirecting to the home page.

    Returns:
        werkzeug.wrappers.response.Response: The response object for redirecting to the home page.
    """
    resetAttemptCounter()
    flash('Number of attempts are over. Redirecting to home page', 'error')
    return redirect(url_for('home'))

def handleUsernameSubmission():
    """
    Handles the username submission during the forgot password process. Shows CAPTCHA for validation.

    Returns:
        str: The rendered HTML of the forgot password page with CAPTCHA.
    """
    username = request.form.get('username')
    showCaptcha = True
    selectedImage = captchaService.selectRandomImage()
    
    session['captchaSolution'] = captchaService.solution
    session['username'] = username
    session['selectedImage'] = selectedImage
    
    return renderForgotPasswordPage(showCaptcha, selectedImage)

def handleCaptchaSubmission():
    """
    Handles the CAPTCHA and password submission during the forgot password process. Validates CAPTCHA and new password.

    Returns:
        str: The rendered HTML of the forgot password page with a CAPTCHA error message if validation fails.
    """
    newPassword = request.form.get('newPassword')
    confirmPassword = request.form.get('reEnterPassword')
    captchaInput = request.form.get('otp')

    username = session.get('username')
    selectedImage = session.get('selectedImage')

    if isCaptchaAndPasswordValid(captchaInput, newPassword, confirmPassword):
        flash('Success!', 'success')
        return redirect(url_for('home'))
    else:
        decrementAttemptCounter()
        
        # Regenerate CAPTCHA on failed attempt
        selectedImage = captchaService.selectRandomImage()
        session['captchaSolution'] = captchaService.solution
        session['selectedImage'] = selectedImage

        flash('Invalid CAPTCHA or mismatched password, please try again.', 'error')
        message = 'Invalid CAPTCHA or mismatched password, please try again.'
        return renderForgotPasswordPage(showCaptcha=True, selectedImage=selectedImage, message=message)

def isCaptchaAndPasswordValid(captchaInput, newPassword, confirmPassword):
    """
    Validates the CAPTCHA input and new password against the CAPTCHA solution and password policy.

    Args:
        captchaInput (str): The input CAPTCHA value.
        newPassword (str): The new password to be validated.
        confirmPassword (str): The confirmation password to be validated.

    Returns:
        bool: True if CAPTCHA and passwords are valid, False otherwise.
    """
    return ('captchaSolution' in session and 
            captchaService.validateCaptcha(captchaInput) and 
            captchaService.validatePassword(newPassword, confirmPassword))

def renderForgotPasswordPage(showCaptcha=False, selectedImage=None, message=''):
    """
    Renders the forgot password page with optional CAPTCHA and message.

    Args:
        showCaptcha (bool, optional): Whether to display the CAPTCHA. Defaults to False.
        selectedImage (str, optional): The filename of the selected CAPTCHA image. Defaults to None.
        message (str, optional): The message to display on the page. Defaults to an empty string.

    Returns:
        str: The rendered HTML of the forgot password page.
    """
    attemptCounter = session.get('currentAttempts', DEFAULT_ATTEMPTS)
    
    return render_template('forgot_password.html', 
                           showCaptcha=showCaptcha, 
                           imageName=selectedImage,
                           attemptsRemaining=attemptCounter, 
                           message=message)

@app.route('/mainStudent')
def mainStudent():
    """
    Renders the main page for students.

    Returns:
        str: The rendered HTML of the student main page.
    """
    return render_template('main_student.html')

@app.route('/mainMember')
def mainMember():
    """
    Renders the main page for members.

    Returns:
        str: The rendered HTML of the member main page.
    """
    return render_template('main_member.html')

if __name__ == '__main__':
    app.run(debug=True)
