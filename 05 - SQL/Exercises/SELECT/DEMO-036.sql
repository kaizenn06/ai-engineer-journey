-- Bai bua deo the AC =))
SELECT
    c.CustID,
    c.CustomerName
FROM Customer c
JOIN SaleOrder s
    ON c.CustID = s.CustID
JOIN Payment p
    ON s.OrderID = p.OrderID
WHERE p.Status = 'PAID'
  AND s.OrderDate >= '2023-01-01'
  AND s.OrderDate < '2025-01-01'
GROUP BY
    c.CustID,
    c.CustomerName
HAVING SUM(p.Amount) >= 500;