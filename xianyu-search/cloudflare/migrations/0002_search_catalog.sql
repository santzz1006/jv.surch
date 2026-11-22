CREATE TABLE IF NOT EXISTS catalog_products (
 id TEXT PRIMARY KEY,
 payload TEXT NOT NULL,
 search_text TEXT NOT NULL,
 price REAL,
 first_seen TEXT NOT NULL,
 updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS catalog_updated ON catalog_products(updated_at,id);
