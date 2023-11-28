import sqlite3

class User:
    def __init__(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name
        self.logged_in = False
        self.user_id = ""
        self.conn = sqlite3.connect(self.database_name)
        self.cursor = self.conn.cursor()

    def login(self, username, password):
        if self.logged_in:
            print("You are already logged in.")
            return False

        self.cursor.execute("SELECT * FROM {} WHERE username=? AND password=?".format(self.table_name), (username, password))
        user = self.cursor.fetchone()

        if user:
            self.logged_in = True
            self.user_id = user[0]
            print(f"|----- Login successful. Welcome, {username}.")
            return True
        else:
            print("|----- Login failed. Incorrect username or password.")
            return False

    def logout(self):
        if not self.logged_in:
            print("|----- You are not logged in.")
            return False

        self.logged_in = False
        self.user_id = ""
        print("|----- Logout successful.")
        return True

    def view_account_information(self):
        if not self.logged_in:
            print("You need to log in to view account information.")
            return

        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE user_id=?", (self.user_id,))
        user = self.cursor.fetchone()
        print("Account Information:")
        print(f"User ID: {user[0]}")
        print(f"Username: {user[1]}")
        print(f"Email: {user[3]}")
        print(f"FirstName: {user[4]}")
        print(f"LastName: {user[5]}")
        print(f"Address: {user[6]}")
        print(f"City: {user[7]}")
        print(f"State: {user[8]}")
        print(f"Zip: {user[9]}")
        print(f"Payment: {user[10]}")
        # Add other fields as needed

    def create_account(self):
        if self.logged_in:
            print("You are already logged in. Please log out before creating a new account.")
            return

        username = input("Enter a new username: ")
        password = input("Enter a new password: ")
        email = input("Enter your email address: ")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        address = input("Enter your address: ")
        city = input("Enter your city: ")
        state = input("Enter your state: ")
        zip_code = input("Enter your ZIP code: ")
        payment = input("Enter your payment information: ")
        # Add other fields as needed

        self.cursor.execute(
            "INSERT INTO {} (username, password, email, first_name, last_name, address, city, state, zip, payment) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(self.table_name),
            (username, password, email, first_name, last_name, address, city, state, zip_code, payment)
        )
        self.conn.commit()
        print("Account creation successful.")

    def get_logged_in(self):
        return self.logged_in

    def get_user_id(self):
        return self.user_id

    def close_connection(self):
        self.conn.close()

# Function to create the user database
def create_user_database(database_name, table_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        zip TEXT,
        payment TEXT
    );
    """

    cursor.execute(create_table_query)

    conn.commit()
    conn.close()

# Example usage:
# create_user_database("users.db", "user_table")
# user = User("users.db", "user_table")
# user.create_account()
# user.login("username", "password")
# user.view_account_information()
# user.logout()
# user.close_connection()
