from datetime import datetime
from db.db import DB
from model.token import Token


class TokenRepo:
    def __init__(self):
        self.db = DB()
    

    def get_token_by_userId(self):
         with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM token")
                token_records = cursor.fetchall()
                for row in token_records:
                   print(row)
    
    def insert_token(self, token: Token):
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                sql = """INSERT INTO login.tokens
                        (access_token, refresh_token, user_id, expired_access_token, expired_refresh_token, created_at)
                        VALUES(%s, %s, %s, %s, %s, %s);"""
                cursor.execute(sql, (token.access_token, token.refresh_token, token.user_id, token.expired_access_token, token.expired_refresh_token, token.created_at))
                conn.commit()
                print("Token inserted successfully.")

    def count_user_token_current_date(self, user_id:str):
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                sql ="""select count(1)
                       from login.tokens t
                       where t.user_id = %s and t.created_at::date = %s::date;
                    """
                cursor.execute(sql, (user_id, datetime.now()))
                token_count = cursor.fetchone()
                return token_count[0]
    
    