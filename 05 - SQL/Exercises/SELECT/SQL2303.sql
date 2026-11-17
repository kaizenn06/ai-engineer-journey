SELECT 
    i1.initiative_name, 
    COUNT(i2.student_id) students_impacted 
FROM initiatives i1
JOIN impact i2 
    ON i1.initiative_id = i2.initiative_id
WHERE i1.community_type = 'historically_underrepresented'
GROUP BY i1.initiative_id, i1.initiative_name
ORDER BY students_impacted DESC, i1.initiative_name
LIMIT 5;