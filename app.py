from flask import Flask, render_template, request, redirect, url_for, session, flash
from Captcha import Captcha
from UserAuthentication import UserAuthentication
from VenueManagement import VenueManagement

app = Flask(__name__)
app.secret_key = '!@#$%^&*()-=_+[]{}\|;:\'\"/.,<>?`~'

# Initialize services
captchaService = Captcha()
userAuthService = UserAuthentication()
venueManagementService = VenueManagement()

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
    Handles student login by authenticating credentials.
    
    If the credentials are valid, redirects to the main student page. 
    Otherwise, displays an error message.
    
    Returns:
        str: The rendered HTML of the student login page.
    """
    message = ''
    if request.method == 'POST':
        rollNo = request.form.get('roll_no')
        password = request.form.get('password')
        
        if userAuthService.authenticateStudent(rollNo, password):
            return redirect(url_for('mainStudent'))
        else:
            flash('Invalid credentials', 'error')
            message = 'Invalid credentials. Please try again.'
    
    return render_template('student_login.html', message=message)

@app.route('/memberLogin', methods=['GET', 'POST'])
def memberLogin():
    """
    Handles member login by authenticating credentials.
    
    If the credentials are valid, redirects to the main member page. 
    Otherwise, displays an error message.
    
    Returns:
        str: The rendered HTML of the member login page.
    """
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if userAuthService.authenticateMember(username, password):
            return redirect(url_for('mainMember'))
        else:
            flash('Invalid credentials', 'error')
            message = 'Invalid credentials. Please try again.'
    
    return render_template('member_login.html', message=message)

@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    """
    Handles the forgot password process, including CAPTCHA validation and password reset.
    
    If the user has exhausted attempts, they are redirected to the home page. 
    Otherwise, manages username submission, CAPTCHA validation, and new password entry.
    
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
    Initializes the attempt counter for the forgot password process if it doesn't already exist in the session.
    """
    if 'currentAttempts' not in session:
        session['currentAttempts'] = DEFAULT_ATTEMPTS

def decrementAttemptCounter():
    """
    Decreases the number of attempts remaining for the forgot password process by 1, 
    if there are still remaining attempts.
    """
    if session.get('currentAttempts', 0) > 0:
        session['currentAttempts'] -= 1

def resetAttemptCounter():
    """
    Resets the attempt counter to the default value.
    """
    session['currentAttempts'] = DEFAULT_ATTEMPTS

def areAttemptsExhausted():
    """
    Checks whether the number of allowed attempts for the forgot password process has been exhausted.
    
    Returns:
        bool: True if the attempts are exhausted, False otherwise.
    """
    return session.get('currentAttempts', 0) <= 0

def handleExhaustedAttempts():
    """
    Handles cases where the user has exhausted their allowed attempts for resetting the password.
    Resets the counter and redirects the user to the home page with a message.
    
    Returns:
        werkzeug.wrappers.response.Response: The response object for redirecting to the home page.
    """
    resetAttemptCounter()
    flash('Number of attempts are over. Redirecting to home page', 'error')
    return redirect(url_for('home'))

def handleUsernameSubmission():
    """
    Handles the submission of the username during the forgot password process.
    Upon valid submission, the CAPTCHA challenge is presented.
    
    Returns:
        str: The rendered HTML of the forgot password page with the CAPTCHA displayed.
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
    Handles the submission of the CAPTCHA and the new password during the forgot password process.
    Validates both the CAPTCHA input and the new password, and either proceeds with the reset or 
    prompts the user to try again.
    
    Returns:
        str: The rendered HTML of the forgot password page if validation fails, 
             or redirects to the home page upon success.
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
    Validates the provided CAPTCHA input and checks that the new password matches 
    the confirmation password and meets the required policy.
    
    Args:
        captchaInput (str): The input provided for the CAPTCHA validation.
        newPassword (str): The new password entered by the user.
        confirmPassword (str): The confirmation of the new password.
    
    Returns:
        bool: True if both the CAPTCHA and password validation pass, False otherwise.
    """
    return ('captchaSolution' in session and 
            captchaService.validateCaptcha(captchaInput) and 
            captchaService.validatePassword(newPassword, confirmPassword))

def renderForgotPasswordPage(showCaptcha=False, selectedImage=None, message=''):
    """
    Renders the forgot password page, optionally displaying the CAPTCHA and any error message.
    
    Args:
        showCaptcha (bool, optional): Whether to display the CAPTCHA section. Defaults to False.
        selectedImage (str, optional): The filename of the selected CAPTCHA image. Defaults to None.
        message (str, optional): Any message to display to the user. Defaults to an empty string.
    
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
    Renders the main dashboard for students, displaying their booked venues.
    
    Returns:
        str: The rendered HTML of the student main page with booking information.
    """
    bookings = venueManagementService.fetchBookedVenues()
    return render_template('main_student.html', bookings=bookings)

@app.route('/mainMember')
def mainMember():
    """
    Renders the main dashboard for members.
    
    Returns:
        str: The rendered HTML of the member main page.
    """
    return render_template('main_member.html')

if __name__ == '__main__':
    app.run(debug=True)