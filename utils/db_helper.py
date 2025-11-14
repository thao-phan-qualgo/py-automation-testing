"""
Database helper utilities for PostgreSQL connections.

This module provides reusable functions for connecting to and querying
PostgreSQL databases in test automation scenarios.
"""

import os
import logging
from typing import Any, Dict, List, Optional, Tuple
from contextlib import contextmanager

try:
    import psycopg2
    from psycopg2 import pool
    from psycopg2.extras import RealDictCursor

    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    print("⚠️ psycopg2 not installed. Install with: pip install psycopg2-binary")

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class DatabaseHelper:
    """Helper class for PostgreSQL database operations."""

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """
        Initialize database helper with connection parameters.

        Args:
            host: Database host (defaults to env DB_HOST)
            port: Database port (defaults to env DB_PORT or 5432)
            database: Database name (defaults to env DB_NAME)
            username: Database username (defaults to env DB_USERNAME)
            password: Database password (defaults to env DB_PASSWORD)
        """
        if not PSYCOPG2_AVAILABLE:
            raise ImportError(
                "psycopg2 is required for database operations. "
                "Install with: pip install psycopg2-binary"
            )

        self.host = host or os.getenv("DB_HOST")
        self.port = port or int(os.getenv("DB_PORT", "5432"))
        self.database = database or os.getenv("DB_NAME")
        self.username = username or os.getenv("DB_USERNAME")
        self.password = password or os.getenv("DB_PASSWORD")

        # Validate required parameters
        if not all([self.host, self.database, self.username, self.password]):
            raise ValueError(
                "Missing required database connection parameters. "
                "Ensure DB_HOST, DB_NAME, DB_USERNAME, and DB_PASSWORD are set in .env"
            )

        self.connection_pool = None
        logger.info(f"Database helper initialized for {self.database}@{self.host}")

    def get_connection_string(self) -> str:
        """
        Get connection string for PostgreSQL.

        Returns:
            Connection string (with masked password for logging)
        """
        return (
            f"host={self.host} port={self.port} dbname={self.database} "
            f"user={self.username} password=***"
        )

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.

        Yields:
            psycopg2 connection object

        Example:
            with db_helper.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()
        """
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password,
            )
            logger.debug("Database connection established")
            yield conn
            conn.commit()
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
                logger.debug("Database connection closed")

    def execute_query(
        self, query: str, params: Optional[Tuple] = None, fetch: bool = True
    ) -> Optional[List[Tuple]]:
        """
        Execute a SQL query.

        Args:
            query: SQL query string
            params: Query parameters (for parameterized queries)
            fetch: Whether to fetch results (False for INSERT/UPDATE/DELETE)

        Returns:
            List of tuples (rows) if fetch=True, None otherwise

        Example:
            # SELECT query
            results = db_helper.execute_query("SELECT * FROM users WHERE id = %s", (1,))

            # INSERT query
            db_helper.execute_query(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                ("John Doe", "john@example.com"),
                fetch=False
            )
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                if fetch:
                    results = cursor.fetchall()
                    logger.debug(f"Query returned {len(results)} rows")
                    return results
                else:
                    logger.debug(f"Query affected {cursor.rowcount} rows")
                    return None
            finally:
                cursor.close()

    def execute_query_dict(
        self, query: str, params: Optional[Tuple] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return results as list of dictionaries.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            List of dictionaries (column_name: value)

        Example:
            results = db_helper.execute_query_dict("SELECT * FROM users")
            for row in results:
                print(row['name'], row['email'])
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                cursor.execute(query, params)
                results = cursor.fetchall()
                logger.debug(f"Query returned {len(results)} rows as dictionaries")
                return [dict(row) for row in results]
            finally:
                cursor.close()

    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Tuple]:
        """
        Execute a query and fetch a single row.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Single row as tuple, or None if no results

        Example:
            user = db_helper.fetch_one("SELECT * FROM users WHERE id = %s", (1,))
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                result = cursor.fetchone()
                logger.debug(f"Query returned {'1 row' if result else 'no rows'}")
                return result
            finally:
                cursor.close()

    def fetch_one_dict(
        self, query: str, params: Optional[Tuple] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Execute a query and fetch a single row as dictionary.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Single row as dictionary, or None if no results

        Example:
            user = db_helper.fetch_one_dict("SELECT * FROM users WHERE id = %s", (1,))
            print(user['name'])
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                cursor.execute(query, params)
                result = cursor.fetchone()
                logger.debug(f"Query returned {'1 row' if result else 'no rows'}")
                return dict(result) if result else None
            finally:
                cursor.close()

    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.

        Args:
            table_name: Name of the table to check

        Returns:
            True if table exists, False otherwise
        """
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """
        result = self.fetch_one(query, (table_name,))
        return result[0] if result else False

    def get_table_count(self, table_name: str) -> int:
        """
        Get the number of rows in a table.

        Args:
            table_name: Name of the table

        Returns:
            Number of rows in the table
        """
        query = f"SELECT COUNT(*) FROM {table_name};"
        result = self.fetch_one(query)
        return result[0] if result else 0

    def get_column_names(self, table_name: str) -> List[str]:
        """
        Get column names for a table.

        Args:
            table_name: Name of the table

        Returns:
            List of column names
        """
        query = """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND table_name = %s
            ORDER BY ordinal_position;
        """
        results = self.execute_query(query, (table_name,))
        return [row[0] for row in results] if results else []

    def test_connection(self) -> bool:
        """
        Test database connection.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()
                cursor.close()

                if result and result[0] == 1:
                    logger.info("✅ Database connection test successful")
                    return True
                else:
                    logger.error(
                        "❌ Database connection test failed: unexpected result"
                    )
                    return False
        except Exception as e:
            logger.error(f"❌ Database connection test failed: {e}")
            return False


# Convenience function for quick usage
def get_db_helper() -> DatabaseHelper:
    """
    Get a DatabaseHelper instance using environment variables.

    Returns:
        DatabaseHelper instance

    Example:
        db = get_db_helper()
        users = db.execute_query_dict("SELECT * FROM users")
    """
    return DatabaseHelper()


# Example usage
if __name__ == "__main__":
    # Example: Test connection
    db = get_db_helper()

    if db.test_connection():
        print("✅ Database connection successful!")

        # Example queries
        # results = db.execute_query_dict("SELECT * FROM users LIMIT 5")
        # print(f"Found {len(results)} users")
    else:
        print("❌ Database connection failed!")
