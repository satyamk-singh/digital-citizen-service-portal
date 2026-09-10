# Security Notes

Implemented in this prototype:

- Password hashing using Werkzeug.
- Parameterized SQLite queries.
- Input validation for key API fields.
- File extension and 5 MB size validation for document uploads.
- Session-based authentication.
- Foreign-key constraints and indexes.
- Environment-variable support for the Flask secret.

Not claimed as production-ready:

- Full CSRF protection
- HTTPS termination
- Centralized identity provider
- Malware scanning
- Production secret management
- Rate limiting/WAF
- Enterprise audit logging
- Enterprise backup infrastructure

A real deployment would require formal security, privacy, legal and accessibility review.
