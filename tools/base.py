"""Base tool class and registry"""
from typing import Dict, Callable

class BaseTool:
    """Base class for all tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, action_context: Dict, **kwargs) -> Dict:
        """Execute the tool - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement execute()")

class ToolRegistry:
    """Registry for all available tools"""
    
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
    
    def register(self, name: str, tool_func: Callable):
        """Register a tool function"""
        self._tools[name] = tool_func
    
    def get(self, name: str) -> Callable:
        """Get a tool by name"""
        return self._tools.get(name)
    
    def list_tools(self):
        """List all registered tools"""
        return list(self._tools.keys())