import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_socketio import SocketIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

from utils.firestore_methods import FireMethods
from utils.ml_methods import CustML

# Load env variables from .env
load_dotenv()

# Init variables
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
json_creds = os.getenv("FIRE_JSON")
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# Setups
# Setup JWT
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

# Setup SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)

# Utils
ml = CustML()
fm = FireMethods(json_creds)

@app.route("/")
def index():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    try:
        if google.authorized:
            google_data = google.get(user_info_endpoint).json()
    except Exception as e:
        print(e)

    return render_template('index.j2',
                           google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint,
                           user_posts=fm.get_user_posts(fm.get_user_id_from_email("alice@example.com")))

@app.route('/login')
@limiter.limit("10 per minute")
def login():
    return redirect(url_for('google.login'))

@app.route('/loginjwt', methods=['POST'])
@limiter.limit("10 per minute")
def loginjwt():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    # Check if user exists in the database
    user = next((u for u in fm.get_all_api_users() if u["username"] == username), None)
    if not user or user["password"] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is JSON serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Protected route
@app.route('/get_alice')
@limiter.limit("10 per minute")
@jwt_required()
def get_alice():
    # Access the identity of the current user with get_jwt_identity
    #current_user = get_jwt_identity()
    user_id = fm.get_user_id_from_email("alice@example.com")
    return jsonify(fm.get_user_posts(user_id)), 200

@app.route('/get_all_users')
@limiter.limit("10 per minute")
@jwt_required()
def get_all_users():
    # Fetsch all users
    return jsonify(fm.get_all_users()), 200

# On client connect
@socketio.on('connect')
def handle_connect(text):
    print('Client connected')

# On client disconnect
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Define a WebSocket event for receiving text input
@socketio.on('message')
@cache.cached(timeout=60)
def handle_message(text):
    # Update context of the ML with current users
    new_context = fm.get_all_users()

    # Process the text and generate a response 
    response = ml.answer_question(text, new_context)

    # Send the response back to the client
    socketio.send(response)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, allow_unsafe_werkzeug=True)