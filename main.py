"""Main entry point for the invoice agent"""
from core.agent import ReActAgent

if __name__ == "__main__":
    agent = ReActAgent()
    print("\nMode: Load from file")
    agent.run_from_file("invoices.txt")