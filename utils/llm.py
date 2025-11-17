"""LLM interaction utilities"""
import json
import time
from typing import Dict
from config.settings import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS, MAX_RETRY_COUNT

try:
    from litellm import completion as _litellm_completion
except ModuleNotFoundError:
    _litellm_completion = None


def _call_completion(*args, **kwargs):
    """Lazy wrapper so imports succeed even when litellm is missing."""
    if _litellm_completion is None:
        raise ModuleNotFoundError(
            "Missing dependency 'litellm'. Install via `pip install litellm` "
            "or provide a compatible completion callable."
        )
    return _litellm_completion(*args, **kwargs)

def prompt_llm_for_json(schema: Dict, prompt: str, retry_count: int = 0) -> Dict:
    """Enhanced LLM call with retry logic"""
    schema_text = json.dumps(schema, ensure_ascii=False)
    full_prompt = f"""
Bạn là AI chuyên trích xuất dữ liệu hóa đơn.

QUAN TRỌNG: Trả về JSON hợp lệ 100%, tuân thủ schema, KHÔNG thêm text giải thích.

Schema:
{schema_text}

Dữ liệu hóa đơn:
{prompt}

CHỈ trả về JSON thuần túy, ví dụ:
{{"invoices": [{{"ID_invoice": "HD001", "date": "2025-01-15", "amount": 5200000}}]}}
"""
    
    try:
        response = _call_completion(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": full_prompt}],
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        return json.loads(content)
    
    except json.JSONDecodeError as e:
        if retry_count < MAX_RETRY_COUNT:
            print(f" JSON parse error, retrying... (attempt {retry_count + 1})")
            time.sleep(1)
            return prompt_llm_for_json(schema, prompt, retry_count + 1)
        else:
            print(f" Failed to parse JSON after {retry_count + 1} attempts")
            return {"error": "JSON parsing failed", "raw_response": content}
    
    except Exception as e:
        return {"error": str(e)}