"""Self-evaluation and quality checking"""
from typing import Dict, Any
from utils.validators import is_valid_date
from config.settings import QUALITY_THRESHOLD

class AgentReflector:
    """Self-evaluation and quality checking"""
    
    @staticmethod
    def evaluate_extraction(extracted_data: Dict) -> Dict[str, Any]:
        """Validate extraction quality"""
        issues = []
        score = 100
        
        # Check required fields
        if not extracted_data.get("ID_invoice"):
            issues.append("Missing invoice ID")
            score -= 40
        
        if not extracted_data.get("date"):
            issues.append("Missing date")
            score -= 30
        elif not is_valid_date(extracted_data["date"]):
            issues.append("Invalid date format")
            score -= 20
        
        if not extracted_data.get("amount") or extracted_data.get("amount") == 0:
            issues.append("Missing or zero amount")
            score -= 30
        
        return {
            "quality_score": score,
            "issues": issues,
            "passed": score >= QUALITY_THRESHOLD,
            "recommendation": "Retry extraction with different prompt" if score < QUALITY_THRESHOLD else "Proceed to next step"
        }
    
    @staticmethod
    def reflect_on_progress(memory, current_step: int, total_steps: int) -> str:
        """Reflect on overall progress"""
        success_rate = memory.get_success_rate()
        
        reflection = f"""
Progress Analysis:
- Completed: {current_step}/{total_steps} steps
- Success Rate: {success_rate*100:.1f}%
- Recent Actions: {len(memory.episodic)} recorded
"""
        
        if success_rate < 0.5:
            reflection += "\n Warning: High failure rate. Consider adjusting approach."
        
        return reflection