UPDATE EMPLOYEE e1
SET e1.Salary = e1.Salary * 1.1
WHERE e1.EmpID IN (
    SELECT EmpID
    FROM ( 
        SELECT e2.EmpID 
        FROM EMPLOYEE e2
        JOIN SALEORDER s 
            ON s.EmpID = e2.EmpID
        WHERE s.Status = 'COMPLETED'
        GROUP BY e2.EmpID, e2.FullName
        HAVING SUM(s.TotalAmount) > 50000
    ) temp
);