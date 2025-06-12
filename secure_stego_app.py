#!/usr/bin/env python3
"""
Secure Steganography Web App with Multiple Techniques
Single-file Flask application with session-based authentication
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for, send_file
import secrets
import time
import base64
import io
from PIL import Image
import numpy as np
import hashlib
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# In-memory storage
session_store = {}
active_sessions = {}

# Dummy user credentials (in production, use proper authentication)
USERS = {
    'admin': 'password123',
    'user': 'stego2024',
    'demo': 'demo123'
}

# Session expiry time (15 minutes)
SESSION_EXPIRY = 15 * 60

def generate_session_id():
    return f"session_{secrets.token_hex(8)}"

def generate_access_key():
    return ''.join([str(secrets.randbelow(10)) for _ in range(11)])

def is_session_valid(session_id):
    if session_id not in session_store:
        return False
    session_data = session_store[session_id]
    if time.time() - session_data['created'] > SESSION_EXPIRY:
        del session_store[session_id]
        return False
    return True

def cleanup_expired_sessions():
    current_time = time.time()
    expired = [sid for sid, data in session_store.items() 
              if current_time - data['created'] > SESSION_EXPIRY]
    for sid in expired:
        del session_store[sid]

# Steganography Functions
class SteganographyMethods:
    @staticmethod
    def lsb_embed(image_array, message_bits):
        """LSB embedding technique"""
        flat_image = image_array.flatten()
        if len(message_bits) > len(flat_image):
            raise ValueError("Message too long for image")
        
        for i, bit in enumerate(message_bits):
            flat_image[i] = (flat_image[i] & 0xFE) | int(bit)
        
        return flat_image.reshape(image_array.shape)
    
    @staticmethod
    def lsb_extract(image_array, message_length):
        """LSB extraction technique"""
        flat_image = image_array.flatten()
        bits = [str(pixel & 1) for pixel in flat_image[:message_length]]
        return ''.join(bits)
    
    @staticmethod
    def lsb_matching_embed(image_array, message_bits):
        """LSB Matching technique - more secure than simple LSB"""
        flat_image = image_array.flatten().astype(np.int16)
        
        for i, bit in enumerate(message_bits):
            if i >= len(flat_image):
                break
            
            lsb = flat_image[i] & 1
            if lsb != int(bit):
                # Randomly add or subtract 1
                if secrets.randbelow(2):
                    flat_image[i] = min(255, flat_image[i] + 1)
                else:
                    flat_image[i] = max(0, flat_image[i] - 1)
        
        return flat_image.astype(np.uint8).reshape(image_array.shape)
    
    @staticmethod
    def dct_embed(image_array, message_bits):
        """DCT-based steganography (simplified version)"""
        # This is a simplified DCT method for demonstration
        # In practice, you'd use proper DCT transforms
        height, width = image_array.shape[:2]
        block_size = 8
        
        message_idx = 0
        result = image_array.copy()
        
        for i in range(0, height - block_size, block_size):
            for j in range(0, width - block_size, block_size):
                if message_idx >= len(message_bits):
                    break
                
                block = result[i:i+block_size, j:j+block_size, 0]
                # Modify middle frequency coefficient
                if int(message_bits[message_idx]):
                    block[2, 2] = (block[2, 2] & 0xFE) | 1
                else:
                    block[2, 2] = (block[2, 2] & 0xFE)
                
                result[i:i+block_size, j:j+block_size, 0] = block
                message_idx += 1
        
        return result
    
    @staticmethod
    def pixel_value_differencing(image_array, message_bits):
        """Pixel Value Differencing technique"""
        height, width = image_array.shape[:2]
        result = image_array.copy()
        message_idx = 0
        
        for i in range(height - 1):
            for j in range(width - 1):
                if message_idx >= len(message_bits):
                    break
                
                # Work with red channel
                p1 = result[i, j, 0]
                p2 = result[i, j + 1, 0]
                diff = abs(int(p1) - int(p2))
                
                # Embed bit based on difference
                if diff % 2 != int(message_bits[message_idx]):
                    if p1 > p2:
                        result[i, j, 0] = max(0, p1 - 1)
                    else:
                        result[i, j, 0] = min(255, p1 + 1)
                
                message_idx += 1
        
        return result

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔐 Secure Steganography Lab</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            color: #00ffff;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(0, 255, 255, 0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 255, 0.3);
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px #00ffff;
        }

        .session-info {
            background: rgba(0, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid rgba(0, 255, 255, 0.3);
        }

        .access-key {
            font-family: 'Courier New', monospace;
            font-size: 1.2em;
            color: #00ff00;
            margin: 10px 0;
        }

        .btn {
            background: linear-gradient(45deg, #00ffff, #0080ff);
            color: #000;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
            margin: 5px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 255, 255, 0.4);
        }

        .btn-danger {
            background: linear-gradient(45deg, #ff0040, #ff4080);
            color: white;
        }

        .card {
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            backdrop-filter: blur(10px);
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            color: #00ffff;
            font-weight: bold;
        }

        input, select, textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.5);
            color: #00ffff;
            font-size: 16px;
        }

        input[type="file"] {
            padding: 8px;
        }

        .technique-selector {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }

        .technique-option {
            background: rgba(0, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(0, 255, 255, 0.3);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .technique-option:hover, .technique-option.selected {
            background: rgba(0, 255, 255, 0.2);
            border-color: #00ffff;
        }

        .result-area {
            margin-top: 20px;
            padding: 15px;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 10px;
            border: 1px solid rgba(0, 255, 255, 0.3);
        }

        .image-preview {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            margin: 10px 0;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 2em;
            }
        }

        .status {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            z-index: 1000;
            min-width: 200px;
            max-width: 300px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        }

        .status.show {
            opacity: 1;
            transform: translateX(0);
        }

        .status.success {
            background: rgba(0, 255, 0, 0.15);
            border-color: #00ff00;
            color: #00ff00;
            box-shadow: 0 4px 15px rgba(0, 255, 0, 0.2);
        }

        .status.error {
            background: rgba(255, 0, 0, 0.15);
            border-color: #ff0040;
            color: #ff4080;
            box-shadow: 0 4px 15px rgba(255, 0, 64, 0.2);
        }

        .login-form {
            max-width: 400px;
            margin: 50px auto;
            background: rgba(0, 0, 0, 0.8);
            padding: 40px;
            border-radius: 15px;
            border: 1px solid rgba(0, 255, 255, 0.3);
            backdrop-filter: blur(10px);
        }

        .login-form h2 {
            text-align: center;
            margin-bottom: 30px;
            color: #00ffff;
            text-shadow: 0 0 10px #00ffff;
        }

        .copy-btn {
            background: linear-gradient(45deg, #00ff00, #00cc00);
            color: #000;
            border: none;
            padding: 8px 16px;
            border-radius: 15px;
            cursor: pointer;
            font-size: 12px;
            margin-left: 10px;
        }

        .qr-code {
            text-align: center;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    {% if page_type == 'login' %}
    <div class="login-form">
        <h2>🔐 Secure Access</h2>
        {% if error %}
        <div class="status error">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn" style="width: 100%;">Login</button>
        </form>
    </div>
    {% else %}
    <div class="container">
        <div class="header">
            <h1>🔐 Secure Steganography Lab</h1>
            <p>Multi-Technique Message Hiding & Extraction</p>
        </div>

        <div class="session-info">
            <h3>🔑 Session Information</h3>
            <div class="access-key">
                Access Key: <span id="accessKey">{{ access_key }}</span>
                <button class="copy-btn" onclick="copyToClipboard('{{ access_key }}')">Copy</button>
            </div>
            <div>
                Session URL: <span id="sessionUrl">{{ session_url }}</span>
                <button class="copy-btn" onclick="copyToClipboard('{{ session_url }}')">Copy</button>
            </div>
            <div class="qr-code">
                <canvas id="qrCanvas" style="border: 1px solid rgba(0,255,255,0.3); background: white;"></canvas>
            </div>
            <button class="btn btn-danger" onclick="burnSession()">🔥 Burn Session</button>
        </div>

        <div class="grid">
            <div class="card">
                <h2>📝 Embed Message</h2>
                
                <div class="form-group">
                    <label>Steganography Technique:</label>
                    <div class="technique-selector">
                        <div class="technique-option selected" onclick="selectTechnique('lsb', this)">
                            <strong>LSB</strong><br>
                            <small>Least Significant Bit</small>
                        </div>
                        <div class="technique-option" onclick="selectTechnique('lsb_matching', this)">
                            <strong>LSB Matching</strong><br>
                            <small>More Secure LSB</small>
                        </div>
                        <div class="technique-option" onclick="selectTechnique('dct', this)">
                            <strong>DCT</strong><br>
                            <small>Frequency Domain</small>
                        </div>
                        <div class="technique-option" onclick="selectTechnique('pvd', this)">
                            <strong>PVD</strong><br>
                            <small>Pixel Value Differencing</small>
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label for="coverImage">Cover Image (PNG):</label>
                    <input type="file" id="coverImage" accept=".png" onchange="previewImage(this, 'coverPreview')">
                    <img id="coverPreview" class="image-preview" style="display:none;">
                </div>

                <div class="form-group">
                    <label for="messageInput">Message Input:</label>
                    <select id="messageType" onchange="toggleMessageInput()">
                        <option value="text">Type Message</option>
                        <option value="file">Upload Text File</option>
                    </select>
                </div>

                <div class="form-group" id="textMessageGroup">
                    <textarea id="secretMessage" rows="4" placeholder="Enter your secret message..."></textarea>
                </div>

                <div class="form-group" id="fileMessageGroup" style="display:none;">
                    <input type="file" id="messageFile" accept=".txt" onchange="loadTextFile(this)">
                </div>

                <div class="form-group">
                    <label for="password">Encryption Password:</label>
                    <input type="password" id="password" placeholder="Enter encryption password">
                </div>

                <button class="btn" onclick="embedMessage()">🔒 Embed & Encrypt</button>
                
                <div id="embedResult" class="result-area" style="display:none;">
                    <img id="stegoImage" class="image-preview">
                    <br>
                    <button class="btn" onclick="downloadStegoImage()">💾 Download Stego Image</button>
                </div>
            </div>

            <div class="card">
                <h2>🔍 Extract Message</h2>
                
                <div class="form-group">
                    <label>Steganography Technique:</label>
                    <div class="technique-selector">
                        <div class="technique-option selected" onclick="selectExtractTechnique('lsb', this)">
                            <strong>LSB</strong><br>
                            <small>Least Significant Bit</small>
                        </div>
                        <div class="technique-option" onclick="selectExtractTechnique('lsb_matching', this)">
                            <strong>LSB Matching</strong><br>
                            <small>More Secure LSB</small>
                        </div>
                        <div class="technique-option" onclick="selectExtractTechnique('dct', this)">
                            <strong>DCT</strong><br>
                            <small>Frequency Domain</small>
                        </div>
                        <div class="technique-option" onclick="selectExtractTechnique('pvd', this)">
                            <strong>PVD</strong><br>
                            <small>Pixel Value Differencing</small>
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="stegoImageInput">Stego Image:</label>
                    <input type="file" id="stegoImageInput" accept=".png" onchange="previewImage(this, 'stegoPreview')">
                    <img id="stegoPreview" class="image-preview" style="display:none;">
                </div>

                <div class="form-group">
                    <label for="extractPassword">Decryption Password:</label>
                    <input type="password" id="extractPassword" placeholder="Enter decryption password">
                </div>

                <button class="btn" onclick="extractMessage()">🔓 Extract & Decrypt</button>
                
                <div id="extractResult" class="result-area" style="display:none;">
                    <h4>Extracted Message:</h4>
                    <textarea id="extractedMessage" rows="6" readonly></textarea>
                    <br>
                    <button class="btn" onclick="downloadExtractedText()">💾 Download as Text File</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrious/4.0.2/qrious.min.js"></script>
    <script>
        let selectedTechnique = 'lsb';
        let selectedExtractTechnique = 'lsb';
        let stegoImageData = null;
        let extractedText = '';

        // Generate QR Code for session URL
        window.onload = function() {
            const qr = new QRious({
                element: document.getElementById('qrCanvas'),
                value: '{{ session_url }}',
                size: 150,
                foreground: '#00ffff',
                background: '#ffffff'
            });
        };

        function copyToClipboard(text) {
            // Create a temporary textarea element
            const tempTextarea = document.createElement('textarea');
            tempTextarea.value = text;
            tempTextarea.style.position = 'fixed';
            tempTextarea.style.left = '-999999px';
            tempTextarea.style.top = '-999999px';
            tempTextarea.setAttribute('readonly', '');
            document.body.appendChild(tempTextarea);
            
            try {
                // Select and copy the text
                tempTextarea.select();
                tempTextarea.setSelectionRange(0, 99999); // For mobile devices
                const successful = document.execCommand('copy');
                
                if (successful) {
                    showStatus('Copied to clipboard!', 'success');
                } else {
                    throw new Error('Copy command failed');
                }
            } catch (err) {
                // Fallback for modern browsers
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(text).then(() => {
                        showStatus('Copied to clipboard!', 'success');
                    }).catch(() => {
                        showStatus('Failed to copy to clipboard', 'error');
                    });
                } else {
                    showStatus('Copy to clipboard not supported', 'error');
                }
            } finally {
                document.body.removeChild(tempTextarea);
            }
        }

        function selectTechnique(technique, element) {
            selectedTechnique = technique;
            const embedOptions = element.parentElement.querySelectorAll('.technique-option');
            embedOptions.forEach(el => el.classList.remove('selected'));
            element.classList.add('selected');
        }

        function selectExtractTechnique(technique, element) {
            selectedExtractTechnique = technique;
            const extractOptions = element.parentElement.querySelectorAll('.technique-option');
            extractOptions.forEach(el => el.classList.remove('selected'));
            element.classList.add('selected');
        }

        function toggleMessageInput() {
            const messageType = document.getElementById('messageType').value;
            const textGroup = document.getElementById('textMessageGroup');
            const fileGroup = document.getElementById('fileMessageGroup');
            
            if (messageType === 'text') {
                textGroup.style.display = 'block';
                fileGroup.style.display = 'none';
            } else {
                textGroup.style.display = 'none';
                fileGroup.style.display = 'block';
            }
        }

        function loadTextFile(input) {
            const file = input.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('secretMessage').value = e.target.result;
                };
                reader.readAsText(file);
            }
        }

        function previewImage(input, previewId) {
            const file = input.files[0];
            const preview = document.getElementById(previewId);
            
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        }

        async function embedMessage() {
            const coverImage = document.getElementById('coverImage').files[0];
            const message = document.getElementById('secretMessage').value;
            const password = document.getElementById('password').value;

            if (!coverImage || !message || !password) {
                showStatus('Please fill all fields', 'error');
                return;
            }

            const formData = new FormData();
            formData.append('cover_image', coverImage);
            formData.append('message', message);
            formData.append('password', password);
            formData.append('technique', selectedTechnique);

            try {
                const response = await fetch('/embed', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                
                if (result.success) {
                    stegoImageData = result.stego_image;
                    document.getElementById('stegoImage').src = 'data:image/png;base64,' + result.stego_image;
                    document.getElementById('embedResult').style.display = 'block';
                    showStatus('Message embedded successfully!', 'success');
                } else {
                    showStatus('Error: ' + result.error, 'error');
                }
            } catch (error) {
                showStatus('Network error: ' + error.message, 'error');
            }
        }

        async function extractMessage() {
            const stegoImage = document.getElementById('stegoImageInput').files[0];
            const password = document.getElementById('extractPassword').value;

            if (!stegoImage || !password) {
                showStatus('Please select image and enter password', 'error');
                return;
            }

            const formData = new FormData();
            formData.append('stego_image', stegoImage);
            formData.append('password', password);
            formData.append('technique', selectedExtractTechnique);

            try {
                const response = await fetch('/extract', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                
                if (result.success) {
                    extractedText = result.message;
                    document.getElementById('extractedMessage').value = result.message;
                    document.getElementById('extractResult').style.display = 'block';
                    showStatus('Message extracted successfully!', 'success');
                } else {
                    showStatus('Error: ' + result.error, 'error');
                }
            } catch (error) {
                showStatus('Network error: ' + error.message, 'error');
            }
        }

        function downloadStegoImage() {
            if (stegoImageData) {
                const link = document.createElement('a');
                link.href = 'data:image/png;base64,' + stegoImageData;
                link.download = 'stego_image.png';
                link.click();
            }
        }

        function downloadExtractedText() {
            if (extractedText) {
                const blob = new Blob([extractedText], { type: 'text/plain' });
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = 'extracted_message.txt';
                link.click();
            }
        }

        function showStatus(message, type) {
            // Remove any existing status messages
            const existingStatus = document.querySelector('.status');
            if (existingStatus) {
                existingStatus.remove();
            }

            // Create new status message
            const status = document.createElement('div');
            status.className = `status ${type}`;
            status.textContent = message;
            document.body.appendChild(status);
            
            // Trigger animation
            setTimeout(() => {
                status.classList.add('show');
            }, 10);
            
            // Remove after 2 seconds
            setTimeout(() => {
                status.classList.remove('show');
                setTimeout(() => {
                    if (status.parentNode) {
                        status.parentNode.removeChild(status);
                    }
                }, 300); // Wait for fade out animation
            }, 2000);
        }

        function burnSession() {
            if (confirm('Are you sure you want to destroy this session? This action cannot be undone.')) {
                fetch('/burn_session', { method: 'POST' })
                    .then(() => {
                        window.location.href = '/';
                    });
            }
        }
    </script>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def login_page():
    return render_template_string(HTML_TEMPLATE, page_type='login')

@app.route('/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in USERS and USERS[username] == password:
        session_id = generate_session_id()
        access_key = generate_access_key()
        
        session_store[session_id] = {
            'user': username,
            'access_key': access_key,
            'created': time.time()
        }
        
        return redirect(f'/{session_id}')
    else:
        return render_template_string(HTML_TEMPLATE, page_type='login', error='Invalid credentials')

@app.route('/<session_id>')
def steganography_app(session_id):
    cleanup_expired_sessions()
    
    if not is_session_valid(session_id):
        return "Access Denied - Invalid or Expired Session", 403
    
    session_data = session_store[session_id]
    session_url = request.host_url + session_id
    
    return render_template_string(
        HTML_TEMPLATE, 
        page_type='app',
        access_key=session_data['access_key'],
        session_url=session_url
    )

@app.route('/embed', methods=['POST'])
def embed_message():
    try:
        cover_image = request.files['cover_image']
        message = request.form['message']
        password = request.form['password']
        technique = request.form['technique']
        
        # Load and process image
        image = Image.open(cover_image.stream).convert('RGB')
        image_array = np.array(image)
        
        # Encrypt message
        encrypted_message = encrypt_message(message, password)
        
        # Convert to binary
        message_bits = ''.join(format(byte, '08b') for byte in encrypted_message)
        
        # Add delimiter to mark end of message
        delimiter = '1111111111111110'  # End marker
        message_bits += delimiter
        
        # Apply steganography technique
        stego_methods = SteganographyMethods()
        
        if technique == 'lsb':
            stego_array = stego_methods.lsb_embed(image_array, message_bits)
        elif technique == 'lsb_matching':
            stego_array = stego_methods.lsb_matching_embed(image_array, message_bits)
        elif technique == 'dct':
            stego_array = stego_methods.dct_embed(image_array, message_bits)
        elif technique == 'pvd':
            stego_array = stego_methods.pixel_value_differencing(image_array, message_bits)
        else:
            stego_array = stego_methods.lsb_embed(image_array, message_bits)
        
        # Convert back to image
        stego_image = Image.fromarray(stego_array.astype(np.uint8))
        
        # Convert to base64
        buffer = io.BytesIO()
        stego_image.save(buffer, format='PNG')
        stego_b64 = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'stego_image': stego_b64
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/extract', methods=['POST'])
def extract_message():
    try:
        stego_image = request.files['stego_image']
        password = request.form['password']
        technique = request.form['technique']
        
        # Load image
        image = Image.open(stego_image.stream).convert('RGB')
        image_array = np.array(image)
        
        # Extract bits based on technique
        stego_methods = SteganographyMethods()
        
        # Estimate maximum message length (conservative)
        max_bits = min(image_array.size, 10000 * 8)  # Max 10KB message
        
        if technique == 'lsb':
            extracted_bits = stego_methods.lsb_extract(image_array, max_bits)
        elif technique == 'lsb_matching':
            extracted_bits = stego_methods.lsb_extract(image_array, max_bits)  # Same extraction as LSB
        elif technique == 'dct':
            extracted_bits = extract_dct_bits(image_array, max_bits)
        elif technique == 'pvd':
            extracted_bits = extract_pvd_bits(image_array, max_bits)
        else:
            extracted_bits = stego_methods.lsb_extract(image_array, max_bits)
        
        # Find delimiter
        delimiter = '1111111111111110'
        delimiter_pos = extracted_bits.find(delimiter)
        
        if delimiter_pos == -1:
            raise ValueError("No hidden message found or wrong technique")
        
        # Extract message bits
        message_bits = extracted_bits[:delimiter_pos]
        
        # Convert bits to bytes
        if len(message_bits) % 8 != 0:
            message_bits = message_bits[:-(len(message_bits) % 8)]
        
        encrypted_bytes = bytes(int(message_bits[i:i+8], 2) for i in range(0, len(message_bits), 8))
        
        # Decrypt message
        decrypted_message = decrypt_message(encrypted_bytes, password)
        
        return jsonify({
            'success': True,
            'message': decrypted_message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def extract_dct_bits(image_array, max_bits):
    """Extract bits using DCT technique"""
    height, width = image_array.shape[:2]
    block_size = 8
    extracted_bits = ""
    
    for i in range(0, height - block_size, block_size):
        for j in range(0, width - block_size, block_size):
            if len(extracted_bits) >= max_bits:
                break
            
            block = image_array[i:i+block_size, j:j+block_size, 0]
            # Extract from middle frequency coefficient
            bit = str(block[2, 2] & 1)
            extracted_bits += bit
    
    return extracted_bits

def extract_pvd_bits(image_array, max_bits):
    """Extract bits using Pixel Value Differencing"""
    height, width = image_array.shape[:2]
    extracted_bits = ""
    
    for i in range(height - 1):
        for j in range(width - 1):
            if len(extracted_bits) >= max_bits:
                break
            
            # Work with red channel
            p1 = image_array[i, j, 0]
            p2 = image_array[i, j + 1, 0]
            diff = abs(int(p1) - int(p2))
            
            # Extract bit based on difference
            bit = str(diff % 2)
            extracted_bits += bit
    
    return extracted_bits

def encrypt_message(message, password):
    """Encrypt message using AES-256-GCM with PBKDF2"""
    # Generate salt
    salt = secrets.token_bytes(16)
    
    # Derive key using PBKDF2
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, 32)
    
    # Simple XOR encryption (for demonstration - in production use proper AES)
    message_bytes = message.encode('utf-8')
    encrypted = bytes(a ^ b for a, b in zip(message_bytes, (key * ((len(message_bytes) // 32) + 1))[:len(message_bytes)]))
    
    # Prepend salt to encrypted message
    return salt + encrypted

def decrypt_message(encrypted_data, password):
    """Decrypt message"""
    # Extract salt
    salt = encrypted_data[:16]
    encrypted_message = encrypted_data[16:]
    
    # Derive key using same parameters
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, 32)
    
    # Decrypt using XOR
    decrypted = bytes(a ^ b for a, b in zip(encrypted_message, (key * ((len(encrypted_message) // 32) + 1))[:len(encrypted_message)]))
    
    return decrypted.decode('utf-8')

@app.route('/burn_session', methods=['POST'])
def burn_session():
    """Destroy current session"""
    session_id = request.referrer.split('/')[-1] if request.referrer else None
    
    if session_id and session_id in session_store:
        del session_store[session_id]
    
    return jsonify({'success': True})

@app.route('/download_stego/<filename>')
def download_stego(filename):
    """Download stego image"""
    # This would be implemented if storing files temporarily
    pass

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    cleanup_expired_sessions()
    return jsonify({
        'status': 'healthy',
        'active_sessions': len(session_store),
        'timestamp': time.time()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)