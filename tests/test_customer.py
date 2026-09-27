import unittest
from unittest.mock import patch
from src.utils import validate_phone, validate_email
from src.customer import CustomerManager, CUSTOMERS_DB

class TestUtils(unittest.TestCase):
    
    def test_validate_phone_valid(self):
        self.assertTrue(validate_phone("1234567890"))
        self.assertTrue(validate_phone(" 9876543210 "))

    def test_validate_phone_invalid(self):
        self.assertFalse(validate_phone("12345"))
        self.assertFalse(validate_phone("12345678901"))
        self.assertFalse(validate_phone("abcdefghij"))

    def test_validate_email_valid(self):
        self.assertTrue(validate_email("user@example.com"))
        self.assertTrue(validate_email("john.doe@domain.co"))

    def test_validate_email_invalid(self):
        self.assertFalse(validate_email("userexample.com"))
        self.assertFalse(validate_email("user@.com"))
        self.assertFalse(validate_email("user@domain"))

class TestCustomerManager(unittest.TestCase):

    def setUp(self):
        CUSTOMERS_DB.clear()

    @patch("builtins.input", side_effect=["0000000000", "1234567890", "Jane Doe", "invalid-email", "jane@example.com"])
    def test_register_new_customer(self, mock_input):
        customer = CustomerManager.get_or_create_customer()
        
        self.assertEqual(customer["name"], "Jane Doe")
        self.assertEqual(customer["phone"], "1234567890")
        self.assertEqual(customer["email"], "jane@example.com")
        self.assertIn("1234567890", CUSTOMERS_DB)

    @patch("builtins.input", side_effect=["1234567890"])
    def test_returning_customer(self, mock_input):
        CUSTOMERS_DB["1234567890"] = {"name": "John Doe", "email": "john@example.com"}
        
        customer = CustomerManager.get_or_create_customer()
        
        self.assertEqual(customer["name"], "John Doe")
        self.assertEqual(customer["phone"], "1234567890")

if __name__ == "__main__":
    unittest.main()
