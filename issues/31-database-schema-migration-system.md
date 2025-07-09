# Database Schema Migration System

## Priority: High
## Category: Data Management
## Estimated Effort: Large (2-3 weeks)

## Problem Statement
The SFM system lacks a proper database schema migration system, making it difficult to evolve the database structure safely in production environments. This creates risks for data integrity and deployment consistency.

## Current Issues

### Missing Migration Framework
- No versioned schema changes
- Manual database setup process
- Risk of schema drift between environments
- No rollback mechanism for failed migrations

### Data Integrity Concerns
- Missing foreign key constraints
- No data validation at database level
- Inconsistent indexing strategy
- Missing backup/restore procedures

### Environment Consistency
- Development/staging/production schema differences
- No automated schema deployment
- Manual data seeding process
- Missing environment-specific configurations

## Proposed Solution

### Phase 1: Migration Infrastructure
```python
# migrations/migration_manager.py
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Migration:
    version: str
    description: str
    up_sql: str
    down_sql: str
    timestamp: datetime

class MigrationManager:
    def __init__(self, db_connection):
        self.db = db_connection
        self._ensure_migration_table()
    
    def run_migrations(self) -> None:
        """Run all pending migrations"""
        pending = self._get_pending_migrations()
        for migration in pending:
            self._execute_migration(migration)
    
    def rollback(self, target_version: str) -> None:
        """Rollback to specific version"""
        pass
    
    def _get_pending_migrations(self) -> List[Migration]:
        """Get migrations not yet applied"""
        pass
```

### Phase 2: Schema Management
```sql
-- migrations/001_initial_schema.sql
CREATE TABLE IF NOT EXISTS sfm_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_type VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    properties JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sfm_nodes_type ON sfm_nodes(node_type);
CREATE INDEX idx_sfm_nodes_name ON sfm_nodes(name);
```

## Implementation Tasks

### Core Migration System
1. [ ] Create migration table structure
2. [ ] Implement MigrationManager class
3. [ ] Build migration file loader
4. [ ] Add version tracking
5. [ ] Implement rollback mechanism

### Schema Definitions
6. [ ] Design comprehensive schema
7. [ ] Add proper constraints and indexes
8. [ ] Create seed data migrations
9. [ ] Add data validation rules

### Tooling
10. [ ] Create migration CLI tools
11. [ ] Add migration status commands
12. [ ] Implement dry-run capability
13. [ ] Build migration testing framework

### Integration
14. [ ] Integrate with deployment pipeline
15. [ ] Add environment-specific configs
16. [ ] Create backup procedures
17. [ ] Document migration processes

## Technical Specifications

### Migration File Format
```python
# migrations/001_create_nodes_table.py
from migrations.base import Migration

class CreateNodesTable(Migration):
    version = "001"
    description = "Create base nodes table"
    
    def up(self):
        return """
        CREATE TABLE sfm_nodes (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            node_type VARCHAR(50) NOT NULL,
            properties JSONB
        );
        """
    
    def down(self):
        return "DROP TABLE IF EXISTS sfm_nodes;"
```

### CLI Interface
```bash
# Migration commands
python -m sfm.migrations status
python -m sfm.migrations migrate
python -m sfm.migrations rollback 001
python -m sfm.migrations create "add_user_table"
```

## Testing Strategy
- Unit tests for migration manager
- Integration tests for schema changes
- Performance tests for large migrations
- Rollback testing for all migrations

## Dependencies
- SQLAlchemy (if using ORM)
- psycopg2 (PostgreSQL driver)
- Click (CLI framework)
- pytest (testing)

## Success Criteria
- All schema changes versioned and tracked
- Automated migration deployment
- Successful rollback capability
- Consistent schemas across environments
- Zero-downtime deployment support

## Risk Mitigation
- Always backup before migrations
- Test migrations on staging first
- Implement migration timeouts
- Add data validation checks
- Monitor migration performance

## Related Issues
- #21-persistence-improvements
- #26-transaction-data-integrity
- #28-production-readiness
