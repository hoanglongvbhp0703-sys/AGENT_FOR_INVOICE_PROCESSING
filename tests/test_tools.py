"""Unit tests for tools"""
import unittest
from tools.storage import store_invoice
from tools.calculation import total_amount
from utils.validators import validate_invoice_data, is_valid_date

class TestInvoiceTools(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.action_context = {}
        self.sample_invoice = {
            "ID_invoice": "HD001",
            "date": "2025-01-15",
            "amount": 5200000
        }
    
    def test_validate_invoice_valid(self):
        """Test valid invoice validation"""
        is_valid, errors = validate_invoice_data(self.sample_invoice)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_invoice_missing_id(self):
        """Test invoice validation with missing ID"""
        invalid_invoice = {
            "date": "2025-01-15",
            "amount": 5200000
        }
        is_valid, errors = validate_invoice_data(invalid_invoice)
        self.assertFalse(is_valid)
        self.assertIn("Missing ID_invoice", errors)
    
    def test_is_valid_date(self):
        """Test date validation"""
        self.assertTrue(is_valid_date("2025-01-15"))
        self.assertTrue(is_valid_date("15/01/2025"))
        self.assertFalse(is_valid_date("invalid-date"))
    
    def test_store_invoice(self):
        """Test invoice storage"""
        result = store_invoice(self.action_context, self.sample_invoice)
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["stored"]), 1)
        self.assertIn("HD001", self.action_context["invoice_storage"])
    
    def test_store_multiple_invoices(self):
        """Test storing multiple invoices"""
        invoice_data = {
            "invoices": [
                {"ID_invoice": "HD001", "date": "2025-01-15", "amount": 5200000},
                {"ID_invoice": "HD002", "date": "2025-01-20", "amount": 3100000}
            ]
        }
        result = store_invoice(self.action_context, invoice_data)
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["stored"]), 2)
    
    def test_total_amount(self):
        """Test amount calculation"""
        invoices = [
            {"ID_invoice": "HD001", "date": "2025-01-15", "amount": 5200000},
            {"ID_invoice": "HD002", "date": "2025-01-20", "amount": 3100000}
        ]
        result = total_amount(self.action_context, invoices)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["processed"], 2)
        self.assertIn("2025-01", result["monthly_total"])
        self.assertEqual(result["monthly_total"]["2025-01"], 8300000)

if __name__ == '__main__':
    unittest.main()