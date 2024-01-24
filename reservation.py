from datetime import datetime

class Reservation:
    last_assigned_id = 0

    def __init__(self, customer_name, table_number, reservation_date, reservation_time, menu_items, guests):
        Reservation.last_assigned_id += 1
        self.reservation_id = format(Reservation.last_assigned_id, '03d')
        self.customer_name = customer_name
        self.table_number = table_number
        self.validate_reservation_date(reservation_date)
        self.validate_reservation_time(reservation_time)
        self.reservation_date = reservation_date
        self.reservation_time = reservation_time
        self.menu_items = menu_items 
        self.guests = guests

    def validate_reservation_date(self, reservation_date):
        while True:
            try:
                datetime.strptime(reservation_date, '%Y-%m-%d')
                break  # Exit the loop if the format is correct
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                reservation_date = input("Enter reservation date (YYYY-MM-DD): ")

    def validate_reservation_time(self, reservation_time):
        while True:
            try:
                datetime.strptime(reservation_time, '%H:%M')
                break 
            except ValueError:
                print("Invalid time format. Please use HH:MM.")
                reservation_time = input("Enter reservation time (HH:MM): ")
                
    def calculate_total_price(self, menu):
        total_price = 0.0
        for item_id, quantity in self.menu_items.items():
            menu_item = next((item for item in menu.menu_items if item.item_id == item_id), None)
            if menu_item:
                total_price += menu_item.price * quantity
        return total_price

class ReservationManager:
    def __init__(self):
        self.reservations = []
        
    def __iter__(self):
        return iter(self.reservations)

    def add_reservation(self, reservation, menu):
        self.reservations.append(reservation)
        print("Reservation added successfully.")


    def view_reservations(self, menu):
        print("\nReservations:")
        for reservation in self.reservations:
            print(f"{reservation.reservation_id}. {reservation.customer_name} - Table {reservation.table_number}")
            print(f"   Date: {reservation.reservation_date}")
            print(f"   Time: {reservation.reservation_time}")
            print(f"   Number of Guests: {reservation.guests}")

            # Display menu items and quantities
            print("   Foods Ordered:")
            for item_id, quantity in reservation.menu_items.items():
                menu_item = next((item for item in menu.menu_items if item.item_id == item_id), None)
                if menu_item:
                    print(f"      {menu_item.name} - Quantity: {quantity}")

            total_price = reservation.calculate_total_price(menu)
            print(f"   Total Price: ${total_price}")

            print("-" * 30)

    def edit_reservation(self, reservation_id, menu):
        for reservation in self.reservations:
            if reservation.reservation_id == reservation_id:
                while True:
                    print("\nEditing Reservation:")
                    print("1. Edit Customer Name")
                    print("2. Edit Table Number")
                    print("3. Edit Reservation Date")
                    print("4. Edit Reservation Time")
                    print("5. Edit Menu Items")
                    print("6. Edit Number of Guests")
                    print("0. Exit Editing")

                    choice = input("Enter your choice (0-6): ")

                    if choice == "1":
                        new_customer_name = input("Enter new customer name: ")
                        reservation.customer_name = new_customer_name
                        print("Customer name updated successfully.")
                    elif choice == "2":
                        new_table_number = int(input("Enter new table number: "))
                        # Check if the new table number is available
                        if new_table_number not in set(range(1, 11)):
                            print("Invalid table number. Please enter a number between 1 and 10.")
                            continue
                        reservation.table_number = new_table_number
                        print("Table number updated successfully.")
                    elif choice == "3":
                        new_reservation_date = input("Enter new reservation date (YYYY-MM-DD): ")
                        try:
                            reservation.validate_reservation_date(new_reservation_date)
                            reservation.reservation_date = new_reservation_date
                            print("Reservation date updated successfully.")
                        except ValueError as ve:
                            print(f"Error: {ve}. Please re-enter the date.")
                            continue  # Prompt the user again
                    elif choice == "4":
                        new_reservation_time = input("Enter new reservation time (HH:MM): ")
                        try:
                            reservation.validate_reservation_time(new_reservation_time)
                            reservation.reservation_time = new_reservation_time
                            print("Reservation time updated successfully.")
                        except ValueError as ve:
                            print(f"Error: {ve}. Please re-enter the time.")
                            continue  # Prompt the user again
                    elif choice == "5":
                        # Edit Menu Items
                        new_menu_items = {}
                        while True:
                            menu_item_id = input("Enter menu item ID or 'done' to finish: ")
                            if menu_item_id.lower() == 'done':
                                break

                            valid_menu_item = next((item for item in menu.menu_items if item.item_id == menu_item_id), None)
                            if not valid_menu_item:
                                print("Invalid menu item ID. Please enter a valid ID.")
                                continue

                            while True:
                                try:
                                    new_quantity = int(input(f"Enter the new quantity for menu item {menu_item_id}: "))
                                    if new_quantity <= 0:
                                        raise ValueError("Quantity must be a positive integer. Please enter a valid quantity.")
                                    break
                                except ValueError as ve:
                                    print(f"Error: {ve}. Please re-enter the quantity.")

                            new_menu_items[menu_item_id] = new_quantity

                        reservation.menu_items = new_menu_items
                        print("Menu items updated successfully.")
                    elif choice == "6":
                        new_guests = int(input("Enter the new number of guests: "))
                        if new_guests <= 0:
                            print("Number of guests must be a positive integer.")
                            continue  # Prompt the user again
                        else:
                            reservation.guests = new_guests
                            print("Number of guests updated successfully.")
                    elif choice == "0":
                        print("Exiting Editing.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
                break
        else:
            print("Reservation not found.")

    def delete_reservation(self, reservation_id, menu):
        for reservation in self.reservations:
            if reservation.reservation_id == reservation_id:
                self.reservations.remove(reservation)
                print("Reservation deleted successfully.")
                break
        else:
            print("Reservation not found.")

