README – Invoice Agent
Overview
Invoice Agent is a small ReAct-style workflow that ingests raw invoice text, extracts structured data, stores it in memory, calculates monthly totals, and optionally renders a revenue chart. The agent orchestrates its steps through a configurable plan and can run directly from main.py with an input text file.
Key Components
core/agent.py: ReAct loop (planning → execution → reflection), state management, and runtime logging. Supports file-driven runs via run_from_file.
core/planner.py: Builds dynamic plans based on the user request (extraction, storage, totals, visualization, termination).
core/memory.py: Episode history and success tracking used for reflections and retries.
tools/:
extraction.py: Prompts an LLM (via utils/llm.py) to return JSON invoices matching the required schema.
storage.py: Persists invoice dicts in action_context["invoice_storage"], handles duplicates, and reports new/updated IDs.
calculation.py: Aggregates invoice amounts by month and stores results in monthly_total_storage.
visualization.py: Uses matplotlib to plot monthly revenue (invoice_revenue_chart.png).
control.py: Workflow termination summary and recovery guidance.
Configuration / Setup
config/settings.py: Sets LLM credentials/model, retry limits, default chart filename, etc. Ensure GROQ_API_KEY is valid before running.
Requires Python 3.11+ (from the venv path shown) and dependencies in requirements.txt (if provided; otherwise install matplotlib and litellm manually).
Running
Place or paste raw invoices into invoices.txt (each invoice block uses the “HÓA ĐƠN BÁN HÀNG … ---” format).
From repo root: python main.py. Output logs show planning/execution progress, any LLM parse errors, stored invoices, monthly totals, and chart status.
Chart output (when generated) is invoice_revenue_chart.png in the project root.
Testing
tests/test_tools.py covers validation, storage, and total calculations. Run: python -m unittest tests.test_tools.
Notes / Limitations
Extraction is LLM-dependent; large inputs can exceed token limits and cause JSON parse errors or rate-limit responses.
State is in-memory; no database persistence beyond the runtime context.
Visualization requires matplotlib. If missing, the tool reports how to install it.
__pycache__ files are auto-generated and can be ignored or added to .gitignore.
