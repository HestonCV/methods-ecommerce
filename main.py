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
            'cart': self.cart_page
        }
        # Render page from top of stack
        active_page = self.nav_stack[-1]
        pages[active_page]()
    
    def initial_page(self):
        
        # Process input from user
        def process_selection():

            while True:
                selection = input('|- Enter your selection: ')
                # If register page was selected
                if selection == '1':
                    self.forward('login')
                    return
                # if login page was selected
                elif selection == '2': 
                    self.forward('register')
                    return
                elif selection == 'X' or selection == 'x':
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

                # Check if credential is too short
                if len(credential) < 4:
                    print(f'|----- {credential_type.capitalize()} is too short.')
                    continue

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
                elif selection == '4':
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
        print('|----- 4. Logout')
        process_selection()
    
    def account_info_page(self):
        print()
        self.user.view_account_information()
        self.back()
    
    def for_sale_page(self):
        self.inventory.view_Inventory()
        self.inventory.search_Inventory()
        self.back()
    
    def cart_page(self):
        print('This is the Cart Page.')
    

def create_database(database_name, user_table_name, cart_table_name, inventory_table_name):
    create_user_database(database_name, user_table_name)
    create_cart_database(database_name, cart_table_name)
    create_inventory_database(database_name, inventory_table_name)


if __name__ == '__main__':
    database_name = 'ecommerce_database.db'
    user_table_name = 'user'
    cart_table_name = 'cart'
    inventory_table_name = 'inventory'

    
    inventory = Inventory(database_name, inventory_table_name)
    user = User(database_name, user_table_name)
    cart = Cart(database_name, cart_table_name)

    create_database(database_name, user_table_name, cart_table_name, inventory)

    menu = Menu(user, cart)
