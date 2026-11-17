SELECT 
    s.OrderID,
    c.CustomerName
FROM SALEORDER s
JOIN CUSTOMER c 
    ON c.CustID = s.CustID
ORDER BY s.OrderID;