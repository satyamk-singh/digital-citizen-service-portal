# Week 3 Backend Architecture

```text
Citizen Browser
      |
      v
HTML/CSS/JavaScript Frontend
      |
      | HTTP + JSON / multipart upload
      v
Flask REST API
      |
      +--> Authentication & Session
      +--> Service / Application Logic
      +--> Appointment Management
      +--> Document Validation & Storage
      +--> Notification Service
      |
      v
SQLite Relational Database
      |
      +--> users
      +--> services
      +--> applications
      +--> appointments
      +--> documents
      +--> notifications

Document files -> database/uploads/
```

This is an internship prototype architecture, not a production government system.
