-- CREATING DATABASE
CREATE DATABASE fib_data;

--CONNECTING TO IT
\c fib_data

-- CREATING TABLE
CREATE TABLE IF NOT EXISTS fibonacci_numbers(
    numbers INTEGER PRIMARY KEY,
    fib_value TEXT NOT NULL
);
