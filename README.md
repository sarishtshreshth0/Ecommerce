Flask Ecommerce Web Application
This Flask-based web application provides user authentication, email verification, contact form functionality, and user profile management using MongoDB as the backend database.
Dependencies
Flask
Flask-Mail
Flask-Session
pymongo
random
datetime
Configuration
The application is configured to connect to MongoDB using a connection URI. Email services are set up using Gmail SMTP.
app.secret_key = "securemore"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'yourmail' 
app.config['MAIL_PASSWORD'] = "yourpassword" 
app.config['MAIL_DEFAULT_SENDER'] = 'yourmail' 

Database Collections
db_user: Stores user details (first name, last name, email, mobile number, password)
db_otp: Stores OTPs for email verification
db_contact: Stores user contact messages
Routes
/login
Handles user login. Checks user credentials against the database and creates a session if valid.
/signup
Handles user registration. Stores user details in the database and redirects to OTP verification.
/verify
Handles OTP verification. Users must enter the received OTP to complete registration.
/logout
Clears the session and logs the user out.
/reset-password
Renders the password reset page.
/
Homepage route. Displays user information if logged in, otherwise shows login prompt.
/contact
Handles user inquiries. Messages are stored in the database and emailed to the user.
/ticketraise
Displays the total number of tickets raised by the user.
/raisedlist
Shows a list of raised tickets for the logged-in user.
/setting
Displays user profile settings such as name, email, and mobile number.
/giftcard
Renders the gift card page.
Functions
send_otp()
Generates a random 4-digit OTP, stores it in the database, and sends it via email.
send_mail(stored_otp)
Sends an email with the generated OTP to the registered email address.
Running the Application
To start the application:
python app.py

This will launch the application in debug mode.
Security Considerations
Use environment variables for storing credentials.
Implement password hashing before storing in the database.
Restrict database access using role-based permissions.
This documentation provides an overview of the application’s structure and functionalities.

