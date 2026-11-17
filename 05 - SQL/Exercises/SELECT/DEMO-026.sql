SELECT 
    o.OrderID, 
    c.CustomerName,
    COUNT(o.PID) TotalLines
FROM Customer c
JOIN SaleOrder s 
    ON s.CustID = c.CustID
JOIN OrderItem o
    ON o.OrderID = s.OrderID
GROUP BY o.OrderID
HAVING COUNT(o.PID) >= 2
ORDER BY o.OrderID;
