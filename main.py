from cart import Cart, create_cart_database
from user import User, create_user_database
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
    def __init__(self, user, cart): # add inventory
        self.user = user
        self.cart = cart
        # self.inventory = inventory
        self.nav_stack = ['initial_page']
        self.render_active_page()
    
    def back(self):
        # Remove page from top of stack and render the new active_page
        self.nav_stack.pop()
        self.render_active_page()
    
    def forward(self, page):
        self.nav_stack.append(page)
        self.render_active_page()
    
    def render_page_header(self):
        print('\n|-------------------------')
        if len(self.nav_stack) > 1:
            print('|(B/b) -> Back')
            return
        
        if self.nav_stack[0] == 'initial_page':
            print('|(X/x) -> Quit')


    
    def render_active_page(self):
        pages = {
            'initial_page': self.initial_page,
            'login': self.login_page,
            'register': self.register_page,
            'main_menu': self.main_menu_page
        }
        active_page = self.nav_stack[-1]
        pages[active_page]()
    
    def initial_page(self):
        self.render_page_header()
        print('|----- 1. Login')
        print('|----- 2. Register')
        
        while True:
            selection = input('|- Enter your selection: ')
            # If register page was selected
            if selection == '1':
                self.forward('login')
                return
            elif selection == '2': # if login page was selected
                self.forward('register')
                return
            elif selection == 'X' or selection == 'x':
                return
            else:
                print('|----- Invalid Selection.')


    def login_page(self):

            # Validates username and checks for back selection 
            def enter_username():
                username = input('|- Enter your username: ')

                # If user chooses back
                if username == 'B' or username == 'b':
                    self.back()
                    return False
                
                # Loop while user enters invalid username
                while len(username) < 4:
                    self.render_page_header()
                    print('|----- Username is too short.')
                    username = input('|- Enter your username: ').strip()

                    # If user chooses back
                    if username == 'B' or username == 'b':
                        self.back()
                        return False
                
                return username
            
            # Validates password and checks for back selection 
            def enter_password():
                # print('\n|-------------------------')
                # print('|(B/b) -> Back')
                password = input('|- Enter your password: ')

                # If user chooses back
                if password == 'B' or password == 'b':
                    self.back()
                    return False

                # Loop while user enters invalid password
                while len(password) < 4:
                    print('|----- Password is too short.')
                    password = input('|- Enter your password: ')

                    # If user chooses back
                    if password == 'B' or password == 'b':
                        self.back()
                        return False
                
                return password
            
            self.render_page_header()
            username = enter_username()
            # if user chose back
            if not username:
                return
            
            password = enter_password()
            # if user chose back
            if not password:
                return
            
            while not self.user.logged_in:
                self.render_page_header()

                if self.user.login(username, password):
                    break

                username = enter_username()
                # if user chose back
                if not username:
                    return
                
                password = enter_password()

                # if user chose back
                if not password:
                    return
                
                self.user.login(username, password)
                
            self.forward('main_menu')
    
    def main_menu_page(self):
        print('This is the Main Menu.')
    
    def register_page(self):
        print('This is the Register Page.')

def create_database(database_name, user_table_name, cart_table_name, inventory_table_name):
    create_user_database(database_name, user_table_name)
    create_cart_database(database_name, cart_table_name)
    # create_inventory_database(database_name, inventory_table_name)


if __name__ == '__main__':
    database_name = 'ecommerce_database.db'
    user_table_name = 'user'
    cart_table_name = 'cart'
    inventory_table_name = 'inventory'

    create_database(database_name, user_table_name, cart_table_name, inventory_table_name)
    
    user = User(database_name, user_table_name)
    cart = Cart(database_name, cart_table_name)

    menu = Menu(user, cart)
