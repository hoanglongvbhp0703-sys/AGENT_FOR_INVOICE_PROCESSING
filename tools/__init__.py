"""Tools package - Registry of all available tools"""
from tools.extraction import extract_invoices_data
from tools.storage import store_invoice
from tools.calculation import total_amount
from tools.visualization import paint_graph
from tools.control import terminate, error_recovery

# Tool registry
TOOLS = {
    "extract_invoices_data": extract_invoices_data,
    "store_invoice": store_invoice,
    "total_amount": total_amount,
    "paint_graph": paint_graph,
    "terminate": terminate,
    "error_recovery": error_recovery
}

__all__ = [
    'TOOLS',
    'extract_invoices_data',
    'store_invoice',
    'total_amount',
    'paint_graph',
    'terminate',
    'error_recovery'
]