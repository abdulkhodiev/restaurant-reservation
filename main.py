from interface import display_start_interface
from console import reservation_management_console, customer_interface, staff_interface
from menu import Menu
from reservation import ReservationManager

def main():
    
    menu_instance = Menu()
    reservation_manager = ReservationManager()

    while True:
        display_start_interface()

        user_choice = input("\nEnter your choice (1 or 2): ")

        if user_choice == "1":
            staff_interface(reservation_manager, menu_instance)  
        elif user_choice == "2":
            customer_interface(reservation_manager, menu_instance) 
        else:
            print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()

