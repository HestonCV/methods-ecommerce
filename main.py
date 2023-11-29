from cart import Cart, create_cart_database
from user import User, create_user_database
from inventory import Inventory, create_inventory_database
# Before Login:            # After Login (Main Menu):
# ● Login                  # ● Logout
# ● Create Account         # ● View Account Information
# ● Logout                 # ● Inventory Information
                           # ● Cart Information

# After Login (Cart Info)  # After Login (Inventory Info)
# ● Go Back                # ● Go Back
# ● View Cart              # ● View Inventory
# ● Add Items to Cart      # ● Search Inventory
# ● Remove an Item from Cart
# ● Check Out


class Menu:
    def __init__(self, user, cart, inventory): 
        self.user = user
        self.cart = cart
        self.inventory = inventory
        self.nav_stack = ['initial_page']
        self.render_active_page()
    
    def back(self):
        # Remove page from top of stack and render the new active page
        self.nav_stack.pop()
        self.render_active_page()
    
    def forward(self, page):
        # Add page to top of stack and render the new active page
        self.nav_stack.append(page)
        self.render_active_page()
    
    def render_page_header(self, header_message=''):
        
        if header_message:
            header_message = '- ' + header_message

        print(f'\nCongo {header_message}')
        print('|-------------------------')

        if self.nav_stack[-1] == 'initial_page':
            print('|(X/x) -> Quit')
            return
        
        if self.nav_stack[-1] == 'main_menu':
            print('|(B/b) -> Logout')
            return
        
        if len(self.nav_stack) > 1:
            print('|(B/b) -> Back')
            return
        
    
    def render_active_page(self):
        # Define pages
        pages = {
            'initial_page': self.initial_page,
            'login': self.login_page,
            'register': self.register_page,
            'main_menu': self.main_menu_page,
            'account_info': self.account_info_page,
            'for_sale': self.for_sale_page,
            'cart': self.cart_page,
            'add_to_cart': self.add_to_cart_page,
            'remove_from_cart': self.remove_from_cart_page,
        }
        print('\n\n----------------------------------------\n')
        # Render page from top of stack
        active_page = self.nav_stack[-1]
        pages[active_page]()

    def display_inventory(self):
        items = self.inventory.view_inventory()

        if items['empty']:
            print('|')
            print('|-- Inventory Is Empty.')
        
        else:
            items_in_inventory = len(items['titles'])

            print('|-- Items In Inventory:', items_in_inventory)
            print('|')
            for i in range(items_in_inventory):
                print(f'|-- | Stock: {items["stock"][i]} | ISBN: {items["isbns"][i]} | Title: {items["titles"][i]} | Author: {items["authors"][i]} | Genre: {items["genres"][i]} | Pages: {items["pages"][i]} |  Release Date: {items["release_dates"][i]} |')
        print('|')
        
        return
    
    def display_cart(self):
        items = self.cart.view_cart(self.user.getUserID(), inventory.table_name)
        
        if items['empty']:
            print('|')
            print('|-- Your Cart Is Empty.')
        
        else:
            items_in_cart = sum(items['quantities'])

            print('|-- Items In Cart:', items_in_cart)
            print('|')
            for i in range(len(items['titles'])):
                print(f'|-- | Qty: {items["quantities"][i]} | ISBN: {items["isbns"][i]} | Title: {items["titles"][i]} | Author: {items["authors"][i]} | Genre: {items["genres"][i]} | Pages: {items["pages"][i]} |  Release Date: {items["release_dates"][i]} |')
        print('|')
        
        return
    
    def initial_page(self):
        
        # Process input from user
        def process_selection():

            while True:
                selection = input('|- Enter your selection: ')
                selection = selection.strip().lower()
                
                # If register page was selected
                if selection == '1':
                    self.forward('login')
                    return
                # if login page was selected
                elif selection == '2': 
                    self.forward('register')
                    return
                elif selection == 'x':
                    return
                else:
                    print('|----- Invalid Selection.')

        # Render Initial Page UI
        self.render_page_header(header_message="Welcome")
        print('|----- 1. Login')
        print('|----- 2. Register')
        process_selection()
        
    def login_page(self):
        def enter_credentials(credential_type):
            while True:
                credential = input(f'|- Enter your {credential_type}: ').strip()

                # If user chooses back
                if credential.lower() == 'b':
                    self.back()
                    return None

                return credential

        def attempt_login():
            username = enter_credentials('username')
            if not username:
                return False

            password = enter_credentials('password')
            if not password:
                return False

            return self.user.login(username, password)

        # Render Login UI
        self.render_page_header(header_message='Login')

        while not self.user.logged_in:
            if attempt_login():
                break

        self.forward('main_menu')
    
    def register_page(self):
        self.render_page_header(header_message='Register')
        self.user.create_account()
        self.back()

    def main_menu_page(self):

        def process_selection():
            # Get selection
            while True:
                selection = input('|- Enter your selection: ')
                selection = selection.strip().lower()

                # If register page was selected
                if selection == '1':
                    self.forward('account_info')
                    return
                # if login page was selected
                elif selection == '2': 
                    self.forward('for_sale')
                    return
                elif selection == '3': 
                    self.forward('cart')
                    return
                elif selection == 'b':
                    if user.logout():
                        self.nav_stack = ['initial_page']
                        self.render_active_page()
                    return
                else:
                    print('|----- Invalid Selection.')

        # Render Main Menu UI
        self.render_page_header(header_message="Main Menu")
        print('|----- 1. Account Info')
        print('|----- 2. For Sale')
        print('|----- 3. Your Cart')
        process_selection()
    
    def account_info_page(self):
        def display_user_information():
            user_info = self.user.view_account_information()
            
            print('|')
            if user_info:
                print(f"|- User ID: {user_info['user_id']}")
                print(f"|- Username: {user_info['username']}")
                print(f"|- Email: {user_info['email']}")
                print(f"|- Name: {user_info['first_name']} {user_info['last_name']}")
                print(f"|- Address: {user_info['address']}")
                print(f"|- City: {user_info['city']}")
                print(f"|- State: {user_info['state']}")
                print(f"|- Zip: {user_info['zip']}")
                print(f"|- Payment: {user_info['payment']}")
                
            else:
                print('|- Database Error.')
            
            print('|')

        def process_selection():
            # Get selection
            while True:
                selection = input('|- Enter your selection: ')
                selection = selection.strip().lower()

                if selection == 'b':
                    self.back()
                    return
                else:
                    print('|----- Invalid Selection.')

        self.render_page_header(header_message='Account Information')
        display_user_information()
        process_selection()
    
    def for_sale_page(self):
        
        def process_selection():
            # Get selection
            while True:
                selection = input('|- Enter your selection: ')
                selection = selection.strip().lower()
                # If register page was selected
                if selection == '1': 
                    self.forward('add_to_cart')
                    return
                elif selection == '2': 
                    self.forward('search_inventory')
                    return
                elif selection == 'b':
                    self.back()
                    return
                else:
                    print('|----- Invalid Selection.')

        self.render_page_header(header_message='Inventory')
        self.display_inventory()
        print('|----- 1. Add Item To Cart')
        print('|----- 2. Search Inventory')
        process_selection()
    
    # Cart Pages Start
    def cart_page(self):

        def process_selection():
            # Get selection
            while True:
                selection = input('|- Enter your selection: ')
                # If register page was selected
                if selection == '1': 
                    self.forward('add_to_cart')
                    return
                elif selection == '2': 
                    self.forward('remove_from_cart')
                    return
                elif selection == '3':
                    self.forward('check_out')
                    return
                elif selection == 'b':
                    self.back()
                    return
                else:
                    print('|----- Invalid Selection.')

        self.render_page_header(header_message="Cart")
        self.display_cart()
        print('|----- 1. Add Item To Cart')
        print('|----- 2. Remove Item From Cart')
        print('|----- 3. Check Out')
        process_selection()

    def add_to_cart_page(self):
        def process_selection():
            # Get selection
            while True:
                selection = input('|- Enter An ISBN To Add: ')\
                
                # If user wants to go back
                if selection == 'b':
                    self.back()
                    return
                
                # Add item to cart
                success = self.cart.add_to_cart(self.user.user_id, selection)
                if success:
                    print('|----- Item Added To Cart.')
                else:
                    print('|----- Invalid Selection.')

        self.render_page_header(header_message='Add To Cart')
        self.display_inventory()
        process_selection()
    
    def remove_from_cart_page(self):
        def process_selection():
            # Get selection
            while True:
                selection = input('|- Enter An ISBN To Remove: ')\
                
                # If user wants to go back
                if selection == 'b':
                    self.back()
                    return
                
                # Add item to cart
                success = self.cart.remove_from_cart(self.user.user_id, selection)
                if success:
                    print('|----- Item Removed From Cart.')
                else:
                    print('|----- Invalid Selection.')

        self.render_page_header(header_message='Remove From Cart')
        self.display_cart()
        process_selection()

    

