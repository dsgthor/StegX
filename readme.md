# 🔒 Secure Image Steganography Tool

A modern, browser-based steganography application that allows you to securely hide encrypted messages within PNG images using advanced cryptographic techniques.

![Steganography Demo](https://img.shields.io/badge/Status-Active-brightgreen) ![License](https://img.shields.io/badge/License-MIT-blue) ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)

## ✨ Features

- **🔐 Military-Grade Encryption**: Uses AES-256-GCM encryption with PBKDF2 key derivation
- **🖼️ Advanced Steganography**: Supports LSB (Least Significant Bit) and LSB Matching algorithms
- **🌐 Browser-Based**: No installation required - runs entirely in your web browser
- **🔒 Password Protection**: Secure your hidden messages with strong passwords
- **📱 Responsive Design**: Modern, mobile-friendly interface with dark theme
- **💾 File Support**: Upload text files or type messages directly
- **⚡ Real-Time Processing**: Fast embedding and extraction with progress indicators
- **🛡️ Client-Side Security**: All processing happens locally - no data sent to servers

## 🚀 Quick Start

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/secure-steganography.git
cd secure-steganography
```

2. **Open the application**:
   - Simply open `steganography_app.html` in any modern web browser
   - Or serve it using a local web server:
```bash
# Using Python 3
python -m http.server 8000

# Using Node.js (if you have http-server installed)
npx http-server

# Using PHP
php -S localhost:8000
```

3. **Start hiding messages**:
   - Upload a PNG image
   - Enter your secret message
   - Set a strong password
   - Download the stego image

## 🔧 How It Works

### Embedding Process
1. **Message Encryption**: Your message is encrypted using AES-256-GCM with a password-derived key
2. **Bit Conversion**: The encrypted data is converted to binary bits
3. **Steganographic Embedding**: Bits are hidden in the least significant bits of RGB channels
4. **Image Export**: The modified image is saved as a PNG file

### Extraction Process
1. **Bit Extraction**: Hidden bits are extracted from the RGB channels of the stego image
2. **Data Reconstruction**: Binary bits are converted back to encrypted data
3. **Decryption**: The encrypted data is decrypted using the provided password
4. **Message Recovery**: Your original message is revealed

## 🔐 Security Features

### Encryption Specifications
- **Algorithm**: AES-256-GCM (Galois/Counter Mode)
- **Key Derivation**: PBKDF2 with 100,000 iterations
- **Salt**: 128-bit random salt for each message
- **IV**: 96-bit random initialization vector
- **Hash Function**: SHA-256

### Steganography Methods

#### LSB (Least Significant Bit)
- Replaces the least significant bit of each color channel
- Maximum capacity: ~12.5% of image size
- Fast and reliable for most use cases

#### LSB Matching
- Uses ±1 modification instead of direct bit replacement
- More resistant to statistical analysis
- Slightly larger file size variations

## 📋 Supported Formats

- **Input Images**: PNG format only (preserves quality and supports lossless embedding)
- **Text Files**: UTF-8 encoded text files (.txt)
- **Output**: PNG images with embedded encrypted messages

## 🎯 Use Cases

- **Secure Communication**: Send confidential messages hidden in innocent-looking images
- **Digital Watermarking**: Embed copyright or ownership information
- **Data Backup**: Hide important text data within image files
- **Privacy Protection**: Conceal sensitive information in plain sight
- **Educational Purposes**: Learn about cryptography and steganography techniques

## 🔍 Capacity Guidelines

The maximum message size depends on your image dimensions:

| Image Size | Max Message Size (approx.) |
|------------|---------------------------|
| 800×600    | ~60KB of text |
| 1920×1080  | ~260KB of text |
| 3840×2160  | ~1MB of text |

*Formula: (Width × Height × 3) ÷ 8 = Maximum bytes*

## 🛡️ Security Best Practices

1. **Use Strong Passwords**: Minimum 12 characters with mixed case, numbers, and symbols
2. **Keep Passwords Secure**: Store passwords in a password manager
3. **Use High-Quality Images**: Larger images provide better security through increased capacity
4. **Verify Extraction**: Always test extraction immediately after embedding
5. **Secure Deletion**: Securely delete original images and messages after embedding

## 🌐 Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 60+ | ✅ Full Support |
| Firefox | 55+ | ✅ Full Support |
| Safari | 11+ | ✅ Full Support |
| Edge | 79+ | ✅ Full Support |

*Requires support for Web Crypto API and Canvas API*

## 🔬 Technical Details

### Dependencies
- **Web Crypto API**: For AES encryption and key derivation
- **Canvas API**: For image manipulation and pixel data access
- **File API**: For file reading and blob creation
- **No External Libraries**: Pure HTML5/JavaScript implementation

### Architecture
```
steganography_app.html
├── HTML Structure (UI Components)
├── CSS Styling (Modern Dark Theme)
└── JavaScript Logic
    ├── SecureSteganography Class
    ├── Encryption/Decryption Methods
    ├── Steganography Algorithms
    ├── File Handling
    └── UI Event Management
```

## 🚨 Limitations

- **PNG Only**: Only supports PNG images (JPEG compression would destroy hidden data)
- **Client-Side Only**: Requires JavaScript-enabled browser
- **Memory Intensive**: Large images may consume significant RAM during processing
- **No Mobile Camera**: Direct camera capture not implemented (upload from gallery works)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the Repository**
2. **Create a Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow existing code style and structure
- Test thoroughly across different browsers
- Update documentation for new features
- Ensure security best practices are maintained

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and legitimate privacy purposes only. Users are responsible for complying with local laws and regulations regarding encryption and data privacy. The authors are not responsible for any misuse of this software.

## 🙏 Acknowledgments

- Inspired by classical steganography techniques
- Built with modern web standards and security practices
- Thanks to the cryptography and security community for guidance

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/secure-steganography/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/secure-steganography/discussions)
- **Security Issues**: Please report privately via email

---

**Remember**: The security of your hidden messages depends on the strength of your password and the secrecy of the stego image. Keep both safe!