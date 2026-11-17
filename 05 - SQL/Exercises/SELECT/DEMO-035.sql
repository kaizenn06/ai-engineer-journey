SELECT 
    City,
    SUM(Amount) TotalRevenue
FROM (
    (SELECT City, Amount
     FROM OnlineOrder)
  
    UNION ALL
  
    (SELECT City, Amount
     FROM StoreOrder)
) AllOrder
GROUP BY City
ORDER BY City;