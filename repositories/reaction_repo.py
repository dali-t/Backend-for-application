from repositories.db import get_pool
from psycopg.rows import dict_row  
from datetime import datetime, timedelta

def create_reaction(image_id, user_id, reaction_type):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                INSERT INTO reactions (image_id, user_id, reaction_type)
                VALUES (%s, %s, %s)
            ''', (image_id, user_id, reaction_type))

def update_reaction(reaction_id, reaction_type):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                UPDATE reactions
                SET reaction_type = %s
                WHERE reaction_id = %s
            ''', (reaction_type, reaction_id))

def get_reaction_counts(image_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT
                    COUNT(*) FILTER (WHERE reaction_type = 'like') AS likes,
                    COUNT(*) FILTER (WHERE reaction_type = 'dislike') AS dislikes,
                    COUNT(*) FILTER (WHERE reaction_type = 'laugh') AS laughs,
                    COUNT(*) FILTER (WHERE reaction_type = 'shock') AS shocks,
                    COUNT(*) FILTER (WHERE reaction_type = 'cry') AS cries,
                    COUNT(*) FILTER (WHERE reaction_type = 'heart') AS hearts
                FROM reactions
                WHERE image_id = %s
            ''', (image_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'likes': row[0] or 0,
                    'dislikes': row[1] or 0,
                    'laughs': row[2] or 0,
                    'shocks': row[3] or 0,
                    'cries': row[4] or 0,
                    'hearts': row[5] or 0
                }
            else:
                return {
                    'likes': 0,
                    'dislikes': 0,
                    'laughs': 0,
                    'shocks': 0,
                    'cries': 0,
                    'hearts': 0
                }