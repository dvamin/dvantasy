# dvantasy
Fantasy Sports Service

## Libraries in use

### Flask
REST

### Flask-SQLAlchemy - migrations
Development setup
```commandline
dvantasy> PYTHONPATH=. FLASK_APP=python/src/service/service.py APP_SETTINGS="python.config.config.DevelopmentConfig" DATABASE_URL="sqlite:///dev.db" flask db init
dvantasy> PYTHONPATH=. FLASK_APP=python/src/service/service.py APP_SETTINGS="python.config.config.DevelopmentConfig" DATABASE_URL="sqlite:///dev.db" flask db migrate -m "Initial migration"
dvantasy> PYTHONPATH=. FLASK_APP=python/src/service/service.py APP_SETTINGS="python.config.config.DevelopmentConfig" DATABASE_URL="sqlite:///dev.db" flask db upgrade
```

## Database

### Development
SQLite

### Production
Postgres