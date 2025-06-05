# Security Policy

## Supported Versions

This project is currently maintained and security updates are provided for the latest version.

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < 1.0   | :x:                |

## Security Features

### Encryption Specifications
- **Algorithm**: AES-256-GCM (Advanced Encryption Standard with Galois/Counter Mode)
- **Key Size**: 256 bits
- **Key Derivation**: PBKDF2 with SHA-256
- **Iterations**: 100,000 (OWASP recommended minimum)
- **Salt**: 128-bit cryptographically secure random salt
- **IV**: 96-bit cryptographically secure random initialization vector
- **Authentication**: Built-in authentication with GCM mode

### Client-Side Security
- All cryptographic operations are performed client-side
- No data is transmitted to external servers
- Uses browser's Web Crypto API for secure random number generation
- Secure key derivation prevents rainbow table attacks

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

### How to Report
1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Send an email to [security@yourproject.com] with the following information:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact assessment
   - Any suggested fixes (if available)

### What to Expect
- **Initial Response**: Within 48 hours of your report
- **Status Updates**: Every 7 days until resolution
- **Resolution Timeline**: Critical issues within 30 days, others within 90 days
- **Credit**: Security researchers will be credited (with permission) in our security acknowledgments

### Security Vulnerability Types We're Interested In
- Cryptographic implementation flaws
- Key derivation weaknesses
- Random number generation issues
- Side-channel attacks
- Browser security bypasses
- Data leakage vulnerabilities

## Security Best Practices for Users

### Password Security
- Use strong, unique passwords (minimum 12 characters)
- Include uppercase, lowercase, numbers, and special characters
- Store passwords securely using a password manager
- Never share passwords through insecure channels

### Image Security
- Use high-quality PNG images for better security
- Avoid using images with predictable patterns
- Don't reuse the same cover image multiple times
- Store stego images securely and limit access

### Operational Security
- Clear browser cache after sensitive operations
- Use private/incognito browsing mode when possible
- Ensure your browser is up to date
- Only use the application on trusted devices
- Verify the application's integrity before use

## Known Security Considerations

### Limitations
- **Browser Dependency**: Security relies on browser's Web Crypto API implementation
- **Memory Security**: Browser memory management may leave traces
- **Side-Channel Attacks**: Timing attacks may be possible in some scenarios
- **File System**: Downloaded files may leave traces on disk

### Mitigation Strategies
- Use latest browser versions with security updates
- Clear browser data after use
- Use full-disk encryption on devices
- Implement proper file deletion practices

## Security Auditing

### Self-Assessment
This project has undergone internal security review focusing on:
- Cryptographic implementation correctness
- Key management practices
- Random number generation quality
- Browser API usage security

### Third-Party Audits
- No formal third-party security audits have been conducted yet
- Community security reviews are welcome and encouraged

## Compliance and Standards

### Standards Followed
- **NIST**: Following NIST cryptographic recommendations
- **OWASP**: Implementing OWASP secure coding practices
- **RFC Standards**: Adhering to relevant RFC specifications for cryptographic protocols

### Regulatory Considerations
- Users are responsible for compliance with local encryption laws
- Export restrictions may apply in some jurisdictions
- Data protection regulations (GDPR, CCPA) should be considered

## Security Changelog

### Version 1.0
- Initial implementation with AES-256-GCM encryption
- PBKDF2 key derivation with 100,000 iterations
- Secure random salt and IV generation
- Client-side only processing

## Contact Information

For security-related questions or concerns:
- Security Email: [security@yourproject.com]
- GPG Key: [Link to GPG public key if available]
- Security Policy Updates: Watch this repository for updates

---

**Important Notice**: This application is designed for legitimate privacy and security purposes. Users must comply with all applicable laws and regulations in their jurisdiction. The developers are not responsible for any misuse of this software.