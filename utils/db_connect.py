import psycopg2
from config.config import host, user, password, db_name


try:
    connection = None
    def connect():
        global connection
        if connection != None: return False

        # подключение к БД
        connection = psycopg2.connect(host=host, 
                                    user=user, 
                                    password=password, 
                                    database=db_name,
                                    )
        
        connection.autocommit = True
    
        # создать таблицу users если её еще нет
        with connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                            id SERIAL PRIMARY KEY,
                            chat_id	BIGINT UNIQUE NOT NULL,
                            language TEXT NOT NULL,
                            processing INTEGER DEFAULT 0
                            );''')
            print('[INFO] Table "users" works succesfuly') 

            cursor.execute('''CREATE TABLE IF NOT EXISTS preferences(
                            id SERIAL PRIMARY KEY,
                            chat_id	BIGINT UNIQUE NOT NULL,
                            chosen_url TEXT DEFAULT '',
                            chosen_mode TEXT DEFAULT ''
                            );''')
            print('[INFO] Table "preferences" works succesfuly') 
            
        return True
    
    # запросы к таблице users
    def add_user(chat_id, language):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''INSERT INTO users (chat_id, language)
            VALUES ('{chat_id}', '{language}') ON CONFLICT DO NOTHING;''')

            cursor.execute(f'''INSERT INTO preferences (chat_id)
            VALUES ('{chat_id}') ON CONFLICT DO NOTHING;''')
            
            print(f'[INFO] Values for {chat_id} ({language}) succesfuly added')
    
    def is_exist(chat_id):
        connect()
        with connection.cursor() as cursor:

            cursor.execute(f'''SELECT chat_id FROM users WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            
            return cursor.fetchone() is not None
    
    def get_language(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT language FROM users WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Getting *{chat_id}* language')
            return cursor.fetchone()[0]
        
    def set_language(chat_id, language):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''UPDATE users SET language = '{language}' WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Setting *{chat_id}* language ({language})')
    
    def set_url(chat_id, url):
        connect()
        with connection.cursor() as cursor:
            sql = "UPDATE users SET chosen_url = %s WHERE CAST(chat_id AS BIGINT) = %s;"
            cursor.execute(sql, (url, chat_id))
            connection.commit()
            print(f'[INFO] Setting *{chat_id}* chosen_url ({url})')

    def set_chosen_mode(chat_id, mode):
        connect()
        with connection.cursor() as cursor:
            sql = "UPDATE preferences SET chosen_mode = %s WHERE CAST(chat_id AS BIGINT) = %s;"
            cursor.execute(sql, (mode, chat_id))
            connection.commit()
            print(f'[INFO] Setting *{chat_id}* chosen_mode ({mode})')
    
    def get_chosen_mode(chat_id):
        connect()
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT chosen_mode FROM preferences WHERE CAST(chat_id AS BIGINT) = {chat_id};''')
            print(f'[INFO] Getting *{chat_id}* chosen_mode')
            return cursor.fetchone()[0]  
        

except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostreSQL connection closed')
    