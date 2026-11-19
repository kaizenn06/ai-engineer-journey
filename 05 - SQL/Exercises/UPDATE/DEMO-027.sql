-- Bai bua deo the AC =))
UPDATE Payment
SET 
    Status = 'PAID',
    PaidAt = '2025-01-01'
WHERE OrderID IN (
    SELECT o.OrderID
    FROM OrderItem o
    JOIN Product p
        ON p.PID = o.PID
    GROUP BY o.OrderID
    HAVING SUM(p.Price * o.Qty) >= 500
)