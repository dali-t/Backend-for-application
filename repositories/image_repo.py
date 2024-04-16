from repositories.db import get_pool
from psycopg.rows import dict_row  
from datetime import datetime, timedelta

def get_all_images_for_table():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT
                    i.image_id,
                    i.created_at,
                    u.email AS author_email
                FROM 
                    images i
                INNER JOIN users u ON i.author_id = u.user_id
            ''')
            return cursor.fetchall()

def get_image_by_id(image_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT
                    i.image_id,
                    i.caption,
                    i.image_link,
                    u.email AS author_email,
                    i.created_at
                FROM
                    images i
                INNER JOIN users u ON i.author_id = u.user_id
                WHERE i.image_id = %s
            ''', (image_id,))
            return cursor.fetchone()


def create_image(caption: str, image_link: str, author_email: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            # Fetch the user_id based on the author's email
            cursor.execute('SELECT user_id FROM users WHERE email = %s', (author_email,))
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"User with email '{author_email}' not found")
            user_id = result[0]

            # Check if the user has created a post within the last 24 hours
            cursor.execute('''
                SELECT MAX(created_at) AS last_post_timestamp
                FROM images
                WHERE author_id = %s
            ''', (user_id,))
            last_post_timestamp = cursor.fetchone()

            if last_post_timestamp:
                last_post_time = last_post_timestamp[0]
                if last_post_time + timedelta(days=1) > datetime.now():
                    raise ValueError("You can only create one post per day.")

            # Insert the new image with the retrieved user_id
            cursor.execute('''
                INSERT INTO images (caption, image_link, author_id)
                VALUES (%s, %s, %s)
                RETURNING image_id
            ''', (caption, image_link, user_id))
            image_id = cursor.fetchone()[0]

            # Update the last post timestamp in the analytics table
            cursor.execute('''
                INSERT INTO analytics (user_id, analytics_type, last_post_timestamp)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE
                SET last_post_timestamp = EXCLUDED.last_post_timestamp
            ''', (user_id, 'create_post', datetime.now()))

            return image_id