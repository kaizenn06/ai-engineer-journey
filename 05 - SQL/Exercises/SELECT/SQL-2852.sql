SELECT 
    p.name provider_name, 
    SUM(pg.power_generated) total_power_generated
FROM provider p
JOIN region r 
    ON r.id = p.region_id
JOIN renewable_source rs 
    ON rs.provider_id = p.id
JOIN power_generation pg 
    ON pg.source_id = rs.id
WHERE 
    rs.name IN ('Solar', 'Wind')
    AND r.name LIKE '%st'
    AND pg.date BETWEEN '2021-01-01' AND '2021-03-31'
    AND pg.power_generated <> 0
GROUP BY p.id, p.name
HAVING COUNT(rs.name) = 2
ORDER BY total_power_generated DESC
LIMIT 3;