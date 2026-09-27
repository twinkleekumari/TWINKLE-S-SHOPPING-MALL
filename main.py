from src.customer import CustomerManager
from src.billing import BillingSystem

def main():
    customer = CustomerManager.get_or_create_customer()
    billing = BillingSystem(customer=customer, tax_rate=0.08)
    billing.add_items_to_cart()

    if not billing.cart:
        print("Cart is empty. Transaction cancelled.")
        return

    subtotal, tax, grand_total = billing.calculate_totals()
    bill_text = billing.generate_bill_text(subtotal, tax, grand_total)
    
    print("\n" + bill_text)

    if billing.process_payment(grand_total):
        billing.send_bill_email(bill_text)

if __name__ == "__main__":
    main()
