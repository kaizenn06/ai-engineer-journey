-- Bai bua deo the AC =))
SELECT
    s.OrderID,
    c.CustomerName,
    s.OrderDate,
    s.TotalAmount
FROM SaleOrder s
JOIN Customer c
    ON s.CustID = c.CustID
ORDER BY s.OrderID ASC;