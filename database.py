import sqlite3
from encryption import encrypt_data, decrypt_data

def initialize_database():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            api_key TEXT
        )
    ''')
    conn.commit()
    conn.close()

def set_api_key(user_id, api_key):
    encrypted_key = encrypt_data(api_key)
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO users (user_id, api_key) VALUES (?, ?)', (user_id, encrypted_key))
    conn.commit()
    conn.close()

def get_api_key(user_id):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT api_key FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    if result and result[0]:
        return decrypt_data(result[0])
    return None
