from interface import display_start_interface
from menu import Menu
from reservation import ReservationManager
from datetime import datetime
from reservation import Reservation

def staff_interface(reservation_manager, menu):
    while True:
        print("\n-----Staff Interface:-----")
        print("1. Menu Management")
        print("2. Reservation Management")
        print("0. Exit")

        choice = input("\nEnter your choice (0-2): ")

        if choice == "1":
            menu_management_console(menu)
        elif choice == "2":
            reservation_management_console(reservation_manager, menu)
        elif choice == "0":
            display_start_interface()
            break
        else:
            print("Invalid choice. Please try again.")            

def menu_management_console(menu):
    while True:
        print("\n-----Menu Management:-----\n")
        print("1. Add MenuItem")
        print("2. View Menu")
        print("3. Edit MenuItem")
        print("4. Delete MenuItem")
        print("5. Search MenuItem")
        print("0. Exit")

        choice = input("\nEnter your choice (0-5): ")

        if choice == "1":
            menu.add_menu_item()
        elif choice == "2":
            menu.view_menu()
        elif choice == "3":
            menu.edit_menu_item()
        elif choice == "4":
            menu.delete_menu_item()
        elif choice == "5":
            menu.search_menu_item()
        elif choice == "0":
            print("Exiting Menu Management.")
            break
        else:
            print("Invalid choice. Please try again.")

def reservation_management_console(reservation_manager, menu):
    while True:
        print("\n-----Reservation Management:-----\n")
        print("1. Add Reservation")
        print("2. View Reservations")
        print("3. Edit Reservation")
        print("4. Delete Reservation")
        print("0. Exit")

        choice = input("\nEnter your choice (1-5): ")
         
        if choice == "1":
            try:
                customer_name = input("Enter customer name: ")

                # Display available tables
                available_tables = set(range(1, 11))
                current_datetime = datetime.now()
                for reservation in reservation_manager.reservations:
                    if (
                        reservation.reservation_date == current_datetime.strftime('%Y-%m-%d')
                        and reservation.reservation_time == current_datetime.strftime('%H:%M')
                    ):
                        available_tables.discard(reservation.table_number)

                while True:
                    print("Available tables:", available_tables)
                    table_number = int(input("Enter table number: "))
                    
                    # Check if the selected table is available
                    if table_number not in available_tables:
                        print("Invalid table number. Please choose an available table.")
                        continue  # Prompt the user again


                    conflicting_reservations = [
                        reservation for reservation in reservation_manager.reservations
                        if (
                            reservation.table_number == table_number
                            and reservation.reservation_date == reservation_date
                            and reservation.reservation_time == reservation_time
                        )
                    ]
                
                    if conflicting_reservations:
                        print("Warning: Table already reserved at the specified date and time. Please choose a different table, date, or time.")
                        continue

                    break   # Exit the loop if a valid table number is entered

                reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                reservation_time = input("Enter reservation time (HH:MM): ")

                # Check for existing reservation with the same date, time, and table number
                conflicting_reservations = [
                    reservation for reservation in reservation_manager
                    if (
                        reservation.table_number == table_number
                        and reservation.reservation_date == reservation_date
                        and reservation.reservation_time == reservation_time
                    )
                ]
                
                if conflicting_reservations:
                    print("Warning: Table already reserved at the specified date and time. Please choose a different table, date, or time.")
                    continue  # Prompt the user again

                # Display menu items
                menu.view_menu()

                # Get menu item IDs and quantities from the user
                menu_items = {}
                while True:
                    menu_item_id = input("Enter menu item ID or 'done' to finish: ")
                    if menu_item_id.lower() == 'done':
                        break

                    # Validate menu item ID
                    valid_menu_item = next((item for item in menu.menu_items if item.item_id == menu_item_id), None)
                    if not valid_menu_item:
                        print("Invalid menu item ID. Please enter a valid ID.")
                        continue

                    while True:
                        try:
                            quantity = int(input(f"Enter the quantity for menu item {menu_item_id}: "))
                            if quantity <= 0:
                                raise ValueError("Quantity must be a positive integer. Please enter a valid quantity.")
                            break 
                        except ValueError as ve:
                            print(f"Error: {ve}. Please re-enter the quantity.")

                    menu_items[menu_item_id] = quantity

                guests = int(input("Enter the number of guests: "))
                if guests <= 0:
                    raise ValueError("Number of guests must be a positive integer.")

                reservation = Reservation(
                    customer_name, table_number, reservation_date, reservation_time, menu_items, guests
                )
                
                total_price = reservation.calculate_total_price(menu)
                print(f"Total Price for Reservation: ${total_price}")
                reservation_manager.add_reservation(reservation, menu)
                break
                

            except ValueError as e:
                print(f"Error: {e}. Please re-enter the information.")



        if choice == "2":
            reservation_manager.view_reservations(menu)
        elif choice == "3":
            reservation_id = input("Enter the reservation ID to edit: ")
            reservation_manager.edit_reservation(reservation_id, menu)
        elif choice == "4":
            reservation_id = input("Enter the reservation ID to delete: ")
            reservation_manager.delete_reservation(reservation_id, menu)
        elif choice == "0":
            print("Exiting Reservation Management.")
            break
        else:
            print("Invalid choice. Please try again.")

