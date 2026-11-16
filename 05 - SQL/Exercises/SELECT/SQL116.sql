SELECT username, fname, lname, started_on
FROM Instructor
WHERE started_on >= DATE_FORMAT(CURRENT_TIMESTAMP - INTERVAL 20 YEAR, "%Y-01-01");