SELECT 
    s1.SID,
    s1.SName
FROM Supplier s1
JOIN Supply s2 
    ON s2.SID = s1.SID
JOIN Product p 
    ON p.PID = s2.PID
JOIN Category c 
    ON c.CatID = p.CatID 
WHERE c.CatName = 'Electronics'
GROUP BY s1.SID, s1.SName
HAVING COUNT(DISTINCT p.PID) >=2;