# Week 3 API Documentation

Base URL: `http://127.0.0.1:5000`

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| GET | `/api/health` | API health check | No |
| POST | `/api/auth/register` | Create citizen account | No |
| POST | `/api/auth/login` | Start citizen session | No |
| POST | `/api/auth/logout` | End session | No |
| GET | `/api/services` | List active services | No |
| GET | `/api/services/<id>` | Get one service | No |
| GET | `/api/applications` | List current user's applications | Yes |
| POST | `/api/applications` | Submit application | Yes |
| GET | `/api/applications/<id>` | Get user's application | Yes |
| GET | `/api/applications/track/<number>` | Track by public reference | No |
| GET | `/api/appointments` | List user's appointments | Yes |
| POST | `/api/appointments` | Create appointment | Yes |
| GET | `/api/documents` | List user's documents | Yes |
| POST | `/api/documents` | Upload a document | Yes |
| GET | `/api/notifications` | List user's notifications | Yes |
| PATCH | `/api/notifications/<id>/read` | Mark notification read | Yes |
| GET | `/api/me` | Get current user | Yes |

## Example registration

```json
POST /api/auth/register
{
  "name": "Demo Citizen",
  "email": "citizen@example.com",
  "password": "StrongPass123"
}
```

The prototype uses cookie-based Flask sessions. Production deployment would require HTTPS, secure cookie configuration, CSRF protection, stronger operational secrets, centralized logging and additional controls.
