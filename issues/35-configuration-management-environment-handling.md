# Configuration Management and Environment Handling

## Priority: Medium
## Category: DevOps/Infrastructure
## Estimated Effort: Medium (2-3 weeks)

## Problem Statement
The SFM system lacks a robust configuration management system for handling different environments (development, staging, production). Configuration is currently hardcoded or scattered across multiple files, making deployment and environment management difficult and error-prone.

## Current Issues

### Configuration Scattered
- Hardcoded values throughout the codebase
- No centralized configuration management
- Missing environment-specific settings
- Lack of configuration validation
- No configuration versioning

### Environment Management
- No clear separation between environments
- Missing environment-specific overrides
- Lack of secrets management
- No configuration hot-reloading
- Missing configuration documentation

### Security Concerns
- Secrets stored in code or plain text
- No encryption for sensitive configuration
- Missing access control for configuration
- Lack of audit trail for configuration changes

## Proposed Solution

### Phase 1: Configuration Architecture
```python
# config/config_manager.py
from typing import Any, Dict, Optional, Type, Union
from dataclasses import dataclass, field
from pathlib import Path
import os
import yaml
import json
from abc import ABC, abstractmethod

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    name: str = "sfm_db"
    username: str = "sfm_user"
    password: str = ""
    pool_size: int = 10
    timeout: int = 30

@dataclass
class CacheConfig:
    backend: str = "redis"
    host: str = "localhost"
    port: int = 6379
    ttl: int = 3600
    max_size: int = 10000

@dataclass
class APIConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: list = field(default_factory=lambda: ["*"])
    rate_limit: str = "100/hour"
    jwt_secret: str = ""

@dataclass
class SFMConfig:
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    api: APIConfig = field(default_factory=APIConfig)

class ConfigLoader:
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self._find_config_file()
        self.environment = os.getenv('SFM_ENV', 'development')
    
    def load_config(self) -> SFMConfig:
        """Load configuration from files and environment variables"""
        # Load base configuration
        base_config = self._load_from_file('config.yml')
        
        # Load environment-specific overrides
        env_config = self._load_from_file(f'config.{self.environment}.yml')
        
        # Apply environment variable overrides
        env_overrides = self._load_from_env()
        
        # Merge configurations
        merged_config = self._merge_configs(base_config, env_config, env_overrides)
        
        # Validate and create config object
        return self._create_config_object(merged_config)
```

### Phase 2: Environment-Specific Configuration
```yaml
# config/config.yml (base configuration)
environment: development
debug: false
log_level: INFO

database:
  host: localhost
  port: 5432
  name: sfm_db
  pool_size: 10
  timeout: 30

cache:
  backend: memory
  ttl: 3600
  max_size: 1000

api:
  host: 0.0.0.0
  port: 8000
  cors_origins:
    - http://localhost:3000
  rate_limit: "100/hour"

# config/config.production.yml
environment: production
debug: false
log_level: WARNING

database:
  pool_size: 50
  timeout: 60

cache:
  backend: redis
  host: redis-cluster
  max_size: 100000

api:
  cors_origins:
    - https://sfm.example.com
  rate_limit: "1000/hour"
```

### Phase 3: Secrets Management
```python
# config/secrets_manager.py
from typing import Any, Dict
import boto3
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import hvac  # HashiCorp Vault client

class SecretsManager(ABC):
    @abstractmethod
    def get_secret(self, key: str) -> str:
        pass

class AWSSecretsManager(SecretsManager):
    def __init__(self, region: str = 'us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region)
    
    def get_secret(self, key: str) -> str:
        response = self.client.get_secret_value(SecretId=key)
        return response['SecretString']

class AzureKeyVaultManager(SecretsManager):
    def __init__(self, vault_url: str):
        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=vault_url, credential=credential)
    
    def get_secret(self, key: str) -> str:
        secret = self.client.get_secret(key)
        return secret.value

class VaultSecretsManager(SecretsManager):
    def __init__(self, url: str, token: str):
        self.client = hvac.Client(url=url, token=token)
    
    def get_secret(self, key: str) -> str:
        response = self.client.secrets.kv.v2.read_secret_version(path=key)
        return response['data']['data']['value']

class EnvironmentSecretsManager(SecretsManager):
    """Fallback for development - reads from environment variables"""
    def get_secret(self, key: str) -> str:
        return os.getenv(key, '')
```

## Implementation Tasks

### Core Configuration System
1. [ ] Design configuration schema
2. [ ] Implement configuration loader
3. [ ] Create environment-specific configs
4. [ ] Add configuration validation
5. [ ] Build configuration documentation

### Secrets Management
6. [ ] Implement secrets manager interface
7. [ ] Add cloud provider integrations
8. [ ] Create local secrets handling
9. [ ] Implement secret rotation
10. [ ] Add secrets audit logging

### Environment Management
11. [ ] Create environment detection system
12. [ ] Implement configuration merging
13. [ ] Add environment validation
14. [ ] Build deployment configuration
15. [ ] Create environment documentation

### Configuration Features
16. [ ] Implement hot configuration reloading
17. [ ] Add configuration caching
18. [ ] Create configuration API endpoints
19. [ ] Build configuration CLI tools
20. [ ] Add configuration monitoring

