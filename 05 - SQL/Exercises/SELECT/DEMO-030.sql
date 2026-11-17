SELECT 
    c.CustID, 
    c.CustomerName,
    SUM(s1.TotalAmount) TotalSpent
FROM Customer c
JOIN SaleOrder s1 
    ON s1.CustID = c.CustID
WHERE YEAR(s1.OrderDate) = 2024
GROUP BY c.CustID, c.CustomerName
HAVING 
    TotalSpent >= 1000
    AND NOT EXISTS (
        SELECT 1
        FROM SaleOrder s2
        WHERE 
            s2.CustID = c.CustID
            AND YEAR(s2.OrderDate) = 2024
            AND s2.Status = 'CANCELLED'
    );
