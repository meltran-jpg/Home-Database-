# tests the SQL validation logic to ensure tjhat only safe queries are allowed

import unittest
from services.validator import validate_sql
class ValidatorTests(unittest.TestCase):
    def test_allows_select(self):
        is_valid, reason = validate_sql("SELECT * FROM devices")
        self.assertTrue(is_valid)
        self.assertEqual(reason, "ok")
    def test_blocks_drop(self):
        is_valid, reason = validate_sql("DROP TABLE devices")
        self.assertFalse(is_valid)
        self.assertIn("Unsafe keyword", reason)
    def test_blocks_multi_statement(self):
        is_valid, _ = validate_sql("SELECT * FROM devices; SELECT * FROM rooms")
        self.assertFalse(is_valid)
    def test_blocks_update_without_where(self):
        is_valid, reason = validate_sql("UPDATE devices SET status='on'")
        self.assertFalse(is_valid)
        self.assertIn("WHERE", reason)

if __name__ == "__main__":
    unittest.main()
