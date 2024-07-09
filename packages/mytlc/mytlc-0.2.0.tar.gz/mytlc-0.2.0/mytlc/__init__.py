# __init__.py
# This file is used to init mytlc package.
# The file is used to expose specific functions.

from .logger import configure_logging

# Adding additional init as global configuration ou environment verifications when importing module.
# Use the custom logger
configure_logging()