def customer_interface(reservation_manager, menu):
    while True:
        print("\n-----Customer Interface:-----\n")
        print("1. View Menu")
        print("2. Make Reservation")
        print("3. View Reservations")
        print("4. Update Reservation")
        print("5. Cancel Reservation")
        print("0. Exit")

        choice = input("\nEnter your choice (0-5): ")

        if choice == "1":
            # View Menu
            menu.view_menu()
        elif choice == "2":
            # Make Reservation
            make_reservation_interface(reservation_manager, menu)
        elif choice == "3":
            # View Reservations
            reservation_manager.view_reservations(menu)
        elif choice == "4":
            # Update Reservation
            reservation_id = input("Enter the reservation ID to update: ")
            reservation_manager.edit_reservation(reservation_id, menu)  # Pass 'menu' as the second argument
        elif choice == "5":
            # Cancel Reservation
            reservation_id = input("Enter the reservation ID to cancel: ")
            reservation_manager.delete_reservation(reservation_id, menu)  # Pass 'menu' as the second argument
        elif choice == "0":
            display_start_interface()
            break
        else:
            print("Invalid choice. Please try again.")


def make_reservation_interface(reservation_manager, menu):
    try:
        customer_name = input("Enter your name: ")

        # Display available tables
        available_tables = set(range(1, 11))
        current_datetime = datetime.now()
        for reservation in reservation_manager.reservations:
            if (
                reservation.reservation_date == current_datetime.strftime('%Y-%m-%d')
                and reservation.reservation_time == current_datetime.strftime('%H:%M')
            ):
                available_tables.discard(reservation.table_number)

        while True:
            print("Available tables:", available_tables)
            table_number = int(input("Enter table number: "))
            
            # Check if the selected table is available
            if table_number not in available_tables:
                print("Invalid table number. Please choose an available table.")
                continue  # Prompt the user again

            # Check if the selected table is available at the given time
            conflicting_reservations = [
                reservation for reservation in reservation_manager.reservations
                if (
                    reservation.reservation_date == current_datetime.strftime('%Y-%m-%d')
                    and reservation.reservation_time == current_datetime.strftime('%H:%M')
                    and reservation.table_number == table_number
                )
            ]
            if conflicting_reservations:
                print(f"Table {table_number} is already reserved at the selected time. Please choose another table.")
                continue

            break   # Exit the loop if a valid table number is entered

        reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
        reservation_time = input("Enter reservation time (HH:MM): ")

        # Check for existing reservation with the same date, time, and table number
        conflicting_reservations = [
            reservation for reservation in reservation_manager
            if (
                reservation.table_number == table_number
                and reservation.reservation_date == reservation_date
                and reservation.reservation_time == reservation_time
            )
        ]

        if conflicting_reservations:
            print("Warning: Table already reserved at the specified date and time. Please choose a different table, date, or time.")
            return  # Prompt the user again

        # Display menu items
        menu.view_menu()

        # Get menu item IDs and quantities from the user
        menu_items = {}
        while True:
            menu_item_id = input("Enter menu item ID or 'done' to finish: ")
            if menu_item_id.lower() == 'done':
                break

            # Validate menu item ID
            valid_menu_item = next((item for item in menu.menu_items if item.item_id == menu_item_id), None)
            if not valid_menu_item:
                print("Invalid menu item ID. Please enter a valid ID.")
                continue

            while True:
                try:
                    quantity = int(input(f"Enter the quantity for menu item {menu_item_id}: "))
                    if quantity <= 0:
                        raise ValueError("Quantity must be a positive integer. Please enter a valid quantity.")
                    break  # Exit the quantity input loop if the format is correct
                except ValueError as ve:
                    print(f"Error: {ve}. Please re-enter the quantity.")

            menu_items[menu_item_id] = quantity

        guests = int(input("Enter the number of guests: "))
        if guests <= 0:
            raise ValueError("Number of guests must be a positive integer.")

        reservation = Reservation(
            customer_name, table_number, reservation_date, reservation_time, menu_items, guests
        )
        reservation_manager.add_reservation(reservation, menu)
        
        print("Reservation made successfully.")
    except ValueError as e:
        print(f"Error: {e}. Please re-enter the information.")

