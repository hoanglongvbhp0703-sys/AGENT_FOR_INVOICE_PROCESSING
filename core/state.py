"""Agent state management"""
from enum import Enum

class AgentState(Enum):
    """Agent lifecycle states"""
    PLANNING = "planning"
    EXECUTING = "executing"
    REFLECTING = "reflecting"
    COMPLETED = "completed"
    ERROR = "error"