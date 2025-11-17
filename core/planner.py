"""Dynamic planning with ReAct pattern"""
from typing import List, Dict

class AgentPlanner:
    """Dynamic planning with ReAct pattern"""
    
    @staticmethod
    def create_plan(user_request: str, context: Dict) -> List[Dict]:
        """Create flexible plan based on current state"""
        # Analyze what needs to be done
        needs_extraction = "hóa đơn" in user_request.lower() or "invoice" in user_request.lower()
        has_stored_invoices = len(context.get("invoice_storage", {})) > 0
        
        plan = []
        
        if needs_extraction:
            plan.append({
                "step": "extract",
                "tool": "extract_invoices_data",
                "reasoning": "User provided invoice text that needs extraction"
            })
            plan.append({
                "step": "store",
                "tool": "store_invoice",
                "reasoning": "Extracted data should be stored for future reference",
                "depends_on": "extract"
            })
            plan.append({
                "step": "calculate",
                "tool": "total_amount",
                "reasoning": "Calculate monthly totals for financial tracking",
                "depends_on": "store"
            })
        
        if "biểu đồ" in user_request.lower() or "graph" in user_request.lower():
            plan.append({
                "step": "visualize",
                "tool": "paint_graph",
                "reasoning": "User requested visualization"
            })
        
        plan.append({
            "step": "complete",
            "tool": "terminate",
            "reasoning": "Finalize and summarize results"
        })
        
        return plan
    
    @staticmethod
    def adjust_plan(plan: List[Dict], failed_step: str, error: str) -> List[Dict]:
        """Adjust plan when error occurs"""
        # Remove failed step and add alternative
        new_plan = [s for s in plan if s["step"] != failed_step]
        
        # Add recovery step
        new_plan.insert(0, {
            "step": "recover",
            "tool": "error_recovery",
            "reasoning": f"Previous step '{failed_step}' failed. Attempting recovery.",
            "error_info": error
        })
        
        return new_plan