-- Bai bua deo the AC =))
SELECT
    s.OrderID,
    c.CustomerName,
    s.OrderDate,
    s.TotalAmount
FROM SaleOrder s
JOIN Customer c
    ON s.CustID = c.CustID
WHERE 
    c.City = 'Ha Noi'
    AND s.TotalAmount > 500
ORDER BY s.OrderID;