import sqlite3, os, datetime, time


def setupDB(schema:list, db_path:str="data/database.db"):
    
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        currentTS = int(time.time())
        date = datetime.datetime.fromtimestamp(currentTS)
        dateFormat = "%d%b %Y %H:%M:%S"
        printDate = date.strftime(dateFormat)
        print(f"{printDate}: Creating /{db_path}")
        os.makedirs(db_dir)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for table in schema:
        table_name = table["table_name"]
        query_content = []
        for key,value in table["table_columns"].items():
            query_content.append(f"{key} {value}")
        columns_content = ', '.join(query_content)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table["table_name"]}({columns_content})")
        cursor.execute(f"PRAGMA table_info({table["table_name"]})")
        table_columns = [col[1] for col in cursor.fetchall()]
        for name,definitions in table["table_columns"].items():
            found = False
            for column in table_columns:
                if column == name:
                    found = True
                    break
            if not found:
                currentTS = int(time.time())
                date = datetime.datetime.fromtimestamp(currentTS)
                dateFormat = "%d%b %Y %H:%M:%S"
                printDate = date.strftime(dateFormat)
                print(f"{printDate}: Adding {name} - {definitions} to {table["table_name"]}")
                cursor.execute(f"ALTER TABLE {table["table_name"]} ADD COLUMN {name} {definitions}")
        
        for column in table_columns:
            found = False
            for name,definitions in table["table_columns"].items():
                if column == name:
                    found = True
                    break
            if not found:
                currentTS = int(time.time())
                date = datetime.datetime.fromtimestamp(currentTS)
                dateFormat = "%d%b %Y %H:%M:%S"
                printDate = date.strftime(dateFormat)
                print(f"{printDate}: Dropping {column} from {table["table_name"]}")
                cursor.execute(f"ALTER TABLE {table["table_name"]} DROP COLUMN {column}")
        
                    
    conn.commit()
    conn.close()

path = "data/database.db"
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
setupDB(schema=schema, db_path=path)