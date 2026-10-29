SELECT ip_address
FROM login_attempts
GROUP BY ip_address
HAVING COUNT(DISTINCT login_status) = 2;