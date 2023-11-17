# - databaseName: string
# - tableName: string
# + Cart():
# + Cart(string databaseName, string tableName)
# + viewCart(string userID, string inventoryDatabase): void
# + addToCart(string userID, string ISBN): void
# + removeFromCart(string userID, string ISBN): void
# + checkOut(string userID): void
import sqlite3


class Cart:
    def __init__(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name
    
    def view_cart(self, user_id, inventory_database):
        pass

    def add_to_cart(self, user_id, isbn):
        pass

    def remove_from_cart(self, user_id, isbn):
        pass

    def check_out(self, user_id):
        pass


def create_cart_database(database_name, table_name):
    # Connect to db
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # SQL query
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES user_info(user_id),
        FOREIGN KEY(item_id) REFERENCES inventory(item_id)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()