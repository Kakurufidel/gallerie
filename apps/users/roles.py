ROLE_CHOICES = [
    ("CLIENT", "Client"),
    ("MERCHANT", "Merchant"),
    ("ADMIN", "Administrator"),
]

ROLE_PERMISSIONS = {
    "MERCHANT": ["add_product", "view_sales"],
    "ADMIN": ["can_manage_merchants"],
}

PRODUCT_CATEGORIES = [
    ("FOOD", "Food"),
    ("CLOTHING", "Clothing"),
    ("ELECTRONICS", "Electronics"),
    ("OTHER", "Other"),
]

VAT_RATES = {
    "STANDARD": 0.20,
    "INTERMEDIATE": 0.10,
    "REDUCED": 0.055,
}
