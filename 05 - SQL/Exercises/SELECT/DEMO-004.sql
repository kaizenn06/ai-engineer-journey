SELECT 
    CustomerName,
    COALESCE(SUM(
      CASE 
          WHEN p.Status = 'PAID' THEN s.Total
          ELSE 0
      END
      ), 0) PaidTotal
FROM CUSTOMER c
LEFT JOIN SALEORDER s
    ON s.CustID = c.CustID
LEFT JOIN PAYMENT p 
    ON p.OrderID = s.OrderID
GROUP BY c.CustID, c.CustomerName
ORDER BY CustomerName;