### Integration
21. [ ] Integrate with application startup
22. [ ] Update all modules to use config
23. [ ] Add configuration testing
24. [ ] Create migration scripts
25. [ ] Update deployment processes

## Technical Specifications

### Configuration Loading Priority
1. Default values (in dataclasses)
2. Base configuration file (config.yml)
3. Environment-specific file (config.{env}.yml)
4. Environment variables
5. Command-line arguments
6. Remote configuration (optional)

### Environment Variable Mapping
```python
# config/env_mapping.py
ENV_VAR_MAPPING = {
    'SFM_DATABASE_HOST': 'database.host',
    'SFM_DATABASE_PORT': 'database.port', 
    'SFM_DATABASE_NAME': 'database.name',
    'SFM_DATABASE_PASSWORD': 'database.password',
    'SFM_CACHE_BACKEND': 'cache.backend',
    'SFM_CACHE_HOST': 'cache.host',
    'SFM_API_JWT_SECRET': 'api.jwt_secret',
    'SFM_LOG_LEVEL': 'log_level',
    'SFM_DEBUG': 'debug'
}

def load_env_overrides() -> Dict[str, Any]:
    """Load configuration overrides from environment variables"""
    overrides = {}
    for env_var, config_path in ENV_VAR_MAPPING.items():
        value = os.getenv(env_var)
        if value is not None:
            set_nested_value(overrides, config_path, value)
    return overrides
```

### Configuration Validation
```python
# config/validation.py
from pydantic import BaseModel, validator
from typing import List

class DatabaseConfigModel(BaseModel):
    host: str
    port: int
    name: str
    username: str
    password: str
    pool_size: int
    timeout: int
    
    @validator('port')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v
    
    @validator('pool_size')
    def validate_pool_size(cls, v):
        if v < 1:
            raise ValueError('Pool size must be at least 1')
        return v

class SFMConfigModel(BaseModel):
    environment: str
    debug: bool
    log_level: str
    database: DatabaseConfigModel
    
    @validator('environment')
    def validate_environment(cls, v):
        valid_envs = ['development', 'staging', 'production']
        if v not in valid_envs:
            raise ValueError(f'Environment must be one of {valid_envs}')
        return v
    
    @validator('log_level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v not in valid_levels:
            raise ValueError(f'Log level must be one of {valid_levels}')
        return v
```

### Configuration CLI
```python
# cli/config_cli.py
import click
from config.config_manager import ConfigManager

@click.group()
def config():
    """Configuration management commands"""
    pass

@config.command()
def validate():
    """Validate current configuration"""
    try:
        config_manager = ConfigManager()
        config_manager.validate()
        click.echo("✓ Configuration is valid")
    except Exception as e:
        click.echo(f"✗ Configuration error: {e}")

@config.command()
@click.option('--key', required=True, help='Configuration key')
def get(key):
    """Get configuration value"""
    config_manager = ConfigManager()
    value = config_manager.get(key)
    click.echo(f"{key}: {value}")

@config.command()
@click.option('--env', required=True, help='Environment name')
def generate_template(env):
    """Generate configuration template for environment"""
    template = config_manager.generate_template(env)
    click.echo(template)
```

## Configuration Files Structure
```
config/
├── config.yml                 # Base configuration
├── config.development.yml     # Development overrides
├── config.staging.yml         # Staging overrides
├── config.production.yml      # Production overrides
├── config.test.yml           # Test environment
├── secrets/
│   ├── development.yml       # Local secrets (gitignored)
│   └── .env                  # Environment variables
└── schemas/
    └── config_schema.json    # Configuration schema
```

## Security Best Practices

### Secrets Handling
- Never commit secrets to version control
- Use encryption for secrets at rest
- Implement secret rotation
- Audit secret access
- Use least-privilege access

### Configuration Security
```python
# config/security.py
class SecureConfigLoader:
    def __init__(self):
        self.encryption_key = self._get_encryption_key()
    
    def encrypt_config(self, config_data: str) -> str:
        """Encrypt sensitive configuration data"""
        from cryptography.fernet import Fernet
        f = Fernet(self.encryption_key)
        return f.encrypt(config_data.encode()).decode()
    
    def decrypt_config(self, encrypted_data: str) -> str:
        """Decrypt configuration data"""
        from cryptography.fernet import Fernet
        f = Fernet(self.encryption_key)
        return f.decrypt(encrypted_data.encode()).decode()
```

## Testing Strategy
- Unit tests for configuration loading
- Integration tests for environment configs
- Validation tests for all config schemas
- Security tests for secrets handling
- Performance tests for config loading

## Dependencies
- pydantic (validation)
- PyYAML (YAML parsing)
- boto3 (AWS secrets)
- azure-keyvault-secrets (Azure)
- hvac (HashiCorp Vault)
- cryptography (encryption)
- click (CLI)

## Success Criteria
- All configuration centralized and validated
- Environment-specific deployments working
- Secure secrets management
- Zero hardcoded configuration values
- Fast configuration loading (<100ms)
- Complete configuration documentation

## Migration Plan
1. Create configuration schema
2. Move existing config to new system
3. Update all modules to use config manager
4. Deploy to staging for testing
5. Gradual production rollout
6. Remove old configuration code

## Related Issues
- #28-production-readiness
- #30-api-layer-security-hardening
- #32-comprehensive-logging-monitoring
- #12-security-validation
