"""ReAct Agent implementation"""
import json
from typing import Dict
from core.memory import Memory
from core.state import AgentState
from core.planner import AgentPlanner
from utils.reflector import AgentReflector
from tools import TOOLS
from config.settings import MAX_ITERATIONS

class ReActAgent:
    """Reasoning and Acting Agent"""
    
    def __init__(self):
        self.memory = Memory()
        self.action_context = {}
        self.state = AgentState.PLANNING
        self.max_iterations = MAX_ITERATIONS
    
    def run(self, user_request: str):
        """Main agent loop with ReAct pattern"""
        print("\n" + "="*60)
        print("AI AGENT STARTED - ReAct Mode")
        print("="*60)
        
        # STEP 1: PLANNING
        print("\nSTEP 1: PLANNING")
        plan = AgentPlanner.create_plan(user_request, self.action_context)
        print(f"Created plan with {len(plan)} steps:")
        for i, step in enumerate(plan, 1):
            print(f"  {i}. {step['tool']} - {step['reasoning']}")
        
        # STEP 2: EXECUTION with Reflection
        print("\nSTEP 2: EXECUTION")
        iteration = 0
        current_plan_index = 0
        
        while iteration < self.max_iterations and current_plan_index < len(plan):
            iteration += 1
            current_step = plan[current_plan_index]
            
            print(f"\n--- Iteration {iteration} ---")
            print(f"Executing: {current_step['tool']}")
            print(f"Reasoning: {current_step['reasoning']}")
            
            relevant_context = self.memory.get_relevant_context(current_step['step'])
            if relevant_context:
                print(f"Context: {relevant_context}")
            
            try:
                result = self._execute_step(current_step, user_request)
                
                success = result.get("status") not in ["failed", "error"]
                
                print(f"Result: {json.dumps(result, ensure_ascii=False, indent=2)[:300]}...")
                
                self.memory.add_episode(
                    step=current_step['step'],
                    action=current_step['tool'],
                    result=result,
                    success=success
                )
                
                if not success:
                    print("Step failed. Adjusting plan...")
                    plan = AgentPlanner.adjust_plan(
                        plan, 
                        current_step['step'],
                        result.get('error', 'Unknown error')
                    )
                    current_plan_index = 0  # Restart from recovery
                    continue
                
                if current_step['tool'] == 'extract_invoices_data':
                    eval_result = result.get('_evaluation', {})
                    if not eval_result.get('passed', True):
                        print(f"Quality check failed: {eval_result.get('issues')}")
                        print(f"Recommendation: {eval_result.get('recommendation')}")
                
                current_plan_index += 1
                
            except Exception as e:
                print(f"Exception: {e}")
                self.memory.add_episode(
                    step=current_step['step'],
                    action=current_step['tool'],
                    result={"error": str(e)},
                    success=False
                )
                break
            
            if iteration % 3 == 0:
                reflection = AgentReflector.reflect_on_progress(
                    self.memory, 
                    current_plan_index, 
                    len(plan)
                )
                print(f"\nREFLECTION:\n{reflection}")
        
        # FINAL SUMMARY
        self._print_final_summary()
    
    def run_from_file(self, file_path: str):
        """Load and process invoices from text file"""
        print("\n" + "="*60)
        print("LOADING INVOICES FROM FILE")
        print("="*60)
        print(f"File: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            invoices = [inv.strip() for inv in content.split("---") if inv.strip()]
            print(f"Found {len(invoices)} invoices in file")
            
            print("\nFirst invoice preview:")
            print("-" * 60)
            print(invoices[0][:200] + "..." if len(invoices[0]) > 200 else invoices[0])
            print("-" * 60)
            
            self.run(content)
            
        except FileNotFoundError:
            print(f"Error: File '{file_path}' does not exist!")
            print("Ensure the file is next to this script or provide the full path.")
        except Exception as e:
            print(f"Error while reading file: {e}")
    
    def _execute_step(self, step: Dict, user_request: str) -> Dict:
        """Execute a single step"""
        tool_name = step['tool']
        
        if tool_name not in TOOLS:
            return {"status": "failed", "error": f"Unknown tool: {tool_name}"}
        
        tool_func = TOOLS[tool_name]
        
        # Prepare arguments based on tool
        if tool_name == "extract_invoices_data":
            return tool_func(self.action_context, user_request)
        
        elif tool_name == "store_invoice":
            # Get last extraction result
            last_extract = self.memory.get_last_result('extract_invoices_data')
            if not last_extract:
                return {"status": "failed", "error": "No extraction data available"}
            return tool_func(self.action_context, last_extract)
        
        elif tool_name == "total_amount":
            # Get stored invoices
            invoices = list(self.action_context.get("invoice_storage", {}).values())
            return tool_func(self.action_context, invoices)
        
        elif tool_name == "paint_graph":
            return tool_func(self.action_context)
        
        elif tool_name == "terminate":
            return tool_func(self.action_context, "Workflow completed successfully")
        
        elif tool_name == "error_recovery":
            issue_details = step.get("error_info") or step.get("reasoning")
            return tool_func(self.action_context, issue_details)
        
        return {"status": "failed", "error": "Unhandled tool"}
    
    def _print_final_summary(self):
        """Print execution summary"""
        print("\n" + "="*60)
        print("FINAL SUMMARY")
        print("="*60)
        
        print(f"\nEpisodes: {len(self.memory.episodic)}")
        print(f"Successful: {sum(1 for ep in self.memory.episodic if ep['success'])}")
        print(f"Failed: {sum(1 for ep in self.memory.episodic if not ep['success'])}")
        
        print("\nData Storage:")
        print(f"  - Invoices: {len(self.action_context.get('invoice_storage', {}))}")
        print(f"  - Monthly totals: {self.action_context.get('monthly_total_storage', {})}")
        
        print("\nEpisode History:")
        for i, ep in enumerate(self.memory.episodic, 1):
            status = "Success" if ep['success'] else "Failed"
            print(f"  {i}. {status} {ep['action']} - {ep['step']}")
        
        if self.action_context.get('invoice_storage'):
            print("\nStored invoice details:")
            for inv_id, inv_data in self.action_context['invoice_storage'].items():
                print(f"  - {inv_id}: {inv_data.get('date')} - {inv_data.get('amount'):,.0f} VND")