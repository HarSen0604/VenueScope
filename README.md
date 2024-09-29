# VenueScope Application

## Overview
VenueScope is a open sourced Flask-based web application that allows users to book venues and manage club events. It integrates MySQL for database operations, offers CAPTCHA functionality for user authentication, and enforces strong password policies.

## Tech Stack
- **Backend**: Flask (Python)
- **Database**: MySQL
- **Authentication**: `bcrypt` for password hashing and student authentication via the eCampus platform (using the `requests` library).
- **CAPTCHA**: Custom CAPTCHA challenge for password recovery.
- **Frontend**: HTML, CSS, and JavaScript

## Installation and Setup

### 1. Clone the Repository
Start by cloning the project repository:
```bash
git clone https://github.com/HarSen0604/VenueScope.git
cd VenueScope
```

### 2. Set Up Python Virtual Environment (Recommended)
Create and activate a virtual environment to manage dependencies:
```bash
python3 -m venv venv  # Create virtual environment
source venv/bin/activate  # On macOS/Linux
.\venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
Install the necessary Python packages:
```bash
pip3 install -r requirements.txt
```

### 4. MySQL Installation
Ensure that MySQL is installed. If it is not, download it from [MySQL's official site](https://dev.mysql.com/downloads/installer/).

### 5. Database Setup
Navigate to the directory containing the database initialization script (`DB_Init`), and execute it to set up the MySQL database and required tables:
```bash
chmod +x DB_Init.sh
./DB_Init.sh
```

This will:
- Create a MySQL database named `VenueScope`.
- Create the necessary tables and insert initial data.
- Clean up by removing SQL files after the script has been successfully executed.

### 6. MySQL Configuration
Update the MySQL connection credentials in the `UserAuthentication.py` and `VenueManagement.py` files to match your local MySQL setup.

### 7. Running the Application
Start the Flask development server:
```bash
python3 app.py
```

By default, the application will be available at: `http://127.0.0.1:5000`.

## Features

### User Login
- **Student Login**: Students log in using their institution's roll number and password, authenticated via the [PSG Tech eCampus platform](https://ecampus.psgtech.ac.in/studzone2/). The students can view the events available and register themselves.
- **Club Member Login**: Club members can log in using their email and password, which are securely stored and hashed using `bcrypt`.

### Venue Management
- Club members can:
  - Book venues.
  - View existing bookings.
  - Cancel their bookings.
- Venue bookings are validated to prevent time conflicts, ensuring that no venue is double-booked for the same time period.

### Forgot Password with CAPTCHA
- The password reset functionality includes a CAPTCHA challenge to prevent automated abuse.
- Users are allowed limited attempts to reset their passwords before being redirected back to the home page.

### MySQL Database Integration
- Club, member, and venue booking data is stored and managed using a MySQL database.

## Routes

| **Route**           | **Method** | **Description**                                          |
|---------------------|------------|----------------------------------------------------------|
| `/`                 | `GET`      | Renders the home page.                                   |
| `/studentLogin`     | `GET, POST`| Manages student login using roll number and password.     |
| `/memberLogin`      | `GET, POST`| Manages club member login using email and password.       |
| `/forgotPassword`   | `GET, POST`| Password recovery process with CAPTCHA challenge.         |
| `/mainStudent`      | `GET`      | Displays the student dashboard with a list of bookings.   |
| `/mainMember`       | `GET`      | Displays the club member dashboard and booking options.   |
| `/book_venue`       | `POST`     | Allows a club member to book a venue.                    |
| `/delete_booking`   | `POST`     | Allows a club member to delete a booked venue.            |

## Security

### Password Hashing
- Passwords are hashed and stored securely using `bcrypt`.

### CAPTCHA Protection
- CAPTCHA validation is implemented for the password recovery process, preventing automated abuse.

## System Requirements

- Python 3.x
- MySQL Server
- Internet connectivity for student authentication via [PSG Tech eCampus](https://ecampus.psgtech.ac.in/studzone2/).