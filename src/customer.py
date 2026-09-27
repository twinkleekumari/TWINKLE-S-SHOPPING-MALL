from src.utils import validate_phone, validate_email

CUSTOMERS_DB = {}

class CustomerManager:
    @staticmethod
    def get_or_create_customer() -> dict:
        """Handles customer lookup or registration."""
        print("\n--- CUSTOMER CHECK-IN ---")
        while True:
            phone = input("Enter Customer Phone Number (10 digits): ").strip()
            if validate_phone(phone):
                break
            print("Invalid phone number! Please enter exactly 10 digits.")

        if phone in CUSTOMERS_DB:
            print(f"Welcome back, {CUSTOMERS_DB[phone]['name']}!")
            customer = CUSTOMERS_DB[phone]
            customer['phone'] = phone
            return customer

        name = input("Enter Customer Name: ").strip()
        while True:
            email = input("Enter Customer Email (for online bill): ").strip()
            if validate_email(email):
                break
            print("Invalid email format! Example: user@example.com")

        customer = {"name": name, "phone": phone, "email": email}
        CUSTOMERS_DB[phone] = customer
        print("New customer registered successfully!")
        return customer
