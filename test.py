import sqlite3

conn = sqlite3.connect('magaz.db')
cursor = conn.cursor()
try:
    cursor.execute("""SELECT * FROM user """)
    print(cursor.fetchall())
except:
    print('mau')
