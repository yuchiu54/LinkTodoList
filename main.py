import argparse
import os
import shutil
import sqlite3

# copy or update place.split from ~/snap/firefox/common/.mozilla/firefox/l63o54ib.default/places.sqlite
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

def get_todo_connection(query):
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

# display items in list with data from sqlite by using queries
def main():
    args = get_parse()
#    if args.messagepath:
#        message_to_steg(args.messagepath)
#
#    if args.stegpath:
#        steg_to_message(args.stegpath)
#    if args.item:
#        print("item", args.item)

def get_parse():
    ap = argparse.ArgumentParser(allow_abbrev=False)

    ap.add_argument(
        "-a",
        "--name",
        help = "adding"
    )

    return ap.parse_args()

if __name__ == "__main__":
    init_todo_tables()
    main()
