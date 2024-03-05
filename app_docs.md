## Code Documentation

### Overview
This code implements a Flask application with various functionalities including authentication using Google OAuth, JWT token generation, fetching data from Firestore, handling WebSocket events, and implementing rate limiting and caching.

### Dependencies
- **os**: This module provides a portable way of using operating system-dependent functionality.
- **dotenv**: This module loads environment variables from a .env file into os.environ.
- **Flask**: A micro web framework for Python.
- **render_template, redirect, url_for, jsonify, request**: Flask modules for rendering templates, redirection, URL handling, JSON response handling, and request handling respectively.
- **flask_dance.contrib.google**: Flask-Dance extension for Google OAuth.
- **flask_jwt_extended**: Flask extension for JSON Web Tokens.
- **flask_socketio**: Flask extension for handling WebSocket connections.
- **flask_limiter**: Flask extension for rate limiting.
- **flask_caching**: Flask extension for caching.
- **utils.firestore_methods.FireMethods**: Custom module for interacting with Firestore.
- **utils.ml_methods.CustML**: Custom module for machine learning functionalities.

### Environment Setup
- The code loads environment variables from a .env file using `load_dotenv()` function.
- The environment variables include `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `FIRE_JSON`, and `SECRET_KEY`.

### Flask Application Setup
- Initializes a Flask application.
- Configures app settings including secret key and OAuth environment variables.
- Sets up JWT token management with a secret key.
- Initializes SocketIO for WebSocket communication.
- Sets up rate limiting using Flask Limiter.
- Configures Flask caching.

### Google OAuth Setup
- Initializes a Google OAuth blueprint for authentication.
- Registers the blueprint for login functionality.

### Routes
1. **/index**: Renders the index page with Google user data and posts.
2. **/login**: Redirects to Google OAuth login.
3. **/loginjwt**: Handles JWT login with username and password.
4. **/get_alice**: Protected route to get posts of a user named "Alice".
5. **/get_all_users**: Protected route to get all users' data.
6. **WebSocket events**: Handles WebSocket connections and message events.

### Functions
- **handle_connect**: Handles client connection to WebSocket.
- **handle_disconnect**: Handles client disconnection from WebSocket.
- **handle_message**: Handles message events on WebSocket, updates ML context, processes text, and sends responses.

### Execution
- Runs the Flask application with SocketIO support on host "0.0.0.0" and port 5001.
