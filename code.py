import datetime
import json
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ==========================================
# 1. CATALOG & CUSTOMER DATABASE (Simulated)
# ==========================================

CATALOG = {
    101: {"name": "Wireless Mouse", "price": 15.99, "category": "Electronics"},
    102: {"name": "Mechanical Keyboard", "price": 45.50, "category": "Electronics"},
    103: {"name": "USB-C Cable", "price": 8.00, "category": "Electronics"},
    104: {"name": "Coffee Mug", "price": 12.00, "category": "Home"},
    105: {"name": "Notebook (A5)", "price": 4.50, "category": "Stationery"},
}

CUSTOMERS_DB = {}


# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

def validate_phone(phone_str: str) -> bool:
    """Validates 10-digit phone number format."""
    return bool(re.match(r"^\d{10}$", phone_str.strip()))

def validate_email(email_str: str) -> bool:
    """Validates basic email format."""
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email_str.strip()))

def display_catalog():
    """Prints available products."""
    print("\n" + "="*40)
    print("           AVAILABLE PRODUCTS           ")
    print("="*40)
    print(f"{'ID':<6}{'Item Name':<22}{'Price ($)':<10}")
    print("-" * 40)
    for item_id, details in CATALOG.items():
        print(f"{item_id:<6}{details['name']:<22}{details['price']:<10.2f}")
    print("="*40)


# ==========================================
# 3. CORE BILLING SYSTEM LOGIC
# ==========================================

class BillingSystem:
    def __init__(self, tax_rate: float = 0.08):
        self.tax_rate = tax_rate
        self.cart = []
        self.customer = {}

    def capture_customer_details(self):
        """Gets or creates customer details via phone number."""
        print("\n--- CUSTOMER CHECK-IN ---")
        while True:
            phone = input("Enter Customer Phone Number (10 digits): ").strip()
            if validate_phone(phone):
                break
            print("Invalid phone number! Please enter exactly 10 digits.")

        if phone in CUSTOMERS_DB:
            print(f"Welcome back, {CUSTOMERS_DB[phone]['name']}!")
            self.customer = CUSTOMERS_DB[phone]
            self.customer['phone'] = phone
        else:
            name = input("Enter Customer Name: ").strip()
            while True:
                email = input("Enter Customer Email (for online bill): ").strip()
                if validate_email(email):
                    break
                print("Invalid email format! Example: user@example.com")

            self.customer = {"name": name, "phone": phone, "email": email}
            CUSTOMERS_DB[phone] = self.customer
            print(f"New customer registered successfully!")

    def add_items_to_cart(self):
        """Interactively adds items and quantities to cart."""
        display_catalog()
        while True:
            item_input = input("\nEnter Product ID to add (or 'done' to finish): ").strip()
            if item_input.lower() == 'done':
                break

            if not item_input.isdigit() or int(item_input) not in CATALOG:
                print("Invalid Product ID. Please try again.")
                continue

            item_id = int(item_input)
            qty_input = input(f"Enter quantity for '{CATALOG[item_id]['name']}': ").strip()
            
            if not qty_input.isdigit() or int(qty_input) <= 0:
                print("Quantity must be a positive integer.")
                continue

            qty = int(qty_input)
            product = CATALOG[item_id]
            line_total = product['price'] * qty
            
            self.cart.append({
                "id": item_id,
                "name": product['name'],
                "price": product['price'],
                "quantity": qty,
                "total": line_total
            })
            print(f"Added {qty} x {product['name']} to cart.")

    def calculate_totals(self):
        """Calculates subtotal, tax, and total amount."""
        subtotal = sum(item['total'] for item in self.cart)
        tax = subtotal * self.tax_rate
        grand_total = subtotal + tax
        return subtotal, tax, grand_total

    def process_payment(self, grand_total: float) -> bool:
        """Handles payment selection and processing."""
        print("\n--- PAYMENT PROCESSING ---")
        print(f"Total Amount Due: ${grand_total:.2f}")
        print("Select Payment Mode:")
        print("1. Cash\n2. Card (Credit/Debit)\n3. UPI / Online")

        mode_map = {"1": "Cash", "2": "Card", "3": "UPI"}
        while True:
            choice = input("Enter choice (1-3): ").strip()
            if choice in mode_map:
                payment_mode = mode_map[choice]
                break
            print("Invalid choice. Please enter 1, 2, or 3.")

        if payment_mode == "Cash":
            while True:
                received = input(f"Enter cash received (min ${grand_total:.2f}): ")
                try:
                    received_val = float(received)
                    if received_val >= grand_total:
                        change = received_val - grand_total
                        print(f"Payment Successful! Change returned: ${change:.2f}")
                        return True
                    print("Insufficient cash provided.")
                except ValueError:
                    print("Please enter a valid monetary value.")

        elif payment_mode in ["Card", "UPI"]:
            input(f"Processing {payment_mode} payment... Press Enter once transaction completes.")
            print(f"Payment of ${grand_total:.2f} via {payment_mode} Verified!")
            return True

        return False

    def generate_bill_text(self, subtotal: float, tax: float, grand_total: float) -> str:
        """Constructs plain text bill for console output and email sending."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bill = []
        bill.append("=" * 45)
        bill.append("             OFFICIAL RECEIPT             ")
        bill.append("=" * 45)
        bill.append(f"Date: {now}")
        bill.append(f"Customer Name : {self.customer['name']}")
        bill.append(f"Phone Number  : {self.customer['phone']}")
        bill.append(f"Email         : {self.customer['email']}")
        bill.append("-" * 45)
        bill.append(f"{'Item':<20}{'Qty':<6}{'Price':<8}{'Total':<8}")
        bill.append("-" * 45)
        for item in self.cart:
            bill.append(f"{item['name']:<20}{item['quantity']:<6}${item['price']:<7.2f}${item['total']:<7.2f}")
        bill.append("-" * 45)
        bill.append(f"{'Subtotal:':<34}${subtotal:.2f}")
        bill.append(f"{'Tax (' + str(int(self.tax_rate*100)) + '%):':<34}${tax:.2f}")
        bill.append(f"{'Grand Total:':<34}${grand_total:.2f}")
        bill.append("=" * 45)
        bill.append("        Thank you for shopping with us!       ")
        bill.append("=" * 45)
        return "\n".join(bill)

    def send_bill_email(self, bill_content: str, sender_email: str = None, sender_password: str = None):
        """Sends the invoice to the customer's email using SMTP."""
        recipient = self.customer['email']
        print(f"\nSending bill online to {recipient}...")

        # NOTE: Supply valid credentials to send actual emails
        if not sender_email or not sender_password:
            print("[SIMULATION MODE] Real email delivery skipped (SMTP credentials not configured).")
            print("To send real emails, set sender_email and sender_password in the code.")
            return

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = "Your Shopping Receipt"
        msg.attach(MIMEText(bill_content, 'plain'))

        try:
            # SMTP Setup (Example uses Gmail TLS settings)
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            print("Bill emailed successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def run(self):
        """Main execution flow."""
        self.capture_customer_details()
        self.add_items_to_cart()

        if not self.cart:
            print("Cart is empty. Transaction cancelled.")
            return

        subtotal, tax, grand_total = self.calculate_totals()
        bill_text = self.generate_bill_text(subtotal, tax, grand_total)
        
        print("\n" + bill_text)

        payment_success = self.process_payment(grand_total)
        if payment_success:
            self.send_bill_email(bill_text)


# ==========================================
# 4. ENTRY POINT
# ==========================================

if __name__ == "__main__":
    system = BillingSystem(tax_rate=0.08)
    system.run()
