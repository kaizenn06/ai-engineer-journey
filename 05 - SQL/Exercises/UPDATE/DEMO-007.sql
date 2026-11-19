UPDATE SALEORDER s
SET s.Status = 'PAID'
WHERE EXISTS (
    SELECT 1 
    FROM PAYMENT p
    WHERE 
        p.Status = 'PAID'
        AND p.OrderID = s.OrderID
);