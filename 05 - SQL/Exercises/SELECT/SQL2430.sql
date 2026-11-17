SELECT 
    c.company_name,
    COUNT(CASE WHEN e.gender = 'Female' THEN 1 END) * 100
    / COUNT(e.employee_id) AS female_percentage,
    COUNT(CASE WHEN e.gender = 'Male' THEN 1 END) * 100
    / COUNT(e.employee_id) AS male_percentage
FROM companies c
JOIN departments d 
    ON d.company_id = c.company_id
JOIN employees e
    ON e.dept_id = d.dept_id
GROUP BY c.company_id, c.company_name;