UPDATE Users
SET name = CONCAT(
    UPPER(LEFT(name, 1)),
    LOWER(SUBSTRING(name, 2))
);