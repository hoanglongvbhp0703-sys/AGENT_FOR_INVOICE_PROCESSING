# Invoice Agent

## Overview
- A small ReAct-style workflow for processing raw invoice text.
- Extracts structured JSON data, stores invoices in memory, computes monthly totals.
- Can optionally generate a revenue chart.
- Runs directly from `main.py` using an input text file.

## Key Components
- core/agent.py: ReAct loop (planning → execution → reflection), state management, runtime logging, supports `run_from_file`.
- core/planner.py: Builds dynamic plans based on user request (extraction, storage, totals, visualization, termination).
- core/memory.py: Episode history and success tracking used for reflections and retry attempts.
- tools/extraction.py: Prompts an LLM (via utils/llm.py) to return JSON invoices matching the required schema.
- tools/storage.py: Persists invoice dicts in `action_context["invoice_storage"]`, handles duplicates, reports new/updated IDs.
- tools/calculation.py: Aggregates invoice amounts by month and stores results in `monthly_total_storage`.
- tools/visualization.py: Uses matplotlib to plot monthly revenue (`invoice_revenue_chart.png`).
- tools/control.py: Workflow termination summary and recovery guidance.

## Configuration / Setup
- config/settings.py: Sets LLM credentials/model, retry limits, default chart filename, etc.
- Ensure `GROQ_API_KEY` is valid before running.
- Requires Python 3.11+.
- If needed, install main dependencies: `matplotlib`, `litellm`.

## Running
- Place/paste raw invoices into `invoices.txt` (each invoice block uses format like: "HÓA ĐƠN BÁN HÀNG … ---").
- Run from repo root:
  `python main.py`
- Output logs show plan/execution progress, LLM JSON parse errors, stored invoices, monthly totals, and chart status.
- Chart output (when generated): `invoice_revenue_chart.png` in the project root.

## Testing
- Tests located in: `tests/test_tools.py`
- Run tests:
  `python -m unittest tests.test_tools`

## Notes / Limitations
- Extraction is LLM-dependent; large input may exceed token limits and cause JSON parse or rate-limit errors.
- State is in-memory only; no persistent database storage.
- Visualization requires matplotlib; if missing, the tool will report installation guidance.
- `__pycache__` files are auto-generated and may be ignored or added to `.gitignore`.
