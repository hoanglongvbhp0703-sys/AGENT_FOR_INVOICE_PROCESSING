"""Visualization tools for invoice data"""
from typing import Dict
from config.settings import CHART_FILENAME

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

def paint_graph(action_context: Dict) -> Dict:
    """Create visualization"""
    if plt is None:
        return {
            "status": "failed",
            "error": "matplotlib is not installed",
            "suggestion": "Install with `pip install matplotlib` to enable charting"
        }
    storage_total = action_context.get("monthly_total_storage", {})
    
    if not storage_total:
        return {
            "status": "failed",
            "error": "No data to visualize",
            "suggestion": "Process invoices first"
        }
    
    months = list(storage_total.keys())
    totals = list(storage_total.values())
    
    plt.figure(figsize=(10, 5))
    plt.plot(months, totals, marker="o", linewidth=2)
    plt.title("Monthly revenue")
    plt.xlabel("Month")
    plt.ylabel("Total amount (VND)")
    plt.grid(True)
    plt.xticks(rotation=45)
    
    file_path = CHART_FILENAME
    plt.savefig(file_path, bbox_inches='tight')
    plt.close()
    
    return {
        "status": "success",
        "message": "Chart created",
        "file_path": file_path,
        "data_points": len(months)
    }