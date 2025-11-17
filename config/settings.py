"""Configuration settings for the invoice agent"""
import os

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ['GROQ_API_KEY'] = GROQ_API_KEY

# Model Configuration
LLM_MODEL = "groq/llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 800
MAX_RETRY_COUNT = 2

# Agent Configuration
MAX_ITERATIONS = 15
QUALITY_THRESHOLD = 70

# File Paths
DEFAULT_OUTPUT_DIR = "outputs"
CHART_FILENAME = "invoice_revenue_chart.png"

# Date Formats
SUPPORTED_DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]