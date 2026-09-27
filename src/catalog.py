CATALOG = {
    101: {"name": "Wireless Mouse", "price": 15.99, "category": "Electronics"},
    102: {"name": "Mechanical Keyboard", "price": 45.50, "category": "Electronics"},
    103: {"name": "USB-C Cable", "price": 8.00, "category": "Electronics"},
    104: {"name": "Coffee Mug", "price": 12.00, "category": "Home"},
    105: {"name": "Notebook (A5)", "price": 4.50, "category": "Stationery"},
}

def display_catalog():
    """Prints available products in formatted table."""
    print("\n" + "=" * 40)
    print("           AVAILABLE PRODUCTS           ")
    print("=" * 40)
    print(f"{'ID':<6}{'Item Name':<22}{'Price ($)':<10}")
    print("-" * 40)
    for item_id, details in CATALOG.items():
        print(f"{item_id:<6}{details['name']:<22}{details['price']:<10.2f}")
    print("=" * 40)
