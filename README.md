# SQLite Dynamic Table Classes
This Python script creates SQLite database tables from a schema and generates classes to interact with them (e.g., insert, update, delete, select).

## How to Use
Copy the Code: Copy the main Python script from this repository.

Set Database Path: Update db_path in the script to your desired SQLite database location (e.g., "data/database.db").

Define Schema: Edit the schema list in setupDB() to define your tables and columns.

Run the Script:
Call setupDB() to create/update the database.
### Coming soon ~ Call generate_table_classes(schema) to create classes for each table.



Notes

Requires Python 3.6+ and SQLite 3.35.0+ for DROP COLUMN support.
Customize the schema in setupDB() to match your database needs.

License
MIT License
