SELECT 
    CustID, 
    SUM(Total) TotalRevenue
FROM SALEORDER 
GROUP BY CustID
ORDER BY CustID;