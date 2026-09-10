# Week 3 Database Schema

The prototype uses SQLite as a lightweight relational database. The schema separates users, services, applications, appointments, documents and notifications.

## Tables

- **users**: `id`, `name`, `email`, `password_hash`, `phone`, `role`, `created_at`
- **services**: `id`, `name`, `category`, `description`, `status`
- **applications**: `id`, `user_id` → users.id, `service_id` → services.id, `application_number`, `status`, `submitted_at`, `updated_at`
- **appointments**: `id`, `user_id` → users.id, `department`, `appointment_date`, `appointment_time`, `status`, `created_at`
- **documents**: `id`, `user_id` → users.id, `application_id` → applications.id, `filename`, `document_type`, `storage_path`, `status`, `uploaded_at`
- **notifications**: `id`, `user_id` → users.id, `application_id` → applications.id, `title`, `message`, `is_read`, `created_at`

## Relationships

- One user can have many applications, appointments, documents and notifications.
- One service can have many applications.
- An application can have multiple documents.
- A notification can optionally reference an application.
- Foreign keys use SQLite referential integrity.

Indexes are added for application lookup, user ownership and notification retrieval.
