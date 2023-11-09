# - databaseName: string
# - tableName: string
# + Cart():
# + Cart(string databaseName, string tableName)
# + viewCart(string userID, string inventoryDatabase): void
# + addToCart(string userID, string ISBN): void
# + removeFromCart(string userID, string ISBN): void
# + checkOut(string userID): void

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
