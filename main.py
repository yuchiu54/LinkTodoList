import argparse
import os
import shutil
import sqlite3
import sys

# copy or update place.split from ~/snap/firefox/common/.mozilla/firefox/l63o54ib.default/places.sqlite
def copy_places_sqlite():
    expanded_user = os.path.expanduser("~/snap/firefox/common/.mozilla/firefox/l63o54ib.default/places.sqlite")
    shutil.copy2(expanded_user, "./")

# predefined sql queries: db for places.sqlite, db for todo
def get_places_sqlite_connection():
    conn = sqlite3.connect("places.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

# access todo list from sqlite
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
    query = "select * from items where status='on-going'"
    query = "select * from items i join urls u on u.item_id = i.id where i.status='on-going'"
    conn = get_todo_connection()
    items = conn.execute(query).fetchall()
    return items

def adding_item(name):
    query = "insert into items (name) values (?)"
    conn = get_todo_connection()
    conn.execute(query, (name,))
    conn.commit()
    conn.close()

def adding_url(item_id, content):
    query = "insert into urls (item_id, content) values (?, ?)"
    conn = get_todo_connection()
    conn.execute(query, (item_id, content,))
    conn.commit()
    conn.close()

def display(items):
    for item in items:
        # name, status, created, content
        name = item["name"]
        status = item["status"]
        created = item["created"]
        content = item["content"]
        result = " - ".join([name, status, content, created])
#        print(f"{name}\t{status}\t{content}\t{created}\t")
        print(result)

def usage():
    guide = """
        python main.py r
                       t --item_name
                       u --item_id --content
    """
    print(guide)

# display items in list with data from sqlite by using queries
def main():
    args = get_parse()
    if args.operation == "r":
        items = read_all_items()
        display(items)
    elif args.operation == "t":
        pass
    elif args.operation == "u":
        pass
    else:
        usage()

#    print(items[0]['name'])
#    adding_item("forever")
#    items = read_all_items()
#    print(items[-1]['name'])

def get_parse():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    sub_parser = parser.add_subparsers(dest="operation")
    read_parser = sub_parser.add_parser("r", help="read todo list")
    read_parser.add_argument("args", nargs="*", help="args for read")
    create_parser = sub_parser.add_parser("c", help="create item or url")
    create_parser.add_argument("args", nargs="+", help="args for create item or url")
    return parser.parse_args()

if __name__ == "__main__":
#    init_todo_tables()
    main()
#    args = get_parse()