def create_database(database_name, user_table_name, cart_table_name, inventory_table_name):
    create_user_database(database_name, user_table_name)
    create_cart_database(database_name, cart_table_name)
    create_inventory_database(database_name, inventory_table_name)

import sqlite3

def add_books_to_inventory():
    # Database connection
    database_name = 'ecommerce_database.db'
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # List of books to add
    books = [
        ("To Kill a Mockingbird", "Harper Lee", "Classic", 281, "1960-07-11", 10, 9780061120084),
        ("1984", "George Orwell", "Dystopian", 328, "1949-06-08", 15, 9780451524935),
        ("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 180, "1925-04-10", 12, 9780743273565),
        ("The Catcher in the Rye", "J.D. Salinger", "Literary Fiction", 234, "1951-07-16", 10, 9780316769488),
        ("Pride and Prejudice", "Jane Austen", "Romance", 432, "1813-01-28", 14, 9780679783268)
    ]

    # SQL query to insert a book
    insert_query = """
    INSERT INTO inventory (Title, Author, Genre, Pages, Release_date, Stock, Isbn)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    # Insert each book
    for book in books:
        try:
            cursor.execute(insert_query, book)
        except sqlite3.IntegrityError:
            print(f"Book with ISBN {book[-1]} already exists in the database.")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()


if __name__ == '__main__':
    database_name = 'ecommerce_database.db'
    user_table_name = 'user'
    cart_table_name = 'cart'
    inventory_table_name = 'inventory'

    
    inventory = Inventory(database_name, inventory_table_name)
    user = User(database_name, user_table_name)
    cart = Cart(database_name, cart_table_name)

    create_database(database_name, user_table_name, cart_table_name, inventory_table_name)

    menu = Menu(user, cart, inventory)
