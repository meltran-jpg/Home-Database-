# Home_Database_LLM

modular smart home database system built with Python and SQLite

this project accepts natural language commands
--> then converts them to SQL through a rule based adapter
--> validates SQL for safety
--> executes queries 
--> returns results through a command line interface

## architecture
user (CLI input)
--> LLM adapter
--> SQL Validator (safety checks)
--> Query Service (execution layer)
--> SQLite Database
-->results (CLI output)

## Project Structure
- 'cli.py' --> User-facing command line interface
- 'services/llm_adapter.py'--> Rule-based natural language to SQL conversion
- 'services/validator.py'-->SQL safety and policy checks
- 'services/query_service.py'-->Core execution service that talks to SQLite
- 'database/schema.sql'--> Relational schema for users/ houses/ floors/ rooms/ devices
- 'database/init_db.py'-->initializes or resets the SQLite database
- 'loader/csv_loader.py'-->Loads device records from CSV
- 'data/devices.csv'-->Example device data

## Schema Model notes
- A 'user' owns one or more 'houses'
- A 'house' has multiple 'floors'
- A'floor' has multiple 'rooms'
- A 'room' contains multiple 'devices'

## Setup

1. Initialize the database:
python database/init_db.py
2. load CSV  data:
python loader/csv_loader.py
3. Run the CLI
python cli.py
# Example Commands
'show on devices'
'show off devices'
'show devices in kitchen'

## Notes on Safety
-only single statement SQL is allowed
- Only 'SELECT' and 'UPDATE' statements are allowed.
- Unsafe keywords like 'DROP' and 'DELETE' are blocked
- 'UPDATE' statements must contain a 'WHERE' clause

## Testing
Run the unit tests:
python -m unittest discover -s tests -p "test_*.py"
