SELECT 
    s.country
FROM SupplyChainViolations s
JOIN Products p
    ON p.country = s.country
JOIN ProductTransparency pt 
    ON pt.product_id = p.product_id
WHERE 
    s.num_violations >= 1
    AND pt.recycled_materials = TRUE;