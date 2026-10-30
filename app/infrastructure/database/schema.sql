CREATE TABLE IF NOT EXISTS shopping_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER NOT NULL,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    category TEXT NOT NULL DEFAULT 'Sem categoria',
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0),
    FOREIGN KEY (list_id) REFERENCES shopping_lists (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_products_list_id ON products (list_id);
