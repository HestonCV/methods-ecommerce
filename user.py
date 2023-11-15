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
    def __init__(self, databaseName, tableName):
        self.databaseName = databaseName
        self.tableName = tableName
        self.loggedIn = False
        self.userID = ""
        self.conn = sqlite3.connect(self.databaseName)
        self.cursor = self.conn.cursor()

    def login(self):
        if self.loggedIn:
            print("You are already logged in.")
            return False

        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Implement SQL query to check if the username and password match
        self.cursor.execute(f"SELECT * FROM {self.tableName} WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()
        
        if user:
            self.loggedIn = True
            self.userID = user[0]
            print(f"Login successful. Welcome, {username}.")
            return True
        else:
            print("Login failed. Incorrect username or password.")
            return False

    def logout(self):
        if not self.loggedIn:
            print("You are not logged in.")
            return False

        self.loggedIn = False
        self.userID = ""
        print("Logout successful.")
        return True

    def viewAccountInformation(self):
        if not self.loggedIn:
            print("You need to log in to view account information.")
            return

        # Implement SQL query to fetch and display the user's account information
        self.cursor.execute(f"SELECT * FROM {self.tableName} WHERE user_id=?", (self.userID,))
        user = self.cursor.fetchone()
        print("Account Information:")
        print(f"User ID: {user[0]}")
        print(f"Username: {user[1]}")
        print(f"Email: {user[3]}")

    def createAccount(self):
        if self.loggedIn:
            print("You are already logged in. Please log out before creating a new account.")
            return

        username = input("Enter a new username: ")
        password = input("Enter a new password: ")
        email = input("Enter your email address: ")

        # Implement SQL query to insert a new user into the database
        self.cursor.execute("INSERT INTO {} (username, password, email) VALUES (?, ?, ?)".format(self.tableName),
                            (username, password, email))
        self.conn.commit()
        print("Account creation successful.")

    def getLoggedIn(self):
        return self.loggedIn

    def getUserID(self):
        return self.userID

    def close_connection(self):
        self.conn.close()

# Function to create the user database
def create_user_database():
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_info (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """

    cursor.execute(create_table_query)

    # Insert a default user at the start
    default_user_query = """
    INSERT INTO user_info (username, password, email) VALUES (?, ?, ?)
    """

    # You can customize the default username, password, and email
    default_user_values = ("default", "password", "default@example.com")

    cursor.execute(default_user_query, default_user_values)

    conn.commit()
    conn.close()

# Example usage:
# Create the user database if it doesn't exist
create_user_database()

# Now you can instantiate the User class and use its methods
user = User("user_database.db", "user_info")
user.login()
user.viewAccountInformation()
# ... (other interactions with the User class)

# Close the connection when done
user.close_connection()