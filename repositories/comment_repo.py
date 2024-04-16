from repositories.db import get_pool
from psycopg.rows import dict_row  
from datetime import datetime, timedelta

def create_comment(image_id: int, user_id: int, comment_text: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                INSERT INTO comments (image_id, user_id, comment_text)
                VALUES (%s, %s, %s)
            ''', (image_id, user_id, comment_text))

def get_comments_for_image(image_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT c.comment_id, c.comment_text, c.created_at, u.email AS author_email
                FROM comments c
                INNER JOIN users u ON c.user_id = u.user_id
                WHERE c.image_id = %s
                ORDER BY c.created_at DESC
            ''', (image_id,))
            return cursor.fetchall()