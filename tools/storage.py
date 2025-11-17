"""Invoice storage tool"""
from typing import Dict, List

def store_invoice(action_context: Dict, invoice_data: Dict) -> Dict:
    """Store single or multiple invoices"""
    storage = action_context.get("invoice_storage", {})
    
    # Handle both single invoice and array of invoices
    invoices_to_store = []
    if "invoices" in invoice_data:
        invoices_to_store = invoice_data["invoices"]
    else:
        invoices_to_store = [invoice_data]
    
    results = {
        "stored": [],
        "updated": [],
        "failed": []
    }
    
    for invoice in invoices_to_store:
        # Validate
        if not invoice.get("ID_invoice"):
            results["failed"].append({
                "invoice": invoice,
                "error": "Missing ID_invoice"
            })
            continue
        
        invoice_id = invoice["ID_invoice"]
        
        # Check duplicate
        if invoice_id in storage:
            results["updated"].append(invoice_id)
        else:
            results["stored"].append(invoice_id)
        
        storage[invoice_id] = invoice
    
    action_context["invoice_storage"] = storage
    
    return {
        "status": "success",
        "message": f"Stored {len(results['stored'])} new invoices, updated {len(results['updated'])} invoices",
        "stored": results["stored"],
        "updated": results["updated"],
        "failed": results["failed"],
        "total_stored": len(storage)
    }