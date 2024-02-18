import argparse
import os
import shutil
import sqlite3
import sys

from dotenv import load_dotenv
from terminaltables import AsciiTable

def copy_places_sqlite():
    places_sqlite = os.getenv("PLACES_SQLITE")
    expanded_user = os.path.expanduser(places_sqlite)
    shutil.copy2(expanded_user, "./")

def get_places_sqlite_connection():
    conn = sqlite3.connect("places.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

def init_todo_tables():
    conn = sqlite3.connect("todo.db")
    with open("schema.sql") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def get_todo_connection():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

def read_all_items():
    query = "Select i.id, name, status, content, created From items i LEFT JOIN urls u ON u.item_id = i.id WHERE i.status='on-going'"
    conn = get_todo_connection()
    items = conn.execute(query).fetchall()
    return items

def read_one_item(item_id):
    query = "Select i.id, name, status, content, created From items i JOIN urls u On u.item_id = i.id WHERE i.id=(?)"
    conn = get_todo_connection()
    item = conn.execute(query, (item_id,)).fetchall()
    return item

def create_item(name):
    query = "insert into items (name) values (?)"
    conn = get_todo_connection()
    conn.execute(query, (name,))
    conn.commit()
    conn.close()

def create_url(item_id, content):
    query = "insert into urls (item_id, content) values (?, ?)"
    conn = get_todo_connection()
    conn.execute(query, (item_id, content,))
    conn.commit()
    conn.close()

def remove_item_from_list(item_id, status):
    query = f"UPDATE items SET status=? WHERE id=?"
    conn = get_todo_connection()
    conn.execute(query, [status, item_id])
    conn.commit()
    conn.close()

def display(items):
    headers = ["id", "name", "status", "content", "created"]
    item_list = [list(item) for item in items]
    item_list.insert(0, headers)
    table = AsciiTable(item_list)
    print(table.table)

def usage():
    guide = """
        python main.py r
                       i    --item_name
                       u    --item_id    --content
                       d    --item_id    --status
    """
    print(guide)

# display items in list with data from sqlite by using queries
def main():
    args = get_parse()
    if args.operation == "r":
        if len(args.params) == 0:
            items = read_all_items()
            display(items)
        else:
            if args.params[0] == "o":
                item_id = args.params[1]
                item = read_one_item(item_id)
                display(item)

    elif args.operation == "i":
        item_name = args.params[0]
        create_item(item_name)

    elif args.operation == "u":
        item_id = args.params[0]
        content = args.params[1]
        create_url(item_id, content)

    elif args.operation == "d":
        item_id = args.params[0]
        status = args.params[1]
        remove_item_from_list(item_id, status)

    else:
        usage()

def get_parse():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    sub_parser = parser.add_subparsers(dest="operation")

    read_parser = sub_parser.add_parser("r", help="read todo list")
    read_parser.add_argument("params", nargs="*", help="params for read mode")

    create_parser = sub_parser.add_parser("i", help="create item")
    create_parser.add_argument("params", nargs="+", help="params for creating item")

    create_parser = sub_parser.add_parser("u", help="create url")
    create_parser.add_argument("params", nargs="+", help="params for creating url")

    create_parser = sub_parser.add_parser("d", help="remove item from todo list")
    create_parser.add_argument("params", nargs="+", help="params for removing item")
    return parser.parse_args()

if __name__ == "__main__":
    load_dotenv()
    copy_places_sqlite()
    init_todo_tables()
    main()
