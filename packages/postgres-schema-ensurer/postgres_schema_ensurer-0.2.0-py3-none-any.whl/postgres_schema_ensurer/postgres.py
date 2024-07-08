from database_schema_ensurer import Database, MigrationRecord
from typing import Optional
import psycopg2
import psycopg2.sql


class Postgres(Database):
    def __init__(self, table_name: str, psycopg2_connection) -> None:
        self._table_name = psycopg2.sql.Identifier(table_name)
        self._connection = psycopg2_connection

    def get_max_migration_version(self) -> Optional[int]:
        with self._connection.cursor() as cursor:
            cursor = self._connection.cursor()
            try:
                cursor.execute(f"SELECT version FROM {self._table_name} ORDER BY version DESC LIMIT 1")
            except:
                return None
            row = cursor.fetchone()
            return row[0] if row else None

    def get_migration(self, version: int) -> MigrationRecord:
        with self._connection.cursor() as cursor:
            cursor.execute(f"SELECT down_sql, version FROM {self._table_name} WHERE version = %s", [version])
            row = cursor.fetchone()
            return MigrationRecord(
                down_sql=row[0],
                version=row[1],
            )

    def add_migration(self, migration: MigrationRecord):
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self._table_name} (down_sql, version) VALUES (%s, %s)",
                [migration.down_sql, migration.version]
            )

    def delete_migration(self, version: int):
        with self._connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {self._table_name} WHERE version = %s", [version])

    def execute_sql(self, sql: str):
        with self._connection.cursor() as cursor:
            cursor.execute(sql)
