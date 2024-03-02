import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_socketio import SocketIO, send
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
from firestore_methods import *

load_dotenv()
app = Flask(__name__)
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
app.config["SECRET_KEY"] = os.getenv('secret_key')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# Setup JWT
app.config['JWT_SECRET_KEY'] = os.getenv('secret_key')
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

# Load the pre-trained model and tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
model.eval()

# Define a function to process text and obtain sentiment prediction
def predict_sentiment(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted sentiment (0: negative, 1: positive)
    predicted_class = torch.argmax(outputs.logits, dim=1).item()
    sentiment = 'positive' if predicted_class == 1 else 'negative'

    return sentiment

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
                           user_posts=get_user_posts(get_user_id_from_email("alice@example.com")))

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
    user = next((u for u in get_all_api_users() if u["username"] == username), None)
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
    #current_user = get_jwt_identity()
    user_id = get_user_id_from_email("alice@example.com")
    return jsonify(get_user_posts(user_id)), 200

@socketio.on('connect')
def handle_connect(text):
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Define a WebSocket event for receiving text input
@socketio.on('message')
def handle_message(text):
    # Process the text and generate a response (you can replace this with your model logic)
    response = predict_sentiment(text)

    # Send the response back to the client
    socketio.send(response)

if __name__ == "__main__":
    socketio.run(app)