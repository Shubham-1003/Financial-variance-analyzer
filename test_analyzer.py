import unittest
from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analyzer import analyze_row


class AnalyzeRowTests(unittest.TestCase):
    def test_revenue_above_budget_is_favourable(self):
        result = analyze_row(
            {"category": "Revenue", "actual": "110", "budget": "100", "type": "revenue"}
        )
        self.assertEqual(result["variance"], "10.00")
        self.assertEqual(result["variance_pct"], "10.00")
        self.assertEqual(result["status"], "Favourable")

    def test_expense_above_budget_is_unfavourable(self):
        result = analyze_row(
            {"category": "Labour", "actual": "110", "budget": "100", "type": "expense"}
        )
        self.assertEqual(result["status"], "Unfavourable")

    def test_expense_below_budget_is_favourable(self):
        result = analyze_row(
            {"category": "Labour", "actual": "90", "budget": "100", "type": "expense"}
        )
        self.assertEqual(result["status"], "Favourable")

    def test_zero_budget_has_blank_percentage(self):
        result = analyze_row(
            {"category": "Other", "actual": "10", "budget": "0", "type": "expense"}
        )
        self.assertEqual(result["variance_pct"], "")

    def test_invalid_type_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_row(
                {"category": "Thing", "actual": "10", "budget": "8", "type": "unknown"}
            )


if __name__ == "__main__":
    unittest.main()
