CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL
);

INSERT INTO customers (name, email)
VALUES
    ('Kaushik', 'kaushik@example.com'),
    ('Arun', 'arun@example.com'),
    ('Rahul', 'rahul@example.com')
ON CONFLICT DO NOTHING;