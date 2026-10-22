INSERT INTO VipCustomer 
SELECT c.CustID, c.CustomerName, c.City, SUM(s.TotalAmount)
FROM Customer AS c
JOIN SaleOrder AS s ON c.CustID = s.CustID
WHERE YEAR(OrderDate) = 2024
GROUP BY c.CustID, c.CustomerName, c.City
HAVING SUM(s.TotalAmount) >= 2000;