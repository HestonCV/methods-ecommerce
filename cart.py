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
    
    def view_cart(self, user_id, inventory_table_name):
        '''
            Returns all books in the logged in User’s cart.
            Please note: this cooperates with the inventory database to display all the
            correct information on the inventory items

            ** Does not display the books. It returns the information for the UI/Menu
            to display. **
        '''
        query = "SELECT isbn, quantity FROM {} WHERE user_id=?".format(self.table_name)
        self.cursor.execute(query, (user_id,))
        # Get each item's quantity and isbn
        items_in_cart = self.cursor.fetchall()

        # Initialize empty to false
        empty = False

        # Unpack isbns and quantites from items in cart
        isbns = [item[0] for item in items_in_cart]
        quantities = [item[1] for item in items_in_cart]

        if isbns:
            # Join isbns for use in query
            placeholders = ', '.join('?' for _ in isbns)

            # Fetch book details from the inventory for each isbn
            query = "SELECT * FROM {} WHERE isbn IN ({})".format(inventory_table_name, placeholders)
            self.cursor.execute(query, isbns)
            books = self.cursor.fetchall()

            titles = [book[1] for book in books]
            authors = [book[2] for book in books]
            genres = [book[3] for book in books]
            pages = [book[4] for book in books]
            release_dates = [book[5] for book in books]

        else:
            empty = True
            titles, authors, genres, pages, release_dates = [], [], [], [], []
        
        return {
            'empty': empty,
            'isbns': isbns,
            'quantities': quantities,
            'titles': titles,
            'authors': authors,
            'genres': genres,
            'pages': pages,
            'release_dates': release_dates
        }


    def add_to_cart(self, user_id, isbn): 
        '''
            Once user selects a book, this ISBN is used to add an item to
            the appropriate cart
        '''
        # Get item with matching isbn and stock > 0 from inventory
        self.cursor.execute("SELECT stock FROM {} WHERE isbn=? AND stock>?".format('inventory'), (isbn, 0))
        
        item_in_inventory = self.cursor.fetchone()

        if item_in_inventory and item_in_inventory[0] > 0:
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
            Once user selects a book to remove, this ISBN is used to
            remove an item from the user’s cart

            ** Because quantity is not specified, this method decrements quantity
            of the item. If the new quantity is 0, it deletes the item from the
            cart. **
        '''
        # Get item from cart
        self.cursor.execute("SELECT quantity FROM {} WHERE isbn=? AND user_id=?".format(self.table_name), (isbn, user_id))
        item_in_cart = self.cursor.fetchone()

        if item_in_cart:
            new_quantity = item_in_cart[0] - 1

            if new_quantity > 0:
                update_query = "UPDATE {} SET quantity=? WHERE user_id=? AND isbn=?".format(self.table_name)
                self.cursor.execute(update_query, (new_quantity, user_id, isbn))
            else:
                # Delete entry from cart
                delete_query = "DELETE FROM {} WHERE user_id=? AND isbn=?".format(self.table_name)
                self.cursor.execute(delete_query, (user_id, isbn))
            
            self.conn.commit()
            return True
        else:
            return False

    def check_out(self, user_id):
        '''
            this removes all their cart items. It also
            calls the Inventory class function to decrease the stock of the books by the correct
            amount the user bought (prior to removing them from the cart)
        '''
        query = 'SELECT isbn, quantity FROM {} WHERE user_id=? AND quantity>0'.format(self.table_name)
        self.cursor.execute(query, user_id)

        items = self.cursor.fetchall()

        if items:
            for item in items:
                isbn = item[0]
                quantity = item[1]
                #inventory.decrease_stock(isbn, quantity)
                delete_query = 'DELETE FROM {} WHERE isbn=? and user_id=?'.format(self.table_name)
                self.cursor.execute(delete_query, isbn, user_id)
                self.conn.commit()

                return True
        else: 
            return False




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