# SQLite Dynamic Table Classes
This Python script creates SQLite database tables from a schema.

## How to Use
Copy the main Python script from this repository.
Add a schema and path
Run the function:

```python
path='data/database.db'
schema = [
    {"table_name":"example_user_table",
    "table_columns":{
        "id":"INTEGER PRIMARY KEY AUTOINCREMENT",
        "name":"TEXT NOT NULL",
        "email":"TEXT NOT NULL",
        "password":"TEXT NOT NULL"
        }},
    {"table_name":"example_product_table",
    "table_columns":{
        "id":"INTEGER PRIMARY KEY AUTOINCREMENT",
        "product_id":"INTEGER NOT NULL",
        "name":"TEXT NOT NULL",
        "description":"TEXT DEFAULT 'An amazing new product!'",
        "price":"FLOAT DEFAULT 0"
        }}
]

setupDB(schema, path)
```

## Coming soon
Call tableClass = generateClasses(schema, path) to create classes for each table.

## Notes
Requires Python 3.6+ and SQLite 3.35.0+ for DROP COLUMN support.
Customize the schema in setupDB() to match your database needs.

## License
MIT License
