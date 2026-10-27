SELECT t.username, t.dept, t.number 
FROM Teaches t
JOIN Instructor i ON i.username = t.username
ORDER BY i.lname DESC 
LIMIT 2;