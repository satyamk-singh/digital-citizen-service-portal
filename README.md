# Digital Citizen Service Portal

A hypothetical e-governance web application prototype for the YuvaIntern Junior Web Developer – E-Governance & Digital Services internship.

## Progress

- **Week 1:** Planning, requirements, user flow and high-level architecture.
- **Week 2:** Front-end development and UI/UX design using HTML, CSS and JavaScript.
- **Week 3:** Backend integration, relational database design, REST APIs, authentication, document handling, notifications, security and testing.

The Week 3 update builds on the existing citizen-facing UI instead of replacing it.

## Technology Stack

HTML5, CSS3, JavaScript, Python, Flask, SQLite and Git/GitHub.

## Run Locally

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\\.venv\\Scripts\\Activate.ps1
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Start the backend from the project root:

```bash
python -m backend.app
```

API: `http://127.0.0.1:5000`

Then open `index.html` in a modern browser while the backend is running.

## Demo Account

Email: `demo@citizen.local`  
Password: `Demo@12345`

This account is for local prototype testing only.

## Documentation

- `docs/API_DOCUMENTATION.md`
- `docs/DATABASE_SCHEMA.md`
- `docs/ARCHITECTURE.md`
- `docs/BACKUP_RECOVERY.md`
- `docs/SECURITY_NOTES.md`

## Testing

```bash
python -m unittest discover -s tests -v
```

## Disclaimer

This is a hypothetical internship project created for academic and learning purposes. It is not an official government portal and is not affiliated with any government department or public authority. India-inspired visual elements are decorative and educational, not official branding.
