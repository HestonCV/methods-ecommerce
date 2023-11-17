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
        self.conn = sqlite3.connect(self.database_name)
        self.cursor = self.conn.cursor()
    
    # def view_cart(self, user_id, inventory_database):
    #     # ISBN *
    #     # Title
    #     # Author
    #     # Genre
    #     # Pages
    #     # ReleaseDate
    #     # Stock
    #     query = "SELECT isbn, quantity FROM {} WHERE user_id=?".format(self.table_name)
    #     self.cursor.execute(query, (user_id,))
    #     # Get each item's quantity and isbn
    #     items_in_cart = self.cursor.fetchall()

    #     isbns = [item[0] for item in items_in_cart]
    #     quantities = [item[1] for item in items_in_cart]

    #     isbn_tuple = tuple(isbns)

    #     if len(isbn_tuple) == 1:
    #         query = "SELECT * FROM {} WHERE isbn IN {}".format('inventory', isbn_tuple,)


    #     query = "SELECT * FROM {} WHERE isbn IN {}".format('inventory', isbn_tuple)
    #     self.cursor.execute(query, (isbn, ))
    #     books = self.cursor.fetchall()

    #     titles = [book[1] for book in books]
    #     authors = [book[2] for book in books]
    #     genres = [book[3] for book in books]
    #     pages = [book[4] for book in books]
    #     release_date = [book[4] for book in books]

    #     for isbn in isbns:

    #      titles.append


    #     query = "SELECT * FROM {} WHERE isbn=?".format('inventory')
    #     self.cursor.execute(query, (,))


    #     book = []



    def add_to_cart(self, user_id, isbn): 

        # Get item with matching isbn and stock > 0 from inventory
        self.cursor.execute("SELECT stock FROM {} WHERE isbn=? AND stock>?".format('inventory'), (isbn, 0))
        
        item_in_inventory = self.cursor.fetchone()

        if item_in_inventory:
            # Check if item is already in the cart
            self.cursor.execute("SELECT quantity FROM {} WHERE isbn=? AND user_id=?".format(self.table_name), (isbn, user_id))
            item_in_cart = self.cursor.fetchone()

            if item_in_cart:
                # Calculate new quantity
                new_quantity = item_in_cart[0] + 1

                # Update item quantity in cart
                update_query = "UPDATE {} SET quantity=? WHERE user_id=? AND isbn=?".format(self.table_name)
                self.cursor.execute(update_query, (new_quantity, user_id, isbn))
            else: 
                # Create new entry in cart with quantity of 1
                insert_query = "INSERT INTO {} (user_id, isbn, quantity) VALUES (?, ?, ?)".format(self.table_name)
                self.cursor.execute(insert_query, (user_id, isbn, 1))
            
            self.conn.commit()
            return True
        else:
            return False

    def remove_from_cart(self, user_id, isbn):
        '''
            Because quantity is not specified, this method removes
            the item from the db regardless of quantity
        '''

        # Get item from cart
        self.cursor.execute("SELECT quantity FROM {} WHERE isbn=? AND user_id=?".format(self.table_name), (isbn, user_id))
        item_in_cart = self.cursor.fetchone()

        if item_in_cart:
            
            # Delete entry from cart
            delete_query = "DELETE FROM {} WHERE user_id=? AND isbn=?".format(self.table_name)
            self.execute(delete_query, (user_id, isbn))
            self.conn.commit()
            return True
        else:
            return False

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
        isbn INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES user(user_id),
        FOREIGN KEY(isbn) REFERENCES inventory(isbn)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()