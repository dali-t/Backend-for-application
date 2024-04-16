from repositories.db import get_pool
from psycopg.rows import dict_row

def get_all_users():
    """Retrieve all users from the database."""
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('SELECT user_id, email FROM users')
            return cursor.fetchall()

def get_user_by_id(user_id: int):
    """Retrieve a user by their ID from the database."""
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('SELECT user_id, email, first_name, last_name FROM users WHERE user_id = %s', (user_id,))
            return cursor.fetchone()

def create_user(email: str, first_name: str, last_name: str, password: str):
    """Create a new user in the database."""
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('INSERT INTO users (email, first_name, last_name, password) VALUES (%s, %s, %s, %s) RETURNING user_id',
                           (email, first_name, last_name, password))
            res = cursor.fetchone()
            if not res:
                raise Exception('Failed to create user')
            return res[0]

# Add more user-related functions as needed, such as updating user data or deleting users