# User role constants
ROLE_CHOICES = [
    ("CLIENT", "Client"),
    ("COMMERCE", "Merchant"),
    ("MANAGER", "Manager"),
    ("ADMIN", "Administrator"),
]

# Role-based permission mapping
ROLE_PERMISSIONS = {
    "COMMERCE": [
        "add_product",
        "change_own_profile",
    ],
    "ADMIN": [
        "view_all_users",
        "change_all_users",
    ],
}
