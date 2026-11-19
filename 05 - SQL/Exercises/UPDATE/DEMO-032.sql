UPDATE Customer c
JOIN (
    SELECT CustID
    FROM (
        SELECT 
            c1.CustID, 
            c1.City, 
            SUM(p1.Amount) TotalPaid
        FROM Customer c1 
        JOIN SaleOrder s1
            ON s1.CustID = c1.CustID
        JOIN Payment p1
            ON p1.OrderID = s1.OrderID
        WHERE p1.Status = 'PAID'
        GROUP BY c1.CustID, c1.City
    ) x
    JOIN (
        SELECT 
            t.City, 
            MAX(t.TotalPaid) MaxTotalPaid
        FROM (
            SELECT 
                c2.CustID, 
                c2.City, 
                SUM(p2.Amount) TotalPaid
            FROM Customer c2
            JOIN SaleOrder s2
                ON s2.CustID = c2.CustID
            JOIN Payment p2
                ON p2.OrderID = s2.OrderID
            WHERE p2.Status = 'PAID'
            GROUP BY c2.CustID, c2.City
        ) t
        GROUP BY t.City
    ) y 
        ON x.City = y.City
        AND x.TotalPaid = y.MaxTotalPaid
) result
    ON c.CustID = result.CustID
SET c.Tier = 'TOP_CITY';