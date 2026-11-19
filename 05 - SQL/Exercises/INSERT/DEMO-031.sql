INSERT INTO VipCustomer
SELECT 
    c.CustID, 
    c.CustomerName, 
    c.City, 
    SUM(TotalAmount) TotalSpent2024
FROM Customer c
JOIN SaleOrder s 
    ON s.CustID = c.CustID
WHERE YEAR(s.OrderDate) = 2024
GROUP BY c.CustID, c.CustomerName
HAVING TotalSpent2024 >= 2000;