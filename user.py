import sqlite3

# - databaseName: string
# - tableName: string
# - loggedIn: bool
# - userID: string
# + User()
# + User(string databaseName, string tableName)
# + login(): bool
# + logout(): bool
# + viewAccountInformation(): void
# + createAccount(): void
# + getLoggedIn(): bool
# + getUserID(): string

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

        # username = input("Enter your username: ")
        # password = input("Enter your password: ")

        # Implement SQL query to check if the username and password match
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE username=? AND password=?", (username, password))
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

        # Implement SQL query to fetch and display the user's account information
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE user_id=?", (self.user_id,))
        user = self.cursor.fetchone()
        print("Account Information:")
        print(f"User ID: {user[0]}")
        print(f"Username: {user[1]}")
        print(f"Email: {user[3]}")
        #new stuff
        print(f"FirstName: {user[4]}")
        print(f"LastName: {user[5]}")
        print(f"Address: {user[6]}")
        print(f"City: {user[7]}")
        print(f"State: {user[8]}")
        print(f"Zip: {user[9]}")
        print(f"Payment: {user[10]}")

    def create_account(self):
        if self.logged_in:
            print("You are already logged in. Please log out before creating a new account.")
            return

        username = input("Enter a new username: ")
        password = input("Enter a new password: ")
        email = input("Enter your email address: ")
        #new stuff
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        address = input("Enter your address: ")
        city = input("Enter your city: ")
        state = input("Enter your state: ")
        zip_code = input("Enter your ZIP code: ")
        payment = input("Enter your payment information: ")

        # Implement SQL query to insert a new user into the database
        self.cursor.execute("INSERT INTO {} (username, password, email, first_name, last_name, address, city, state, zip, payment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(self.table_name),
                            (username, password, email, first_name, last_name, address, city, state, zip_code, payment))
        self.conn.commit()
        print("Account creation successful.")

    def getLoggedIn(self):
        return self.logged_in

    def getUserID(self):
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
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        zip TEXT NOT NULL,
        payment TEXT NOT NULL
    );
    """

    cursor.execute(create_table_query)

    conn.commit()
    conn.close()
