SELECT 
    (r2.recycling_rate - r1.recycling_rate) rate_difference
FROM recycling_rates r1
JOIN recycling_rates r2 
    ON r2.material = r1.material 
WHERE 
    r1.material = 'glass' 
    AND r1.year = 2018 
    AND r2.year = 2019