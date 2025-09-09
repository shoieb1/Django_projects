import sqlite3
from werkzeug.security import generate_password_hash

# Define database file path
DATABASE_FILE = 'users.db'

def create_database():
    try:
        # Connect to SQLite (or create the database if it doesn't exist)
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()

        # Create the users table if it doesn't already exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        print("Database and users table created successfully.")

        # Insert a sample user (username and hashed password)
        username = "test_user"
        password = "your_password"  # Replace with the password you want for the test user
        hashed_password = generate_password_hash(password)

        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            print(f"User '{username}' added successfully.")
        except sqlite3.IntegrityError:
            print(f"User '{username}' already exists in the database.")

        # Commit changes
        conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        # Ensure the connection is closed even if there was an error
        if conn:
            conn.close()
            print("Database connection closed.")

# Run the function to create the database and add a test user
if __name__ == "__main__":
    create_database()
