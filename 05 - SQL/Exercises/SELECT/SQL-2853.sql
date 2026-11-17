SELECT 
    p.name provider_name, 
    COUNT(DISTINCT pg.date) days_active,
    SUM(pg.power_generated) total_power_generated
FROM provider p
JOIN region r 
    ON r.id = p.region_id
JOIN renewable_source rs 
    ON rs.provider_id = p.id
JOIN power_generation pg 
    ON pg.source_id = rs.id
WHERE 
    rs.name = 'Solar'
    AND r.name LIKE '%East%'
    AND pg.date BETWEEN '2021-02-01' AND '2021-05-31'
GROUP BY p.id, p.name
ORDER 
    BY days_active DESC, 
    total_power_generated DESC
LIMIT 2;