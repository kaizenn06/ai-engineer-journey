SELECT 
    c.CustID,
    c.CustomerName
FROM CUSTOMER c
LEFT JOIN SALEORDER s
    ON c.CustID = s.CustID
GROUP BY c.CustID
HAVING COUNT(s.CustID) = 0
ORDER BY c.CustID;