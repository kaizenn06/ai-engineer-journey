UPDATE SinhVien 
SET TrangThai = CASE 
    WHEN DiemTB >= 5 THEN 'Đạt'
    WHEN DiemTB < 5 THEN 'Không đạt'
END;