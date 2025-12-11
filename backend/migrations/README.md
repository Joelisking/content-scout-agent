# Database Migrations

This directory contains SQL migration scripts for the Content Scout database.

## Running Migrations

### Using psql

```bash
psql -U your_username -d content_scout -f migrations/add_fine_tuning_fields.sql
```

### Using Docker

If your database is running in Docker:

```bash
docker-compose exec db psql -U postgres -d content_scout -f /path/to/migrations/add_fine_tuning_fields.sql
```

### Using Python

You can also run migrations programmatically:

```python
from app.core.database import engine

with open('migrations/add_fine_tuning_fields.sql', 'r') as f:
    sql = f.read()

with engine.begin() as conn:
    conn.execute(sql)
```

## Migration Files

- `add_fine_tuning_fields.sql` - Adds optional fine-tuning fields to research_jobs table (custom title, word count, writing style, etc.)

## Notes

- All migrations use `IF NOT EXISTS` clauses to be idempotent
- Existing data will not be affected
- Default values are set for required fields
