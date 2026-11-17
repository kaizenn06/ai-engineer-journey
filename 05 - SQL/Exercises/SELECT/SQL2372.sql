SELECT 
    AVG(budget) num_budget
FROM (
    SELECT budget 
    FROM ai_budget_usa
    WHERE year BETWEEN 2018 AND 2020

    UNION ALL 
  
    SELECT budget 
    FROM ai_budget_uk
    WHERE year BETWEEN 2018 AND 2020

    UNION ALL 

    SELECT budget 
    FROM ai_budget_japan
    WHERE year BETWEEN 2018 AND 2020
) ai_budget;