
# unit tests for the LLM adapter



import unittest
from services.llm_adapter import SQLCommand, nl_to_sql

#these tests validate that the natural language to SQL translation is working correctly
class AdapterTests(unittest.TestCase):
    # test that a simple command to show devices generates a valid SQLCommand with a SELECT statement
    def test_show_devices(self):
        command = nl_to_sql("show devices")
        self.assertIsInstance(command, SQLCommand)
        self.assertIn("SELECT", command.query.upper())
    def test_turn_on_specific_device(self):
        # test that a command to turn on a specific device generates a valid SQLCommand with an UPDATE statement
        command = nl_to_sql("turn on kitchen light")
        self.assertEqual(command.query, "UPDATE devices SET status = ? WHERE name = ?")
        self.assertEqual(command.params, ("on", "Kitchen Light"))
    def test_count_devices(self):
        #test that a command to count devices generates a valid SQLCommand with COUNT statement
        command = nl_to_sql("how many devices do i have")
        self.assertIn("COUNT(*)", command.query.upper())

if __name__ == "__main__":
    unittest.main()
