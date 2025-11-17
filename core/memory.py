"""Advanced memory system for agent"""
from datetime import datetime
from typing import Any, List, Dict

class Memory:
    """Advanced memory system for agent"""
    def __init__(self):
        self.short_term = []  # Current conversation
        self.long_term = {    # Persistent knowledge
            "successful_workflows": [],
            "failed_attempts": [],
            "learned_patterns": {}
        }
        self.episodic = []    # Step-by-step history
    
    def add_episode(self, step: str, action: str, result: Any, success: bool):
        """Record each action episode"""
        self.episodic.append({
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "action": action,
            "result": result,
            "success": success
        })
    
    def get_relevant_context(self, current_step: str) -> str:
        """Retrieve relevant past experiences"""
        relevant = [ep for ep in self.episodic if ep["step"] == current_step]
        if relevant:
            return f"Previous experience with {current_step}: {relevant[-1]}"
        return ""
    
    def get_success_rate(self) -> float:
        """Calculate success rate of episodes"""
        if not self.episodic:
            return 1.0
        return sum(1 for ep in self.episodic if ep["success"]) / len(self.episodic)
    
    def get_last_result(self, action: str) -> Any:
        """Get the last successful result for a specific action"""
        for ep in reversed(self.episodic):
            if ep['action'] == action and ep['success']:
                return ep['result']
        return None