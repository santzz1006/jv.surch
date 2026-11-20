CREATE TABLE IF NOT EXISTS documents (name TEXT PRIMARY KEY, value TEXT NOT NULL, revision INTEGER NOT NULL DEFAULT 0);
INSERT OR IGNORE INTO documents(name,value,revision) VALUES('collection','{"items":[],"suppliers":[],"parcels":[],"offers":[]}',0);
CREATE TABLE IF NOT EXISTS watches (id TEXT PRIMARY KEY, payload TEXT NOT NULL, price REAL, availability TEXT NOT NULL DEFAULT 'unknown', target REAL, last_checked TEXT, error TEXT);
CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, item_id TEXT NOT NULL, kind TEXT NOT NULL, message TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS jobs (name TEXT PRIMARY KEY, lease_until INTEGER NOT NULL DEFAULT 0, last_started INTEGER NOT NULL DEFAULT 0);
INSERT OR IGNORE INTO jobs(name) VALUES('watch');
CREATE TABLE IF NOT EXISTS usage (day TEXT PRIMARY KEY, count INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS shares (id TEXT PRIMARY KEY, folder TEXT NOT NULL, continuous INTEGER NOT NULL DEFAULT 0, payload TEXT NOT NULL, edit_hash TEXT, created_at TEXT NOT NULL);
