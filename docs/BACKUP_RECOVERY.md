# Backup, Recovery & Maintenance

## Backup
The SQLite database is stored as `database/portal.db`. For a prototype, a verified copy of this file can be taken after important changes and stored separately.

## Recovery
1. Stop the backend.
2. Preserve the damaged database if investigation is needed.
3. Restore the latest verified backup as `database/portal.db`.
4. Verify representative records and foreign-key integrity.
5. Restart the backend and run smoke tests.

## Maintenance
- Keep dependencies updated.
- Review logs and failed requests.
- Review database indexes as data grows.
- Test restore procedures periodically.
- Use managed database/object storage before real deployment.
