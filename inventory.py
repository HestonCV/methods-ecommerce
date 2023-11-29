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

    def search_Inventory(self):
        print("What category would you like to search by?\n1. Titles\n2. Authors\n3. Genres")
        selection = int(input())

        search_fields = ['TITLE', 'AUTHOR', 'GENRE']
        if 1 <= selection <= 3:
            search_field = search_fields[selection - 1]
        else:
            print("Invalid selection.")
            return

        print("Search for:")
        search_value = input()

        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE {search_field} LIKE ?", (search_value,))
        result = self.cursor.fetchall()

        if result:
            titles = [book[0] for book in result]
            authors = [book[1] for book in result]
            genres = [book[2] for book in result]
            pages = [book[3] for book in result]
            release_dates = [book[4] for book in result]
            stock = [book[5] for book in result]

            print(f"Results for Books with the {search_field.lower()} {search_value}:\n")
            print(titles, ", ", authors, ", ", genres, ", ", pages, ", ", release_dates, ", ", stock, "\n")
        else:
            print(f"No results found for {search_field.lower()} {search_value}.\n")
        
        return {
        'stock': stock,
        'titles': titles,
        'authors': authors,
        'genres': genres,
        'pages': pages,
        'release_dates': release_dates
        }


    def decrease_Stock(self, ISBN, cart_isbns, cart_quantity):
        self.cursor.execute(f'SELECT Stock FROM {self.table_name} WHERE Isbn = ?', (cart_isbns,))
        old_stock = self.cursor.fetchone()[0]

        new_stock = old_stock - cart_quantity

        self.cursor.execute(f'UPDATE {self.table_name} SET Stock = ? WHERE ISBN = ?', (new_stock, cart_isbns))
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
