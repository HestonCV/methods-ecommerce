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
    def __init__(self):
        self.nav_stack = ['initial_page']
        self.render_active_page()
    
    def back(self):
        # Remove page from top of stack and render the new active_page
        self.nav_stack.pop()
        self.render_active_page()
    
    def forward(self, page):
        self.nav_stack.append(page)
        self.render_active_page()
    
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
        print('\n|-------------------------')
        print('|----- 1. Login')
        print('|----- 2. Register')
        selection = int(input('|- Enter your selection: '))

        # If register page was selected
        if selection == 2:
            self.forward('register')
            return
        else: # if login page was selected
            self.forward('login')
            return

    def login_page(self):
            
            def enter_username():
                print('\n|-------------------------')
                print('|(B/b) -> Back')
                username = input('|- Enter your username: ')
                valid_user = False # check database for username

                # If user chooses back
                if username == 'B' or username == 'b':
                    self.back()
                    return False
                
                # Loop while user enters invalid username
                while not valid_user:
                    print('\n|-------------------------')
                    print('|(B/b) -> Back')
                    print('|----- User does not exist.')
                    username = input('|- Enter your username: ').strip()

                    # If user chooses back
                    if username == 'B' or username == 'b':
                        self.back()
                        return False

                    valid_user = True # check database for username
                
                return username
            
            def enter_password():
                print('\n|-------------------------')
                print('|(B/b) -> Back')
                password = input('|- Enter your password: ')

                valid_password = False # check database for password match
                
                # If user chooses back
                if password == 'B' or password == 'b':
                    self.back()
                    return False

                # Loop while user enters invalid password
                while not valid_password:
                    print('\n|-------------------------')
                    print('|(B/b) -> Back')
                    print('|----- Invalid password.')
                    password = input('|- Enter your password: ')

                    # If user chooses back
                    if password == 'B' or password == 'b':
                        self.back()
                        return False
                    
                    valid_password = True # check database for password match
                
                return password

            username = enter_username()

            if not username:
                return
            
            password = enter_password()

            if not password:
                return
            
            # Check database
            print(f'Login successful. Welcome, {username}.')

            self.forward('main_menu')
            
            # Move to main menu page
    
    def main_menu_page(self):
        print('This is the main menu.')
    
    def register_page(self):
        print('Register Page')


if __name__ == '__main__':
    menu = Menu()
