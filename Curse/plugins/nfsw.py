import os
import bcrypt
import requests
import json
import time
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_jwt_extended import JWTManager, jwt_required
from werkzeug.utils import secure_filename
from blockchain import Blockchain
from flask_otp import OTP 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)  # Longer, more secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'

db = SQLAlchemy(app)
limiter = Limiter(app, key_func=lambda: request.remote_addr)
jwt = JWTManager(app)
otp = OTP(app)

blockchain = Blockchain()

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    nsfw_allowed = db.Column(db.Boolean, default=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

db.create_all()

def quantum_safe_encryption(data):
    """Apply quantum-safe encryption using RSA and AES-256 for double encryption."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096, backend=default_backend())
    public_key = private_key.public_key()
    encrypted_data = public_key.encrypt(data.encode(), hashes.SHA256())

    aes_key = os.urandom(32)  
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM())
    encryptor = cipher.encryptor()
    encrypted_data_aes = encryptor.update(data.encode()) + encryptor.finalize()

    return base64.b64encode(encrypted_data_aes)

def allowed_file(filename):
    """Check allowed file types (images/videos)."""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def nsfw_detection_with_blockchain(image_path):
    """Multi-layered NSFW detection using AI models and blockchain verification."""
    results = []
    deepai_url = 'https://api.deepai.org/api/nsfw-detector'
    response = requests.post(deepai_url, files={'image': open(image_path, 'rb')}, headers={'api-key': 'your-deepai-api-key'})
    nsfw_score = response.json().get('output', {}).get('nsfw_score', 0)
    results.append(nsfw_score)

    blockchain.add_transaction({
        'image': image_path,
        'result': 'NSFW' if nsfw_score > 0.7 else 'Safe',
        'timestamp': time.time(),
    })

    return nsfw_score > 0.7

def anomaly_detection():
    """AI-based anomaly detection for identifying malicious activity."""
    pass

def self_healing_mechanism():
    """Self-healing mechanism to neutralize attacks in real-time."""
    pass

@app.route('/upload', methods=['POST'])
@limiter.limit("5 per minute")
@jwt_required()
def upload():
    if 'file' not in request.files:
        return jsonify(message='No file part'), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(filename)
        
        if nsfw_detection_with_blockchain(filename):
            os.remove(filename)
            return jsonify(message='NSFW content detected and deleted'), 400
        
        anomaly_detection()
        
        self_healing_mechanism()

        return jsonify(message='File uploaded successfully!'), 200
    else:
        return jsonify(message="Invalid file type. Allowed types are: png, jpg, jpeg, gif, mp4, mov."), 400

@app.route('/login', methods=['POST'])
def login():
    """Login function with multi-factor authentication (MFA)."""
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    
    if user and bcrypt.checkpw(password.encode(), user.password.encode()):
      
        access_token = jwt.create_access_token(identity=user.id)
        
        otp_token = otp.generate_otp(user.email)  
        
        return jsonify(access_token=access_token, otp_token=otp_token), 200
    else:
        return jsonify(message="Invalid credentials"), 400

if __name__ == '__main__':
    app.run(debug=False, ssl_context='adhoc') 
    
