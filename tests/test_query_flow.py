# tests workflow from natural  language query to SQL command




import tempfile
import unittest
from pathlib import Path
from database.init_db import init_db
from loader.csv_loader import load_devices
from services.llm_adapter import nl_to_sql
from services.query_service import run_query

#
class QueryFlowTests(unittest.TestCase):
	def setUp(self):
		self.temp_dir = tempfile.TemporaryDirectory()
		self.db_path = Path(self.temp_dir.name) / "test_smarthome.db"
		schema_path = Path(__file__).resolve().parents[1] / "database" / "schema.sql"
		csv_path = Path(__file__).resolve().parents[1] / "data" / "devices.csv"
		init_db(db_path=self.db_path, schema_path=schema_path)
		load_devices(db_path=self.db_path, csv_path=csv_path)
    #clean up the temporary directory after tests are done
	def tearDown(self):
		self.temp_dir.cleanup()
# test that a nl query to show devices goes through the whole flow and returns results
	def test_select_query_end_to_end(self):
		response = run_query(nl_to_sql("show devices"), db_path=self.db_path)
		self.assertTrue(response["ok"])
		self.assertGreaterEqual(len(response["results"]), 1)
	def test_update_query_end_to_end(self):
		update_response = run_query(nl_to_sql("turn on bedroom fan"), db_path=self.db_path)
		self.assertTrue(update_response["ok"])
		verify_response = run_query(nl_to_sql("show on devices"), db_path=self.db_path)
		self.assertTrue(any(row["name"] == "Bedroom Fan" for row in verify_response["results"]))
	def test_invalid_query_is_rejected(self):
		response = run_query("DELETE FROM devices WHERE id = 1", db_path=self.db_path)
		self.assertFalse(response["ok"])


if __name__ == "__main__":
	unittest.main()
