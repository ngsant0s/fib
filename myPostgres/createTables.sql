-- CREATING TABLE
CREATE TABLE fibonacci_numbers(
    digit SERIAL,
    fib_value BIGINT,
    CONSTRAINT digit_idx PRIMARY KEY (digit)
);

-- CALCULATING DEFAULT NUMBERS
CREATE FUNCTION fibonacci_function(n INTEGER) RETURNS BIGINT AS $$
DECLARE
    fib BIGINT := 0;
    a BIGINT := 0;
    b BIGINT := 1;
BEGIN
    IF n = 0 THEN
        RETURN 0;
    ELSIF n = 1 THEN
        RETURN 1;
    ELSE
        FOR i IN 2..n LOOP
            fib := a + b;
            a := b;
            b := fib;
        END LOOP;
        RETURN fib;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- INSERTING SEQUENCIAL NUMBERS
DO $$
DECLARE
    i INTEGER;
BEGIN
    FOR i in 1..10 LOOP
        INSERT INTO fibonacci_numbers (digit) VALUES (DEFAULT);
    END LOOP;
END $$;

-- INSERTING CALCULATED NUMBERS
DO $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..10 LOOP
        INSERT INTO fibonacci_numbers (fib_value) VALUES (fibonacci_function(i-1))
    END LOOP;
END $$;