SELECT DISTINCT a1.Title
FROM Artworks a1
JOIN Exhibitions e1
    ON a1.ArtworkID = e1.ArtworkID
WHERE a1.title <> 'Sunflowers'
AND EXISTS (
    SELECT 1
    FROM Artworks a2
    JOIN Exhibitions e2
        ON a2.ArtworkID = e2.ArtworkID
    WHERE a2.title = 'Sunflowers'
      AND e2.ExhibitionID = e1.ExhibitionID
);