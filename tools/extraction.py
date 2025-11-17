"""Invoice extraction tool"""
from typing import Dict
from utils.llm import prompt_llm_for_json
from utils.reflector import AgentReflector

def extract_invoices_data(action_context: Dict, document_text: str) -> Dict:
    """Extract MULTIPLE invoices from text"""
    schema = {
        "type": "object",
        "properties": {
            "invoices": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "ID_invoice": {"type": "string"},
                        "date": {"type": "string"},
                        "amount": {"type": "number"}
                    },
                    "required": ["ID_invoice", "date", "amount"]
                }
            }
        },
        "required": ["invoices"]
    }
    
    extract_prompt = f"""
Phân tích văn bản và trích xuất TẤT CẢ các hóa đơn tìm thấy.

Quy tắc:
- Tìm TẤT CẢ hóa đơn trong văn bản (có thể có nhiều hóa đơn)
- Mỗi hóa đơn cần có: ID_invoice, date, amount
- ID_invoice: Tìm "Số hóa đơn", "Số HĐ", "Invoice", "HD"
- date: Định dạng YYYY-MM-DD hoặc DD/MM/YYYY
- amount: Chỉ số, loại bỏ "VND", "đồng", dấu phẩy, dấu chấm phân cách

Văn bản:
{document_text}

Trả về JSON với mảng invoices.
"""
    
    result = prompt_llm_for_json(schema, extract_prompt)
    
    # Validate each invoice
    if "invoices" in result:
        all_evaluations = []
        for invoice in result["invoices"]:
            evaluation = AgentReflector.evaluate_extraction(invoice)
            all_evaluations.append(evaluation)
        
        result["_evaluation"] = {
            "total_invoices": len(result["invoices"]),
            "passed_count": sum(1 for e in all_evaluations if e["passed"]),
            "details": all_evaluations
        }
    
    return result