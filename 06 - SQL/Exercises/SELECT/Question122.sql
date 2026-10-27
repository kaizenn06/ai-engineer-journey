SELECT t.username, t.dept, t.number, c.title
FROM Teaches t 
JOIN Class c ON t.dept = c.dept 
            AND t.number = c.number
ORDER BY t.username
LIMIT 2;