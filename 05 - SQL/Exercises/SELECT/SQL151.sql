SELECT 
    l.TenLoaiHang,
    n.TenCongTy,
    n.DiaChi
FROM LOAIHANG l
JOIN MATHANG m 
    ON l.MaLoaiHang = m.MaLoaiHang
JOIN NHACUNGCAP n 
    ON  m.MaCongTy = n.MaCongTy
WHERE l.TenLoaiHang = 'Furniture';