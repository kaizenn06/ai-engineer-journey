-- Bai bua meo the Ac =))
DELETE FROM CustomerArchive ca
WHERE
    COALESCE(
        (
            SELECT SUM(s.TotalAmount)
            FROM SaleOrder s
            WHERE s.CustID = ca.CustID
              AND s.OrderDate < '2024-01-01'
        ), 0
    ) < 500

    AND NOT EXISTS (
        SELECT 1
        FROM SaleOrder s
        WHERE s.CustID = ca.CustID
          AND s.OrderDate >= '2024-01-01'
    );