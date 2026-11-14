SELECT 
    dept, 
    number, 
    SUBSTRING(title, 1, 12) short_title
FROM Class;