SELECT 
    i.project, 
    i.location, 
    i.amount, 
    e.environment, 
    e.social, 
    e.governance
FROM esg_factors e
JOIN impact_investments i
    ON i.company_id = e.company_id
WHERE 
    i.sector = 'Renewable Energy'
    AND e.environment + e.social + e.governance > 7.5;