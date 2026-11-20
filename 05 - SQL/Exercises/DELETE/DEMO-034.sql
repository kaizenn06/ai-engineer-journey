-- Bai bua meo the AC =))
DELETE lh1
FROM LoyaltyHistory lh1
JOIN LoyaltyHistory lh2
    ON lh1.CustID = lh2.CustID
    AND lh1.PointsChange = lh2.PointsChange
    AND lh1.Reason = lh2.Reason
    AND lh1.ChangeDate < lh2.ChangeDate
WHERE lh1.Reason = 'WELCOME_BONUS'
AND (
    SELECT COALESCE(SUM(s.TotalAmount), 0)
    FROM SaleOrder s
    WHERE s.CustID = lh1.CustID
) < 1000;