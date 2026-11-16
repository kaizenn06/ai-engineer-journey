(
    SELECT 
        u.name results
    FROM Users u
    JOIN MovieRating m 
        ON u.user_id = m.user_id
    GROUP BY m.user_id
    ORDER BY COUNT(m.movie_id) DESC, u.name
    LIMIT 1
)

UNION ALL 

(
    SELECT 
        m1.title
    FROM Movies m1
    JOIN MovieRating m2 
        ON m1.movie_id = m2.movie_id
    WHERE m2.created_at LIKE "2020-02-%"
    GROUP BY m1.movie_id
    ORDER BY AVG(m2.rating) DESC, m1.title
    LIMIT 1
);