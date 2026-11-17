SELECT 
    MAX(vr.Horsepower) horsepower
FROM Vehicle_Releases vr 
JOIN Vehicle_Types vt 
    ON vt.id = vr.Vehicle_Type_Id
WHERE 
    vt.Name = 'Sedan' 
    AND YEAR(Release_Date) >= 2020;