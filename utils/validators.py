"""Data validation utilities"""
from datetime import datetime
from config.settings import SUPPORTED_DATE_FORMATS

def is_valid_date(date_str: str) -> bool:
    """Validate date format"""
    for fmt in SUPPORTED_DATE_FORMATS:
        try:
            datetime.strptime(date_str, fmt)
            return True
        except:
            continue
    return False

def validate_invoice_data(invoice: dict) -> tuple[bool, list]:
    """
    Validate invoice data structure
    Returns: (is_valid, list_of_errors)
    """
    errors = []
    
    if not invoice.get("ID_invoice"):
        errors.append("Missing ID_invoice")
    
    if not invoice.get("date"):
        errors.append("Missing date")
    elif not is_valid_date(invoice["date"]):
        errors.append("Invalid date format")
    
    if not invoice.get("amount") or invoice.get("amount") == 0:
        errors.append("Missing or zero amount")
    
    return len(errors) == 0, errors