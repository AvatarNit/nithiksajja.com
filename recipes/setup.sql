.open recipes.db
.mode box

-- This will enforce the foreign key relationships
PRAGMA foreign_keys = ON;

-- DROP TABLE IF EXISTS owners;

-- CREATE TABLE IF NOT EXISTS owners(
--     owner_id INTEGER,
--     first_name TEXT NOT NULL,
--     last_name TEXT NOT NULL,
--     email TEXT NOT NULL UNIQUE,
--     password TEXT,
--     needs_reset INTEGER DEFAULT 1,
--     PRIMARY KEY (owner_id)
-- );

-- CREATE VIEW IF NOT EXISTS dog_owners AS
-- SELECT * FROM dogs NATURAL JOIN owners;