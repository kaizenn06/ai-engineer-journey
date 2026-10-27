SELECT username, fname, lname, started_on
FROM Instructor
WHERE started_on < NOW();