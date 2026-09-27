import unittest
from unittest.mock import patch
from src.billing import BillingSystem

class TestBillingSystem(unittest.TestCase):

    def setUp(self):
        self.customer = {
            "name": "Alice Smith",
            "phone": "5551234567",
            "email": "alice@example.com"
        }
        self.billing = BillingSystem(customer=self.customer, tax_rate=0.08)

    @patch("builtins.input", side_effect=["101", "2", "101", "1", "done"])
    def test_add_items_to_cart_consolidation(self, mock_input):
        self.billing.add_items_to_cart()
        
        # Verify duplicated item 101 consolidates quantity (2 + 1 = 3)
        self.assertEqual(len(self.billing.cart), 1)
        self.assertEqual(self.billing.cart[0]["id"], 101)
        self.assertEqual(self.billing.cart[0]["quantity"], 3)
        self.assertAlmostEqual(self.billing.cart[0]["total"], 47.97)

    def test_calculate_totals(self):
        self.billing.cart = [
            {"id": 101, "name": "Wireless Mouse", "price": 15.99, "quantity": 2, "total": 31.98},
            {"id": 103, "name": "USB-C Cable", "price": 8.00, "quantity": 1, "total": 8.00}
        ]
        
        subtotal, tax, grand_total = self.billing.calculate_totals()
        
        self.assertAlmostEqual(subtotal, 39.98)
        self.assertAlmostEqual(tax, 3.1984)
        self.assertAlmostEqual(grand_total, 43.1784)

    def test_generate_bill_text(self):
        self.billing.cart = [
            {"id": 103, "name": "USB-C Cable", "price": 8.00, "quantity": 1, "total": 8.00}
        ]
        subtotal, tax, grand_total = self.billing.calculate_totals()
        bill_text = self.billing.generate_bill_text(subtotal, tax, grand_total)
        
        self.assertIn("OFFICIAL RECEIPT", bill_text)
        self.assertIn("Alice Smith", bill_text)
        self.assertIn("USB-C Cable", bill_text)
        self.assertIn("Grand Total:", bill_text)

    @patch("builtins.input", side_effect=["1", "50.00"])
    def test_process_payment_cash_success(self, mock_input):
        result = self.billing.process_payment(grand_total=43.18)
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["2", ""])
    def test_process_payment_card_success(self, mock_input):
        result = self.billing.process_payment(grand_total=43.18)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
