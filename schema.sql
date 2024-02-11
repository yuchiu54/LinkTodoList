create table if not exists items (
    id integer primary key autoincrement,
    name text not null,
    created timestamp not null default current_timestamp,
    status string default "on-going" check (status="done" or status="on-going" or status="cancel")
);

create table if not exists urls (
    id integer primary key autoincrement,
    item_id integer not null,
    content text not null,
    FOREIGN KEY (item_id) REFERENCES items (id)
);
