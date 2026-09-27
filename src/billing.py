import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.catalog import CATALOG, display_catalog

class BillingSystem:
    def __init__(self, customer: dict, tax_rate: float = 0.08):
        self.tax_rate = tax_rate
        self.cart = []
        self.customer = customer

    def add_items_to_cart(self):
        """Interactively adds items, consolidating duplicates."""
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

            existing_item = next((item for item in self.cart if item["id"] == item_id), None)
            if existing_item:
                existing_item["quantity"] += qty
                existing_item["total"] = existing_item["quantity"] * existing_item["price"]
            else:
                self.cart.append({
                    "id": item_id,
                    "name": product['name'],
                    "price": product['price'],
                    "quantity": qty,
                    "total": product['price'] * qty
                })
            print(f"Added {qty} x {product['name']} to cart.")

    def calculate_totals(self) -> tuple[float, float, float]:
        subtotal = sum(item['total'] for item in self.cart)
        tax = subtotal * self.tax_rate
        grand_total = subtotal + tax
        return subtotal, tax, grand_total

    def process_payment(self, grand_total: float) -> bool:
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
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bill = [
            "=" * 45,
            "              OFFICIAL RECEIPT              ",
            "=" * 45,
            f"Date: {now}",
            f"Customer Name : {self.customer['name']}",
            f"Phone Number  : {self.customer['phone']}",
            f"Email         : {self.customer['email']}",
            "-" * 45,
            f"{'Item':<20}{'Qty':<6}{'Price':<8}{'Total':<8}",
            "-" * 45
        ]
        for item in self.cart:
            bill.append(f"{item['name']:<20}{item['quantity']:<6}${item['price']:<7.2f}${item['total']:<7.2f}")
        bill.extend([
            "-" * 45,
            f"{'Subtotal:':<34}${subtotal:.2f}",
            f"{'Tax (' + str(int(self.tax_rate*100)) + '%):':<34}${tax:.2f}",
            f"{'Grand Total:':<34}${grand_total:.2f}",
            "=" * 45,
            "        Thank you for shopping with us!       ",
            "=" * 45
        ])
        return "\n".join(bill)

    def send_bill_email(self, bill_content: str, sender_email: str = None, sender_password: str = None):
        recipient = self.customer['email']
        print(f"\nSending bill online to {recipient}...")

        if not sender_email or not sender_password:
            print("[SIMULATION MODE] Real email delivery skipped (SMTP credentials not configured).")
            return

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = "Your Shopping Receipt"
        msg.attach(MIMEText(bill_content, 'plain'))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            print("Bill emailed successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
