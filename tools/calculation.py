"""Calculation tools for invoice totals"""
from typing import Dict, List
from datetime import datetime

def total_amount(action_context: Dict, invoices: List[Dict]) -> Dict:
    """Calculate totals with error handling"""
    if isinstance(invoices, dict):
        invoices = [invoices]
    
    storage_total = action_context.get("monthly_total_storage", {})
    processed = 0
    errors = []
    
    for invoice in invoices:
        try:
            date = invoice.get("date", "")
            amount = invoice.get("amount", 0)
            
            if "/" in date:
                month = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m")
            else:
                month = date[:7] if len(date) >= 7 else "unknown"
            
            storage_total[month] = storage_total.get(month, 0) + amount
            processed += 1
            
        except Exception as e:
            errors.append(f"Invoice {invoice.get('ID_invoice', 'unknown')}: {str(e)}")
    
    action_context["monthly_total_storage"] = storage_total
    
    return {
        "status": "success" if not errors else "partial",
        "processed": processed,
        "errors": errors,
        "monthly_total": storage_total
    }