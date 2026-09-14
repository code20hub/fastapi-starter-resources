'''
Light weight data migration tool for SQLAchemy for Python.
To start: alembic init <<folder_name>>; alembic/migrations

# Config for SQLModel:
# add the line to allow sqlmodel to be part of each migration under script.py.mako file
import sqlmodel

# use --autogenerate if we want to generate from sqlmodel metadata
alembic revision --autogenerate -m "Initial migration"
# run recent migration
alembic upgrade head - affect migrations
alembic downgrade head - reverse migrations
'''
