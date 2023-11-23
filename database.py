import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('wallet_app.db')
cursor = conn.cursor()
# Create login table with default values
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS login (
#         gmail TEXT,
#         username TEXT,
#         password TEXT,
#         phone TEXT PRIMARY KEY,
#         adhaar TEXT,
#         pan TEXT,
#         address TEXT,
#         usertype TEXT DEFAULT 'customer',
#         confirm BLOB DEFAULT 1
#     )
# ''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")

# Sample data
# insert_data = ('Lakshmihatti@gmail.com', 'lux', '1234', '8951195826',
#                '3344667788', 'azcph102eh', 'Dharwad', 'customer', b'true')
#
# # Insert data into the login table
# cursor.execute('''
#     INSERT INTO login (gmail, username, password, phone, adhaar, pan, address, usertype, confirm)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
# ''', insert_data)
# # deleting all values/records
# cursor.execute('''
#     DELETE FROM login
#     WHERE usertype = 'customer'
# ''')
# Commit the changes and close the connection
conn.commit()
cursor.execute('SELECT * FROM login')
records = cursor.fetchall()
for record in records:
    print(record)
conn.close()

# print("Database and table created successfully.")
