# Security Policy

## Supported Versions

This is a **reference/demo repository**, not a production service. As such:

- No security guarantees are provided
- No production deployments should use this code without additional security hardening
- This code is provided "as-is" for demonstration and learning purposes

## Reporting a Vulnerability

If you discover a security vulnerability in this repository:

1. **Do NOT** open a public issue
2. Email security concerns to: [security contact email] (or use GitHub's private security advisory feature)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce (if applicable)
   - Potential impact

**Note:** Since this is a demo/reference repo, vulnerabilities are unlikely to affect production systems. However, we appreciate responsible disclosure for any issues found.

## Security Best Practices for Users

- **Never commit API keys or secrets** to this repository
- Use `.env` files (which are gitignored) for sensitive configuration
- Review the compliance checks before using generated content in production
- The MockProvider is safe for testing; OpenAIProvider requires valid API keys

