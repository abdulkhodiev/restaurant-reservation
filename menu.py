class MenuItem:
    last_assigned_id = 0

    def __init__(self, name, price, description):
        MenuItem.last_assigned_id += 1
        self.item_id = format(MenuItem.last_assigned_id, '03d')
        self.name = self.validate_name(name)
        self.price = self.get_valid_price(price)
        self.description = description

    @staticmethod
    def validate_name(name):
        if not name.isalpha():
            raise ValueError("Invalid name. Name should contain only alphabetical characters.")
        return name

    def get_valid_price(self, price):
        while True:
            try:
                price = float(price)
                if price <= 0:
                    raise ValueError("Price must be a positive number.")
                return price
            except ValueError:
                print("Invalid price. Please enter a valid number.")
                price = input("Enter item price: ")

class Menu:
    def __init__(self):
        self.menu_items = [
            MenuItem("Cheeseburger", 5.99, "Our classic cheeseburger."),
            MenuItem("Fries", 2.99, "Crispy and delicious."),
            MenuItem("Soda", 1.99, "Coke, Diet Coke, Diet Soda, etc."),
        ]

    def add_menu_item(self):
        while True:
            try:
                name = input("\nEnter item name: ")
                price = input("Enter item price: ")
                description = input("Enter item description: ")

                # Create a new MenuItem instance with input validation
                new_item = MenuItem(name, price, description)

                if len(self.menu_items) < 10:
                    self.menu_items.append(new_item)
                    print("Menu item added successfully.")
                else:
                    print("Cannot add more than 10 menu items.")
                break  # Exit the loop if input is valid
            except ValueError as e:
                print(f"Error: {e}")
                # Re-prompt for input

    def view_menu(self):
        print("\n-----Menu:-----")
        for item in self.menu_items:
            print(f"{item.item_id}. {item.name} - ${item.price}")



    def edit_menu_item(self):
        self.view_menu()  # Display the menu before editing

        item_id = input("\nEnter the item ID of the menu item to edit: ")

        for item in self.menu_items:
            if item.item_id == item_id:
                while True:
                    try:
                        name = input("Enter new item name: ")
                        price = input("Enter new item price: ")
                        description = input("Enter new item description: ")

                        # Create a new MenuItem instance with input validation
                        edited_item = MenuItem(name, price, description)

                        # Update the existing item only if all validations pass
                        item.name = edited_item.name
                        item.price = edited_item.price
                        item.description = edited_item.description

                        print("Menu item edited successfully.")
                        break  # Exit the loop if input is valid
                    except ValueError as e:
                        print(f"Error: {e}")
                        # Re-prompt for input
                break
        else:
            print("Menu item not found.")

    def delete_menu_item(self):
        self.view_menu()  # Display the menu before deleting

        item_id = input("\nEnter the item ID of the menu item to delete: ")

        for item in self.menu_items:
            if item.item_id == item_id:
                self.menu_items.remove(item)
                print("Menu item deleted successfully.")
                break
        else:
            print("Menu item not found.")

    def search_menu_item(self):
        search_query = input("\nEnter the item ID or name to search: ")

        found_items = [item for item in self.menu_items if
                       search_query.lower() in item.name.lower() or search_query == item.item_id]

        if found_items:
            print("Search results:")
            for found_item in found_items:
                print(f"{found_item.item_id}. {found_item.name} - ${found_item.price}")
        else:
            print("No matching items found.")

