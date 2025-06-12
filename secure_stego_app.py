from flask import Flask, render_template_string, request, redirect, url_for, jsonify, session
import secrets
import string
import time
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# In-memory storage
session_store = {}
users = {"admin": "password", "user": "test123"}  # Simple user store for demo

def generate_session_id():
    return f"session_{secrets.token_urlsafe(16)}"

def generate_access_key():
    return ''.join(secrets.choice(string.digits) for _ in range(11))

def is_session_valid(session_id):
    if session_id in session_store:
        session_data = session_store[session_id]
        # Check if session expired (15 minutes)
        if datetime.now() - session_data['created'] < timedelta(minutes=15):
            return True
        else:
            # Clean up expired session
            del session_store[session_id]
    return False

@app.route('/')
def login_page():
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in users and users[username] == password:
        # Generate session
        session_id = generate_session_id()
        access_key = generate_access_key()
        
        session_store[session_id] = {
            'username': username,
            'access_key': access_key,
            'created': datetime.now()
        }
        
        return redirect(f'/{session_id}')
    else:
        return render_template_string(LOGIN_TEMPLATE, error="Invalid credentials")

@app.route('/<session_id>')
def steganography_app(session_id):
    if not is_session_valid(session_id):
        return render_template_string(ACCESS_DENIED_TEMPLATE), 403
    
    session_data = session_store[session_id]
    return render_template_string(STEGO_TEMPLATE, 
                                session_id=session_id,
                                access_key=session_data['access_key'],
                                username=session_data['username'])

@app.route('/burn/<session_id>', methods=['POST'])
def burn_session(session_id):
    if session_id in session_store:
        del session_store[session_id]
        return jsonify({"status": "success", "message": "Session destroyed"})
    return jsonify({"status": "error", "message": "Session not found"}), 404

