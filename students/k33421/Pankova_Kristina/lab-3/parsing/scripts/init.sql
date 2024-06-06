CREATE TABLE financialtransaction (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    category_id INTEGER,
    amount REAL,
    date TEXT,
    description text
);
