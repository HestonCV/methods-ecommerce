# - databaseName: string
# - tableName: string
# + Inventory()
# + Inventory(string databaseName, string tableName)
# + viewInventory(): void
# + searchInventory(): void
# + editStock(string ISBN): void
import sqlite3

class Inventory:
    def __init__(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name
        self.conn = sqlite3.connect(self.database_name)
        self.cursor = self.conn.cursor()

    def view_inventory(self):
        self.cursor.execute(f'SELECT * FROM {self.table_name}')
        items_in_inventory = self.cursor.fetchall()

        if items_in_inventory:

            titles = [book[0] for book in items_in_inventory]
            authors = [book[1] for book in items_in_inventory]
            genres = [book[2] for book in items_in_inventory]
            pages = [book[3] for book in items_in_inventory]
            release_dates = [book[4] for book in items_in_inventory]
            stock = [book[5] for book in items_in_inventory]
            isbns = [book[6] for book in items_in_inventory]

            return {
                'empty': len(titles) == 0,
                'titles': titles,
                'authors': authors,
                'genres': genres,
                'pages': pages,
                'release_dates': release_dates,
                'stock': stock,
                'isbns': isbns
            }

    def search_inventory(self, title):

        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE TITLE LIKE ?", (title,))
        book = self.cursor.fetchone()

        if book:
            return {
                'title': book[0],
                'author': book[1],
                'genre': book[2],
                'page': book[3],
                'release_date': book[4],
                'stock': book[5],
                'isbn': book[6],
            }
        
        else: 
            return False
        

    def decrease_stock(self, cart_isbns, cart_quantities):
        
        if len(cart_isbns) != len(cart_quantities):
            return False

        for isbn, quantity in zip(cart_isbns, cart_quantities):
            # Fetch the current stock for each ISBN
            self.cursor.execute(f'SELECT stock FROM {self.table_name} WHERE isbn = ?', (isbn,))
            result = self.cursor.fetchone()
            if result is None:
                return False
            
            old_stock = result[0]

            # Calculate new stock
            new_stock = old_stock - quantity

            if new_stock < 0:
                return False

            self.cursor.execute(f'UPDATE {self.table_name} SET Stock = ? WHERE ISBN = ?', (new_stock, isbn))

        self.conn.commit()


def create_inventory_database(database_name, table_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
        Title TEXT PRIMARY KEY,
        Author TEXT,
        Genre TEXT NOT NULL,
        Pages INTEGER NOT NULL,
        Release_date TEXT,
        Stock INT NOT NULL,
        Isbn INT NOT NULL
        );
        """

    cursor.execute(create_table_query)
    conn.commit()
    conn.close()
