-- Bai bua deo the AC =))
SELECT
    COALESCE(SUM(s.quantity), 0) AS num_products
FROM time AS t
JOIN sales AS s
    ON s.time_id = t.time_id
JOIN products AS p
    ON p.product_id = s.product_id
WHERE p.vegan = TRUE
    AND p.category = 'Hair Care'
    AND t.sale_date >= (
        SELECT DATE_SUB(MAX(t2.sale_date), INTERVAL 6 MONTH)
        FROM time AS t2
    );