# Templates
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureStego - Access Portal</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e);
            color: #00ffff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(0, 255, 255, 0.1) 0%, transparent 50%);
            animation: pulse 4s ease-in-out infinite alternate;
            z-index: -1;
        }
        
        @keyframes pulse {
            0% { opacity: 0.3; }
            100% { opacity: 0.6; }
        }
        
        .login-container {
            background: rgba(0, 20, 40, 0.3);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 15px;
            padding: 3rem;
            box-shadow: 
                0 8px 32px rgba(0, 255, 255, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            text-align: center;
            max-width: 400px;
            width: 90%;
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1); }
            to { box-shadow: 0 8px 32px rgba(0, 255, 255, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2); }
        }
        
        .logo {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
            animation: flicker 3s linear infinite;
        }
        
        @keyframes flicker {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .subtitle {
            color: #00bfff;
            margin-bottom: 2rem;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
            text-align: left;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            color: #00ffff;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px 15px;
            background: rgba(0, 40, 80, 0.2);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 8px;
            color: #00ffff;
            font-family: 'Courier New', monospace;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        input[type="text"]:focus, input[type="password"]:focus {
            outline: none;
            border-color: #00ffff;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
            background: rgba(0, 60, 120, 0.2);
        }
        
        .login-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(45deg, #0080ff, #00ffff);
            border: none;
            border-radius: 8px;
            color: #000;
            font-family: 'Courier New', monospace;
            font-size: 1rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }
        
        .login-btn:hover {
            background: linear-gradient(45deg, #00ffff, #0080ff);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 255, 255, 0.4);
        }
        
        .error {
            background: rgba(255, 0, 0, 0.1);
            border: 1px solid rgba(255, 0, 0, 0.3);
            color: #ff6b6b;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }
        
        .demo-info {
            margin-top: 2rem;
            padding: 1rem;
            background: rgba(0, 255, 255, 0.05);
            border-radius: 8px;
            border: 1px solid rgba(0, 255, 255, 0.1);
            font-size: 0.8rem;
            line-height: 1.4;
        }
        
        @media (max-width: 480px) {
            .login-container {
                padding: 2rem 1.5rem;
                margin: 1rem;
            }
            
            .logo {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <div class="login-container">
        <div class="logo">SecureStego</div>
        <div class="subtitle">Access Portal</div>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required autocomplete="username">
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required autocomplete="current-password">
            </div>
            
            <button type="submit" class="login-btn">Access System</button>
        </form>
        
        <div class="demo-info">
            <strong>Demo Credentials:</strong><br>
            Username: <code>admin</code> | Password: <code>password</code><br>
            Username: <code>user</code> | Password: <code>test123</code>
        </div>
    </div>
</body>
</html>
'''

ACCESS_DENIED_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Access Denied - SecureStego</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e);
            color: #ff4444;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        
        .container {
            background: rgba(40, 0, 0, 0.3);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 68, 68, 0.3);
            border-radius: 15px;
            padding: 3rem;
            max-width: 500px;
            width: 90%;
        }
        
        .error-code {
            font-size: 4rem;
            font-weight: bold;
            margin-bottom: 1rem;
            text-shadow: 0 0 20px rgba(255, 68, 68, 0.8);
        }
        
        .error-message {
            font-size: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .back-btn {
            display: inline-block;
            padding: 12px 30px;
            background: linear-gradient(45deg, #ff4444, #ff6666);
            color: #000;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        
        .back-btn:hover {
            background: linear-gradient(45deg, #ff6666, #ff4444);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 68, 68, 0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="error-code">403</div>
        <div class="error-message">Access Denied</div>
        <p>Your session is invalid or has expired.</p>
        <br>
        <a href="/" class="back-btn">Return to Login</a>
    </div>
</body>
</html>
'''

STEGO_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureStego - Session {{ session_id[-8:] }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e);
            color: #00ffff;
            min-height: 100vh;
            padding: 1rem;
        }
        
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(0, 255, 255, 0.05) 0%, transparent 50%);
            animation: pulse 4s ease-in-out infinite alternate;
            z-index: -1;
        }
        
        @keyframes pulse {
            0% { opacity: 0.3; }
            100% { opacity: 0.6; }
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background: rgba(0, 20, 40, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 15px;
        }
        
        .logo {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 15px rgba(0, 255, 255, 0.8);
        }
        
        .session-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .info-card {
            background: rgba(0, 20, 40, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 10px;
            padding: 1rem;
        }
        
        .info-card h3 {
            color: #00bfff;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .access-key {
            font-size: 1.2rem;
            font-weight: bold;
            color: #00ffff;
            word-break: break-all;
            padding: 0.5rem;
            background: rgba(0, 60, 120, 0.2);
            border-radius: 5px;
            margin-bottom: 0.5rem;
        }
        
        .copy-btn, .burn-btn {
            padding: 8px 15px;
            background: linear-gradient(45deg, #0080ff, #00ffff);
            border: none;
            border-radius: 5px;
            color: #000;
            font-family: 'Courier New', monospace;
            font-size: 0.8rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-right: 0.5rem;
        }
        
        .burn-btn {
            background: linear-gradient(45deg, #ff4444, #ff6666);
        }
        
        .copy-btn:hover, .burn-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 3px 10px rgba(0, 255, 255, 0.3);
        }
        
        .burn-btn:hover {
            box-shadow: 0 3px 10px rgba(255, 68, 68, 0.3);
        }
        
        .main-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .panel {
            background: rgba(0, 20, 40, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 15px;
            padding: 2rem;
            height: fit-content;
        }
        
        .panel h2 {
            color: #00bfff;
            margin-bottom: 1.5rem;
            font-size: 1.3rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-align: center;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            color: #00ffff;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        input[type="text"], input[type="password"], input[type="file"], textarea {
            width: 100%;
            padding: 12px 15px;
            background: rgba(0, 40, 80, 0.2);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 8px;
            color: #00ffff;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
        
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        input:focus, textarea:focus {
            outline: none;
            border-color: #00ffff;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
            background: rgba(0, 60, 120, 0.2);
        }
        
        .action-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(45deg, #0080ff, #00ffff);
            border: none;
            border-radius: 8px;
            color: #000;
            font-family: 'Courier New', monospace;
            font-size: 1rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }
        
        .action-btn:hover {
            background: linear-gradient(45deg, #00ffff, #0080ff);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 255, 255, 0.4);
        }
        
        .action-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .result {
            margin-top: 1.5rem;
            padding: 1rem;
            background: rgba(0, 60, 120, 0.1);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 8px;
            display: none;
        }
        
        .success {
            border-color: rgba(0, 255, 0, 0.3);
            background: rgba(0, 100, 0, 0.1);
            color: #00ff88;
        }
        
        .error {
            border-color: rgba(255, 0, 0, 0.3);
            background: rgba(100, 0, 0, 0.1);
            color: #ff6b6b;
        }
        
        .preview {
            max-width: 100%;
            border-radius: 8px;
            margin-top: 1rem;
        }
        
        .download-link {
            display: inline-block;
            margin-top: 1rem;
            padding: 10px 20px;
            background: rgba(0, 255, 255, 0.1);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 5px;
            color: #00ffff;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .download-link:hover {
            background: rgba(0, 255, 255, 0.2);
            transform: translateY(-1px);
        }
        
        @media (max-width: 768px) {
            .main-container {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            
            .session-info {
                grid-template-columns: 1fr;
            }
            
            .panel {
                padding: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <div class="header">
        <div class="logo">SecureStego</div>
        <div>Welcome, {{ username }} | Session: {{ session_id[-8:] }}</div>
    </div>
    
    <div class="session-info">
        <div class="info-card">
            <h3>Access Key</h3>
            <div class="access-key" id="accessKey">{{ access_key }}</div>
            <button class="copy-btn" onclick="copyAccessKey()">Copy Key</button>
            <button class="burn-btn" onclick="burnSession()">Burn Session</button>
        </div>
        <div class="info-card">
            <h3>Session URL</h3>
            <div class="access-key">{{ request.url }}</div>
            <button class="copy-btn" onclick="copyURL()">Copy URL</button>
        </div>
    </div>
    
    <div class="main-container">
        <!-- Embed Panel -->
        <div class="panel">
            <h2>🔒 Embed Message</h2>
            <form id="embedForm">
                <div class="form-group">
                    <label for="coverImage">Cover Image (PNG)</label>
                    <input type="file" id="coverImage" accept="image/png" required>
                </div>
                
                <div class="form-group">
                    <label for="secretMessage">Secret Message</label>
                    <textarea id="secretMessage" placeholder="Enter your secret message..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="embedPassword">Encryption Password</label>
                    <input type="password" id="embedPassword" placeholder="Enter encryption password" required>
                </div>
                
                <button type="submit" class="action-btn" id="embedBtn">Embed Message</button>
            </form>
            
            <div id="embedResult" class="result"></div>
        </div>
        
        <!-- Extract Panel -->
        <div class="panel">
            <h2>🔓 Extract Message</h2>
            <form id="extractForm">
                <div class="form-group">
                    <label for="stegoImage">Stego Image (PNG)</label>
                    <input type="file" id="stegoImage" accept="image/png" required>
                </div>
                
                <div class="form-group">
                    <label for="extractPassword">Decryption Password</label>
                    <input type="password" id="extractPassword" placeholder="Enter decryption password" required>
                </div>
                
                <button type="submit" class="action-btn" id="extractBtn">Extract Message</button>
            </form>
            
            <div id="extractResult" class="result"></div>
        </div>
    </div>

    <script>
        // Utility functions
        function copyAccessKey() {
            const accessKey = document.getElementById('accessKey').textContent;
            navigator.clipboard.writeText(accessKey).then(() => {
                showNotification('Access key copied to clipboard!');
            });
        }
        
        function copyURL() {
            navigator.clipboard.writeText(window.location.href).then(() => {
                showNotification('Session URL copied to clipboard!');
            });
        }
        
        function burnSession() {
            if (confirm('Are you sure you want to destroy this session? This action cannot be undone.')) {
                fetch(`/burn/{{ session_id }}`, { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        alert('Session destroyed. You will be redirected to the login page.');
                        window.location.href = '/';
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Error destroying session.');
                    });
            }
        }
        
        function showNotification(message) {
            // Simple notification - you could enhance this
            const notification = document.createElement('div');
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: rgba(0, 255, 255, 0.9);
                color: #000;
                padding: 10px 20px;
                border-radius: 5px;
                z-index: 1000;
                font-weight: bold;
            `;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 3000);
        }
        
        // Crypto functions
        async function deriveKey(password, salt) {
            const encoder = new TextEncoder();
            const keyMaterial = await crypto.subtle.importKey(
                'raw',
                encoder.encode(password),
                { name: 'PBKDF2' },
                false,
                ['deriveKey']
            );
            
            return crypto.subtle.deriveKey(
                {
                    name: 'PBKDF2',
                    salt: salt,
                    iterations: 100000,
                    hash: 'SHA-256'
                },
                keyMaterial,
                { name: 'AES-GCM', length: 256 },
                false,
                ['encrypt', 'decrypt']
            );
        }
        
        async function encryptMessage(message, password) {
            const encoder = new TextEncoder();
            const salt = crypto.getRandomValues(new Uint8Array(16));
            const iv = crypto.getRandomValues(new Uint8Array(12));
            
            const key = await deriveKey(password, salt);
            const encrypted = await crypto.subtle.encrypt(
                { name: 'AES-GCM', iv: iv },
                key,
                encoder.encode(message)
            );
            
            // Combine salt, iv, and encrypted data
            const combined = new Uint8Array(salt.length + iv.length + encrypted.byteLength);
            combined.set(salt, 0);
            combined.set(iv, salt.length);
            combined.set(new Uint8Array(encrypted), salt.length + iv.length);
            
            return combined;
        }
        
        async function decryptMessage(encryptedData, password) {
            const salt = encryptedData.slice(0, 16);
            const iv = encryptedData.slice(16, 28);
            const encrypted = encryptedData.slice(28);
            
            const key = await deriveKey(password, salt);
            const decrypted = await crypto.subtle.decrypt(
                { name: 'AES-GCM', iv: iv },
                key,
                encrypted
            );
            
            return new TextDecoder().decode(decrypted);
        }
        
        // Steganography functions
        function embedDataInImage(imageData, data) {
            const pixels = imageData.data;
            const binaryData = Array.from(data).map(byte => 
                byte.toString(2).padStart(8, '0')
            ).join('');
            
            // Add length header (32 bits)
            const lengthBinary = data.length.toString(2).padStart(32, '0');
            const fullBinary = lengthBinary + binaryData;
            
            if (fullBinary.length > pixels.length / 4) {
                throw new Error('Image too small for the data');
            }
            
            // LSB embedding
            for (let i = 0; i < fullBinary.length; i++) {
                const pixelIndex = i * 4; // RGB channels only, skip alpha
                const channel = i % 3; // Distribute across R, G, B channels
                const actualIndex = Math.floor(i / 3) * 4 + channel;
                
                if (actualIndex >= pixels.length) break;
                
                // Clear LSB and set new bit
                pixels[actualIndex] = (pixels[actualIndex] & 0xFE) | parseInt(fullBinary[i]);
            }
            
            return imageData;
        }
        
        function extractDataFromImage(imageData) {
            const pixels = imageData.data;
            
            // Extract length (32 bits)
            let lengthBinary = '';
            for (let i = 0; i < 32; i++) {
                const pixelIndex = i * 4;
                const channel = i % 3;
                const actualIndex = Math.floor(i / 3) * 4 + channel;
                
                if (actualIndex >= pixels.length) {
                    throw new Error('Invalid image data');
                }
                
                lengthBinary += (pixels[actualIndex] & 1).toString();
            }
            
            const dataLength = parseInt(lengthBinary, 2);
            if (dataLength <= 0 || dataLength > 1000000) { // Reasonable limit
                throw new Error('Invalid data length or no hidden data found');
            }
            
            // Extract data bits
            let dataBinary = '';
            const totalBits = dataLength * 8;
            
            for (let i = 0; i < totalBits; i++) {
                const bitIndex = i + 32; // Offset by length header
                const channel = bitIndex % 3;
                const actualIndex = Math.floor(bitIndex / 3) * 4 + channel;
                
                if (actualIndex >= pixels.length) {
                    throw new Error('Image data corrupted or incomplete');
                }
                
                dataBinary += (pixels[actualIndex] & 1).toString();
            }
            
            // Convert binary to bytes
            const extractedData = new Uint8Array(dataLength);
            for (let i = 0; i < dataLength; i++) {
                const binaryByte = dataBinary.substr(i * 8, 8);
                extractedData[i] = parseInt(binaryByte, 2);
            }
            
            return extractedData;
        }
        
        // Canvas utilities
        function loadImageToCanvas(file) {
            return new Promise((resolve, reject) => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                const img = new Image();
                
                img.onload = () => {
                    canvas.width = img.width;
                    canvas.height = img.height;
                    ctx.drawImage(img, 0, 0);
                    resolve({ canvas, ctx, imageData: ctx.getImageData(0, 0, img.width, img.height) });
                };
                
                img.onerror = reject;
                img.src = URL.createObjectURL(file);
            });
        }
        
        function downloadCanvas(canvas, filename) {
            const link = document.createElement('a');
            link.download = filename;
            link.href = canvas.toDataURL('image/png');
            link.click();
        }
        
        function downloadText(text, filename) {
            const blob = new Blob([text], { type: 'text/plain' });
            const link = document.createElement('a');
            link.download = filename;
            link.href = URL.createObjectURL(blob);
            link.click();
        }
        
        // Form handlers
        document.getElementById('embedForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const embedBtn = document.getElementById('embedBtn');
            const resultDiv = document.getElementById('embedResult');
            
            try {
                embedBtn.disabled = true;
                embedBtn.textContent = 'Processing...';
                resultDiv.style.display = 'none';
                
                const coverFile = document.getElementById('coverImage').files[0];
                const message = document.getElementById('secretMessage').value;
                const password = document.getElementById('embedPassword').value;
                
                if (!coverFile || !message || !password) {
                    throw new Error('Please fill in all fields');
                }
                
                // Load image
                const { canvas, ctx, imageData } = await loadImageToCanvas(coverFile);
                
                // Encrypt message
                const encryptedData = await encryptMessage(message, password);
                
                // Embed in image
                const stegoImageData = embedDataInImage(imageData, encryptedData);
                ctx.putImageData(stegoImageData, 0, 0);
                
                // Show result
                resultDiv.className = 'result success';
                resultDiv.innerHTML = `
                    <div><strong>✅ Message embedded successfully!</strong></div>
                    <img src="${canvas.toDataURL()}" class="preview" alt="Stego Image">
                    <br>
                    <button class="download-link" onclick="downloadCanvas(arguments[0], 'stego_image.png')" 
                            style="border:none;cursor:pointer;" data-canvas>Download Stego Image</button>
                `;
                
                // Store canvas reference for download
                const downloadBtn = resultDiv.querySelector('[data-canvas]');
                downloadBtn.onclick = () => downloadCanvas(canvas, 'stego_image.png');
                
                resultDiv.style.display = 'block';
                
            } catch (error) {
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `<strong>❌ Error:</strong> ${error.message}`;
                resultDiv.style.display = 'block';
            } finally {
                embedBtn.disabled = false;
                embedBtn.textContent = 'Embed Message';
            }
        });
        
        document.getElementById('extractForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const extractBtn = document.getElementById('extractBtn');
            const resultDiv = document.getElementById('extractResult');
            
            try {
                extractBtn.disabled = true;
                extractBtn.textContent = 'Processing...';
                resultDiv.style.display = 'none';
                
                const stegoFile = document.getElementById('stegoImage').files[0];
                const password = document.getElementById('extractPassword').value;
                
                if (!stegoFile || !password) {
                    throw new Error('Please select an image and enter the password');
                }
                
                // Load image
                const { imageData } = await loadImageToCanvas(stegoFile);
                
                // Extract encrypted data
                const encryptedData = extractDataFromImage(imageData);
                
                // Decrypt message
                const decryptedMessage = await decryptMessage(encryptedData, password);
                
                // Show result
                resultDiv.className = 'result success';
                resultDiv.innerHTML = `
                    <div><strong>✅ Message extracted successfully!</strong></div>
                    <div style="margin-top: 1rem;">
                        <strong>Decrypted Message:</strong><br>
                        <textarea readonly style="width:100%;height:150px;margin-top:0.5rem;">${decryptedMessage}</textarea>
                    </div>
                    <button class="download-link" onclick="downloadText('${decryptedMessage.replace(/'/g, "\\'")}', 'extracted_message.txt')" 
                            style="border:none;cursor:pointer;">Download as Text File</button>
                `;
                resultDiv.style.display = 'block';
                
            } catch (error) {
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `<strong>❌ Error:</strong> ${error.message}`;
                resultDiv.style.display = 'block';
            } finally {
                extractBtn.disabled = false;
                extractBtn.textContent = 'Extract Message';
            }
        });
        
        // Auto-expire session warning (optional)
        let sessionWarned = false;
        setTimeout(() => {
            if (!sessionWarned) {
                sessionWarned = true;
                if (confirm('Session will expire in 2 minutes. Continue working?')) {
                    // Reset timer (in a real app, you'd refresh the session)
                    sessionWarned = false;
                }
            }
        }, 13 * 60 * 1000); // 13 minutes (2 min before 15 min expiry)
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    print("🔐 SecureStego Server Starting...")
    print("📍 Demo Credentials:")
    print("   Username: admin | Password: password")
    print("   Username: user  | Password: test123")
    print("🌐 Access: http://localhost:5000")
    print("⚠️  All sessions stored in memory only (resets on restart)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)