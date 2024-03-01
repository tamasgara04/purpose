import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

load_dotenv()
app = Flask(__name__)
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
app.secret_key = os.getenv('secret_key')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# Setup JWT
app.config['JWT_SECRET_KEY'] = "asd"
jwt = JWTManager(app)

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

# Mock database with 2 users
users = [
    {
        "username": "user1",
        "password": "password1"
    },
    {
        "username": "user2",
        "password": "password2"
    }
]

@app.route("/")
def index():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()

    return render_template('index.j2',
                           google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint)

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route('/loginjwt', methods=['POST'])
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
    user = next((u for u in users if u["username"] == username), None)
    if not user or user["password"] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is JSON serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Example protected route
@app.route('/protected')
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run()
