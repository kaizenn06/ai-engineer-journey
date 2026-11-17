SELECT 
    SUM(subscription_fee) num_revenue
FROM (
    SELECT subscription_fee 
    FROM mobile_subscribers
    WHERE date LIKE '2025-03-%'

    UNION ALL

    SELECT subscription_fee  
    FROM broadband_subscribers
    WHERE date LIKE '2025-03-%'
) subscribers;