# Contributing to Secure Image Steganography Tool

Thank you for your interest in contributing to this project! We welcome contributions from developers of all skill levels.

## 🚀 Getting Started

### Prerequisites
- Modern web browser with developer tools
- Basic knowledge of HTML5, CSS3, and JavaScript
- Understanding of cryptography concepts (helpful but not required)
- Git for version control

### Setting Up Development Environment
1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/yourusername/secure-steganography.git
cd secure-steganography
```
3. Open `steganography_app.html` in your browser or serve it locally:
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx http-server

# Using PHP
php -S localhost:8000
```

## 🎯 Ways to Contribute

### 🐛 Bug Reports
- Use the GitHub Issues tab
- Search existing issues before creating new ones
- Include browser version and operating system
- Provide steps to reproduce the bug
- Include screenshots if applicable

### 💡 Feature Requests
- Discuss new features in GitHub Issues first
- Explain the use case and benefits
- Consider security implications
- Keep requests focused and specific

### 🔧 Code Contributions
- Bug fixes
- Performance improvements
- New steganography algorithms
- UI/UX enhancements
- Documentation improvements
- Test coverage additions

### 📚 Documentation
- README improvements
- Code comments
- Usage examples
- Security documentation
- Translation (if applicable)

## 📋 Development Guidelines

### Code Style
- Use consistent indentation (2 spaces)
- Follow existing naming conventions
- Write descriptive variable and function names
- Add comments for complex logic
- Keep functions focused and small

### JavaScript Standards
```javascript
// Good
function embedMessage(imageData, message, password) {
  // Clear, descriptive function name
  const encryptedData = this.encryptMessage(message, password);
  return this.embedLSB(imageData, encryptedData);
}

// Avoid
function doStuff(a, b, c) {
  // Unclear purpose and parameters
}
```

### CSS Guidelines
- Use modern CSS features appropriately
- Maintain responsive design principles
- Follow existing color scheme and design patterns
- Test across different screen sizes

### Security Requirements
- Never compromise encryption strength
- Use cryptographically secure random numbers
- Follow established security best practices
- Document security-related changes thoroughly

## 🔄 Pull Request Process

### Before Submitting
1. **Test Thoroughly**
   - Test in multiple browsers (Chrome, Firefox, Safari, Edge)
   - Test with different image sizes
   - Verify encryption/decryption works correctly
   - Check responsive design on mobile devices

2. **Code Quality**
   - Ensure code follows project style guidelines
   - Add appropriate comments
   - Remove debugging code and console.log statements
   - Verify no sensitive information is exposed

3. **Documentation**
   - Update README.md if adding new features
   - Add code comments for complex logic
   - Update SECURITY.md for security-related changes

### Submitting Pull Request
1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit:
```bash
git add .
git commit -m "Add: Clear description of changes"
```

3. Push to your fork:
```bash
git push origin feature/your-feature-name
```

4. Create Pull Request on GitHub with:
   - Clear title and description
   - Reference any related issues
   - List of changes made
   - Testing performed
   - Screenshots (if UI changes)

### Pull Request Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested in Chrome
- [ ] Tested in Firefox
- [ ] Tested in Safari
- [ ] Tested on mobile devices
- [ ] Encryption/decryption verified

## Related Issues
Fixes #(issue number)

## Screenshots
(If applicable)
```

## 🧪 Testing Guidelines

### Manual Testing Checklist
- [ ] **Basic Functionality**
  - Message embedding works
  - Message extraction works
  - Password protection functional
  - File upload/download works

- [ ] **Cross-Browser Testing**
  - Chrome (latest)
  - Firefox (latest)
  - Safari (latest)
  - Edge (latest)

- [ ] **Edge Cases**
  - Very large images
  - Very long messages
  - Special characters in messages
  - Empty/invalid inputs
  - Wrong passwords
  - Corrupted images

- [ ] **Security Testing**
  - Encrypted data appears random
  - Wrong password fails extraction
  - No sensitive data in console
  - No data sent to external servers

### Performance Testing
- Test with images of various sizes
- Monitor memory usage with large files
- Check processing time for complex operations
- Verify UI remains responsive

## 🏗️ Architecture Overview

### File Structure
```
steganography_app.html
├── HTML Structure
│   ├── Header section
│   ├── Embed section
│   ├── Extract section
│   └── Status displays
├── CSS Styling
│   ├── Dark theme
│   ├── Responsive design
│   └── Modern UI components
└── JavaScript Logic
    ├── SecureSteganography class
    ├── Encryption methods
    ├── Steganography algorithms
    ├── File handling
    └── UI management
```

### Key Components
- **SecureSteganography**: Main application class
- **Encryption**: AES-256-GCM with PBKDF2 key derivation
- **Steganography**: LSB and LSB Matching algorithms
- **File Management**: Canvas API for image processing
- **UI Controller**: Event handling and user feedback

## 🔒 Security Considerations

### Critical Security Rules
1. **Never weaken encryption**: Maintain AES-256-GCM standard
2. **Secure random generation**: Use crypto.getRandomValues()
3. **Key derivation**: Keep PBKDF2 with 100,000+ iterations
4. **Client-side only**: No server communication
5. **Memory safety**: Clear sensitive data when possible

### Security Review Process
All security-related changes require:
- Detailed explanation of security implications
- Testing with security focus
- Documentation of potential risks
- Review by security-conscious contributors

## 🌍 Internationalization

Currently, the application is in English only. Contributions for internationalization are welcome:
- Text externalization
- Multi-language support
- Right-to-left language support
- Cultural considerations for UI/UX

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Request Comments**: Code-specific discussions

### Questions Welcome
- "How does X work?"
- "Why was Y implemented this way?"
- "What's the best approach for Z?"
- "Can you review my idea before I code it?"

## 🎉 Recognition

### Contributors
All contributors will be recognized in:
- GitHub contributors list
- README.md acknowledgments section
- Release notes (for significant contributions)

### Types of Recognition
- **Code Contributors**: Listed in Git history and contributors page
- **Bug Reporters**: Credited in issue resolution
- **Security Researchers**: Special acknowledgment in SECURITY.md
- **Documentation**: Acknowledged for improving project docs

## 📜 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional communication
- Respect diverse perspectives

### Unacceptable Behavior
- Harassment or discrimination
- Offensive or inappropriate content
- Personal attacks or insults
- Sharing private information
- Deliberately disruptive behavior

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

**Happy Contributing!** 🚀

Your contributions help make secure communication more accessible to everyone. Whether you're fixing a typo or implementing a new feature, every contribution matters!