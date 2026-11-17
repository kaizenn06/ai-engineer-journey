-- Bai bua deo the AC =))
SELECT DISTINCT
    c.title
FROM Class c
JOIN Teaches t
    ON c.dept = t.dept
    AND c.number = t.number;