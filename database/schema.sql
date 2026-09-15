CREATE TABLE IF NOT EXISTS lists (
    id INTEGER PRIMARY KEY,
    name TEXT , --deixo a exigencia de nome (NOT NULL) ou mantenho como opcional deixando algumas listas sem nomeação
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    list_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    quantity INTEGER,
    category TEXT,
    price INTEGER ,
    FOREIGN KEY (list_id) REFERENCES lists (id) ON DELETE CASCADE
);
