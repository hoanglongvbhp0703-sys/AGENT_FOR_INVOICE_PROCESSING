"""Control flow tools"""
from typing import Dict, Any

def terminate(action_context: Dict, message: str) -> Dict:
    """Terminate with summary"""
    summary = {
        "status": "completed",
        "message": message,
        "statistics": {
            "invoices_stored": len(action_context.get("invoice_storage", {})),
            "months_tracked": len(action_context.get("monthly_total_storage", {})),
            "total_revenue": sum(action_context.get("monthly_total_storage", {}).values())
        }
    }
    return summary


def error_recovery(action_context: Dict, issue: Any = None) -> Dict:
    """Provide guidance when a plan step fails."""
    if isinstance(issue, dict):
        issue_summary = issue.get("error") or issue.get("message") or repr(issue)
    else:
        issue_summary = issue or "Unknown issue"
    
    recovery_actions = []
    if not action_context.get("invoice_storage"):
        recovery_actions.append("Re-run extraction to populate invoice_storage.")
    if not action_context.get("monthly_total_storage"):
        recovery_actions.append("Recalculate totals using total_amount.")
    if not recovery_actions:
        recovery_actions.append("Review previous step outputs for anomalies.")
    
    return {
        "status": "recovered",
        "issue": issue_summary,
        "next_actions": recovery_actions
    }