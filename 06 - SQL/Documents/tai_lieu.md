# MYSQL TỪ SỐ 0 ĐẾN NÂNG CAO

> Tài liệu học MySQL 8.0+ bằng tiếng Việt cho người mới bắt đầu. Mọi ví dụ dùng **một cơ sở dữ liệu bán hàng duy nhất** (`shop_db`) để anh nhìn thấy cùng một dữ liệu được hỏi theo nhiều cách khác nhau.

---

## MỤC LỤC

- [Lộ trình học](#lộ-trình-học)
- [Chuẩn bị: CSDL bán hàng xuyên suốt](#chuẩn-bị-csdl-bán-hàng-xuyên-suốt)
- [Chương 1: Tổng quan về SQL và MySQL](#chương-1-tổng-quan-về-sql-và-mysql)
- [Chương 2: CREATE DATABASE và CREATE TABLE](#chương-2-create-database-và-create-table)
- [Chương 3: INSERT, UPDATE và DELETE](#chương-3-insert-update-và-delete)
- [Chương 4: SELECT từ cơ bản đến nâng cao](#chương-4-select-từ-cơ-bản-đến-nâng-cao)
- [Chương 5: Các hàm trong MySQL](#chương-5-các-hàm-trong-mysql)
- [Chương 6: JOIN nhiều bảng](#chương-6-join-nhiều-bảng)
- [Chương 7: GROUP BY và HAVING](#chương-7-group-by-và-having)
- [Chương 8: Truy vấn con (Subquery)](#chương-8-truy-vấn-con-subquery)
- [Chương 9: UNION](#chương-9-union-và-các-toán-tử-tập-hợp)
- [Chương 10: CTE và Window Functions](#chương-10-cte-và-window-functions)
- [Chương 11: INSERT INTO ... SELECT](#chương-11-insert-into--select)
- [Chương 12: Quy trình suy luận khi làm bài](#chương-12-thứ-tự-thực-thi-và-cách-suy-luận-khi-làm-bài)
- [Chương 13: Các dạng bài thường gặp (có lời giải)](#chương-13-các-dạng-bài-sql-thường-gặp)
- [Chương 14: 30 ví dụ tổng hợp xây từng bước](#chương-14-30-ví-dụ-tổng-hợp-xây-từng-bước)
- [Phụ lục A: Tổng hợp cú pháp](#phụ-lục-a-tổng-hợp-cú-pháp)
- [Phụ lục B: Cheat sheet](#phụ-lục-b-cheat-sheet-tra-cứu-nhanh)
- [Phụ lục C: Khác biệt MySQL / SQL Server / PostgreSQL](#phụ-lục-c-khác-biệt-mysql--sql-server--postgresql)
- [Phụ lục D: Đưa CSDL về trạng thái gốc](#phụ-lục-d-đưa-cơ-sở-dữ-liệu-về-trạng-thái-gốc)

---

## LỘ TRÌNH HỌC

| Bước | Học gì | Chương | Mục tiêu tự kiểm tra |
|---|---|---|---|
| 1 | Khái niệm, kiểu dữ liệu, NULL | 1 | Giải thích được PK, FK, NULL ≠ 0 |
| 2 | Tạo bảng, ràng buộc | 2 | Tự viết được CREATE TABLE có khóa ngoại |
| 3 | Thêm / sửa / xóa | 3 | Biết vì sao thiếu WHERE là nguy hiểm |
| 4 | SELECT + lọc + sắp xếp | 4 | Viết được WHERE phức tạp với AND/OR/LIKE/IN |
| 5 | Hàm | 5 | Dùng CASE WHEN, hàm ngày, hàm NULL |
| 6 | JOIN | 6 | Nối 3–4 bảng, phân biệt ON và WHERE |
| 7 | GROUP BY, HAVING | 7 | Phân biệt WHERE và HAVING không cần nghĩ |
| 8 | Subquery | 8 | Đọc hiểu `UPDATE ... WHERE ... IN (SELECT ...)` |
| 9–11 | UNION, CTE, Window, INSERT…SELECT | 9–11 | Chọn đúng công cụ |
| 12–14 | Quy trình + luyện đề | 12–14 | Tự đọc đề → viết SQL |

**Cách học hiệu quả:** (1) Chạy script CSDL ở phần sau. (2) Với mỗi ví dụ, **tự đoán kết quả trước khi chạy**. (3) Làm bài tự luyện trước khi xem đáp án. (4) Với mọi `UPDATE`/`DELETE`, luôn viết `SELECT` tương ứng chạy trước.

---

## CHUẨN BỊ: CSDL BÁN HÀNG XUYÊN SUỐT

### Sơ đồ quan hệ

```
CUSTOMER 1 ───< SALEORDER >─── 1 EMPLOYEE
                    │ 1
                    │
                    ∨ n
              ORDER_DETAIL >─── 1 PRODUCT
EMPLOYEE (ManagerID) ──► EMPLOYEE (EmpID)    -- quan hệ tự tham chiếu
```

- Một khách hàng có **nhiều** đơn hàng; một nhân viên lập **nhiều** đơn hàng.
- Một đơn hàng có **nhiều** dòng chi tiết; một sản phẩm xuất hiện trong **nhiều** dòng chi tiết.
- `ORDER_DETAIL` là bảng trung gian giữa `SALEORDER` và `PRODUCT` (quan hệ nhiều-nhiều).

### Script tạo CSDL

```sql
DROP DATABASE IF EXISTS shop_db;
CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE shop_db;

CREATE TABLE CUSTOMER (
    CustID    INT AUTO_INCREMENT PRIMARY KEY,
    CustName  VARCHAR(100) NOT NULL,
    City      VARCHAR(50)  NOT NULL,
    Phone     VARCHAR(15)  NOT NULL UNIQUE,
    Email     VARCHAR(100) NULL,
    JoinDate  DATE         NOT NULL
);

CREATE TABLE EMPLOYEE (
    EmpID     INT AUTO_INCREMENT PRIMARY KEY,
    EmpName   VARCHAR(100) NOT NULL,
    Position  VARCHAR(30)  NOT NULL,
    Salary    DECIMAL(12,2) NOT NULL CHECK (Salary > 0),
    HireDate  DATE         NOT NULL,
    ManagerID INT NULL,
    FOREIGN KEY (ManagerID) REFERENCES EMPLOYEE(EmpID)
);

CREATE TABLE PRODUCT (
    ProdID    INT AUTO_INCREMENT PRIMARY KEY,
    ProdName  VARCHAR(100) NOT NULL,
    Category  VARCHAR(30)  NOT NULL,
    Price     DECIMAL(12,2) NOT NULL CHECK (Price >= 0),
    Stock     INT NOT NULL DEFAULT 0
);

CREATE TABLE SALEORDER (
    OrderID     INT AUTO_INCREMENT PRIMARY KEY,
    CustID      INT NOT NULL,
    EmpID       INT NOT NULL,
    OrderDate   DATE NOT NULL,
    Status      VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                CHECK (Status IN ('PENDING','COMPLETED','CANCELLED')),
    TotalAmount DECIMAL(12,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (CustID) REFERENCES CUSTOMER(CustID),
    FOREIGN KEY (EmpID)  REFERENCES EMPLOYEE(EmpID)
);

CREATE TABLE ORDER_DETAIL (
    OrderID   INT NOT NULL,
    ProdID    INT NOT NULL,
    Quantity  INT NOT NULL CHECK (Quantity > 0),
    UnitPrice DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (OrderID, ProdID),
    FOREIGN KEY (OrderID) REFERENCES SALEORDER(OrderID),
    FOREIGN KEY (ProdID)  REFERENCES PRODUCT(ProdID)
);

INSERT INTO CUSTOMER (CustName, City, Phone, Email, JoinDate) VALUES
('Nguyen Van An',  'Ha Noi',      '0901000001', 'an@mail.com',    '2024-01-10'),
('Tran Thi Binh',  'Ho Chi Minh', '0901000002', 'binh@mail.com',  '2024-02-15'),
('Le Van Cuong',   'Da Nang',     '0901000003', NULL,             '2024-03-20'),
('Pham Thi Dung',  'Ha Noi',      '0901000004', 'dung@mail.com',  '2024-05-05'),
('Hoang Van Em',   'Ho Chi Minh', '0901000005', NULL,             '2024-06-18'),
('Vu Thi Phuong',  'Hai Phong',   '0901000006', 'phuong@mail.com','2024-07-01');

INSERT INTO EMPLOYEE (EmpName, Position, Salary, HireDate, ManagerID) VALUES
('Do Minh Quan',   'Manager', 30000000, '2020-01-15', NULL),
('Nguyen Thu Ha',  'Sales',   15000000, '2021-03-01', 1),
('Tran Quoc Huy',  'Sales',   14000000, '2022-06-10', 1),
('Le Thi Lan',     'Sales',   13000000, '2023-02-20', 1),
('Pham Duc Minh',  'Sales',   10000000, '2024-01-08', 2);

INSERT INTO PRODUCT (ProdName, Category, Price, Stock) VALUES
('Laptop Dell',        'Electronics', 15000,  20),
('Mouse Logitech',     'Accessories',   300, 100),
('Keyboard Mechanical','Accessories',  1200,  50),
('Monitor 24 inch',    'Electronics',  4000,  30),
('Headphone',          'Accessories',   800,  40),
('USB 64GB',           'Accessories',   250, 200),
('Smartphone',         'Electronics',  9000,  25),
('Webcam',             'Accessories',   700,  15);

INSERT INTO SALEORDER (CustID, EmpID, OrderDate, Status, TotalAmount) VALUES
(1, 2, '2025-01-05', 'COMPLETED', 15600),   -- OrderID 1
(1, 2, '2025-02-10', 'COMPLETED',  9200),   -- 2
(2, 3, '2025-02-14', 'COMPLETED', 18800),   -- 3
(2, 3, '2025-03-03', 'CANCELLED', 15000),   -- 4
(3, 2, '2025-03-12', 'COMPLETED', 30300),   -- 5
(3, 4, '2025-04-01', 'PENDING',    1600),   -- 6
(4, 3, '2025-04-15', 'COMPLETED', 13000),   -- 7
(4, 4, '2025-05-02', 'COMPLETED',  4500),   -- 8
(5, 2, '2025-05-20', 'COMPLETED', 19000),   -- 9
(5, 3, '2025-06-08', 'PENDING',    9000),   -- 10
(1, 4, '2025-06-25', 'COMPLETED',  1700),   -- 11
(2, 2, '2025-07-07', 'COMPLETED', 24000);   -- 12

INSERT INTO ORDER_DETAIL (OrderID, ProdID, Quantity, UnitPrice) VALUES
(1,1,1,15000),(1,2,2,300),
(2,4,2,4000),(2,3,1,1200),
(3,7,2,9000),(3,5,1,800),
(4,1,1,15000),
(5,1,2,15000),(5,2,1,300),
(6,6,4,250),(6,2,2,300),
(7,7,1,9000),(7,4,1,4000),
(8,3,2,1200),(8,5,2,800),(8,6,2,250),
(9,1,1,15000),(9,4,1,4000),
(10,7,1,9000),
(11,5,1,800),(11,2,3,300),
(12,1,1,15000),(12,7,1,9000);
```

> **Quy ước:** `TotalAmount` của mỗi đơn = tổng `Quantity × UnitPrice` của các dòng chi tiết. Đơn vị tiền giữ nguyên là "đơn vị" để con số gọn.

### Dữ liệu mẫu (để anh tra nhanh khi đọc ví dụ)

**CUSTOMER**

| CustID | CustName | City | Phone | Email | JoinDate |
|---|---|---|---|---|---|
| 1 | Nguyen Van An | Ha Noi | 0901000001 | an@mail.com | 2024-01-10 |
| 2 | Tran Thi Binh | Ho Chi Minh | 0901000002 | binh@mail.com | 2024-02-15 |
| 3 | Le Van Cuong | Da Nang | 0901000003 | NULL | 2024-03-20 |
| 4 | Pham Thi Dung | Ha Noi | 0901000004 | dung@mail.com | 2024-05-05 |
| 5 | Hoang Van Em | Ho Chi Minh | 0901000005 | NULL | 2024-06-18 |
| 6 | Vu Thi Phuong | Hai Phong | 0901000006 | phuong@mail.com | 2024-07-01 |

**EMPLOYEE**

| EmpID | EmpName | Position | Salary | HireDate | ManagerID |
|---|---|---|---|---|---|
| 1 | Do Minh Quan | Manager | 30000000 | 2020-01-15 | NULL |
| 2 | Nguyen Thu Ha | Sales | 15000000 | 2021-03-01 | 1 |
| 3 | Tran Quoc Huy | Sales | 14000000 | 2022-06-10 | 1 |
| 4 | Le Thi Lan | Sales | 13000000 | 2023-02-20 | 1 |
| 5 | Pham Duc Minh | Sales | 10000000 | 2024-01-08 | 2 |

**PRODUCT**

| ProdID | ProdName | Category | Price | Stock |
|---|---|---|---|---|
| 1 | Laptop Dell | Electronics | 15000 | 20 |
| 2 | Mouse Logitech | Accessories | 300 | 100 |
| 3 | Keyboard Mechanical | Accessories | 1200 | 50 |
| 4 | Monitor 24 inch | Electronics | 4000 | 30 |
| 5 | Headphone | Accessories | 800 | 40 |
| 6 | USB 64GB | Accessories | 250 | 200 |
| 7 | Smartphone | Electronics | 9000 | 25 |
| 8 | Webcam | Accessories | 700 | 15 |

**SALEORDER**

| OrderID | CustID | EmpID | OrderDate | Status | TotalAmount |
|---|---|---|---|---|---|
| 1 | 1 | 2 | 2025-01-05 | COMPLETED | 15600 |
| 2 | 1 | 2 | 2025-02-10 | COMPLETED | 9200 |
| 3 | 2 | 3 | 2025-02-14 | COMPLETED | 18800 |
| 4 | 2 | 3 | 2025-03-03 | CANCELLED | 15000 |
| 5 | 3 | 2 | 2025-03-12 | COMPLETED | 30300 |
| 6 | 3 | 4 | 2025-04-01 | PENDING | 1600 |
| 7 | 4 | 3 | 2025-04-15 | COMPLETED | 13000 |
| 8 | 4 | 4 | 2025-05-02 | COMPLETED | 4500 |
| 9 | 5 | 2 | 2025-05-20 | COMPLETED | 19000 |
| 10 | 5 | 3 | 2025-06-08 | PENDING | 9000 |
| 11 | 1 | 4 | 2025-06-25 | COMPLETED | 1700 |
| 12 | 2 | 2 | 2025-07-07 | COMPLETED | 24000 |

**ORDER_DETAIL** (23 dòng)

| OrderID | ProdID | Quantity | UnitPrice |
|---|---|---|---|
| 1 | 1 | 1 | 15000 |
| 1 | 2 | 2 | 300 |
| 2 | 4 | 2 | 4000 |
| 2 | 3 | 1 | 1200 |
| 3 | 7 | 2 | 9000 |
| 3 | 5 | 1 | 800 |
| 4 | 1 | 1 | 15000 |
| 5 | 1 | 2 | 15000 |
| 5 | 2 | 1 | 300 |
| 6 | 6 | 4 | 250 |
| 6 | 2 | 2 | 300 |
| 7 | 7 | 1 | 9000 |
| 7 | 4 | 1 | 4000 |
| 8 | 3 | 2 | 1200 |
| 8 | 5 | 2 | 800 |
| 8 | 6 | 2 | 250 |
| 9 | 1 | 1 | 15000 |
| 9 | 4 | 1 | 4000 |
| 10 | 7 | 1 | 9000 |
| 11 | 5 | 1 | 800 |
| 11 | 2 | 3 | 300 |
| 12 | 1 | 1 | 15000 |
| 12 | 7 | 1 | 9000 |

**Các "cái bẫy" được cài sẵn trong dữ liệu** (để minh họa các tình huống khó):

| Cài đặt | Dùng để minh họa |
|---|---|
| Khách hàng 6 chưa có đơn nào | LEFT JOIN, NOT IN, NOT EXISTS |
| Nhân viên 5 chưa lập đơn nào | LEFT JOIN, NOT IN |
| Sản phẩm 8 (Webcam) chưa bán | LEFT JOIN, NOT IN |
| Khách 3 và 5 có `Email = NULL` | IS NULL, COALESCE |
| Đơn 4 CANCELLED, đơn 6 & 10 PENDING | WHERE theo Status, HAVING |
| Chỉ nhân viên 2 có doanh thu COMPLETED > 50000 (98100) | Ví dụ UPDATE lương ở Chương 8 |
| Nhân viên 1 có `ManagerID = NULL` | Self JOIN |

---

## CHƯƠNG 1: TỔNG QUAN VỀ SQL VÀ MYSQL

### 1.1. SQL là gì? MySQL là gì?

- **SQL** (Structured Query Language) là **ngôn ngữ** để nói chuyện với cơ sở dữ liệu: hỏi dữ liệu, thêm, sửa, xóa, tạo bảng.
- **MySQL** là một **phần mềm** (hệ quản trị cơ sở dữ liệu – DBMS) hiểu và thực thi SQL. Ngoài MySQL còn có SQL Server, PostgreSQL, Oracle... Cùng là SQL nhưng mỗi hệ có vài điểm khác nhau (xem Phụ lục C).

Ví von: SQL là tiếng Việt, MySQL là một người Việt cụ thể; các hệ khác là người nói giọng vùng miền khác.

### 1.2. Database, table, row, column

| Thuật ngữ | Nghĩa | Ví dụ trong `shop_db` |
|---|---|---|
| **Database** (CSDL) | Một "tủ hồ sơ" chứa nhiều bảng | `shop_db` |
| **Table** (bảng) | Một "ngăn" chứa dữ liệu cùng loại | `CUSTOMER` |
| **Column** (cột / trường) | Một thuộc tính | `CustName`, `City` |
| **Row** (dòng / bản ghi) | Một đối tượng cụ thể | Khách "Nguyen Van An" |

### 1.3. Primary key và Foreign key

- **Primary key (khóa chính):** cột (hoặc nhóm cột) **định danh duy nhất** mỗi dòng. Không trùng, không NULL. Ví dụ `CustID`.
- **Foreign key (khóa ngoại):** cột trong bảng này **tham chiếu tới khóa chính** của bảng khác, tạo mối liên kết. Ví dụ `SALEORDER.CustID` tham chiếu `CUSTOMER.CustID` → mỗi đơn hàng thuộc về một khách có thật.

Hệ quả quan trọng: không thể tạo đơn hàng cho khách hàng không tồn tại, và không thể xóa khách còn đơn hàng (MySQL sẽ báo lỗi, xem Chương 3).

### 1.4. Các kiểu dữ liệu thường gặp

| Kiểu | Dùng cho | Ví dụ | Ghi chú |
|---|---|---|---|
| `INT` | Số nguyên (±2,1 tỷ) | `Quantity` | Phổ biến nhất |
| `BIGINT` | Số nguyên rất lớn | ID cực lớn | 8 byte |
| `DECIMAL(p,s)` | Số thập phân **chính xác** | `DECIMAL(12,2)`: tổng 12 chữ số, 2 sau dấu phẩy | **Dùng cho tiền** |
| `FLOAT` | Số thực gần đúng | Tọa độ, đo lường | **Không dùng cho tiền** vì sai số |
| `CHAR(n)` | Chuỗi độ dài **cố định** | Mã quốc gia `CHAR(2)` | Thiếu thì độn khoảng trắng |
| `VARCHAR(n)` | Chuỗi **thay đổi**, tối đa n ký tự | Tên, email | Phổ biến nhất cho chữ |
| `TEXT` | Văn bản dài | Mô tả, bài viết | Không đặt DEFAULT được dễ dàng |
| `DATE` | Ngày `YYYY-MM-DD` | `2025-01-05` | |
| `DATETIME` | Ngày + giờ | `2025-01-05 14:30:00` | Không đổi theo múi giờ |
| `TIMESTAMP` | Ngày + giờ, theo UTC | Thời điểm ghi log | Phạm vi nhỏ hơn (đến năm 2038) |
| `BOOLEAN` | Đúng/sai | `IsActive` | Thực chất là `TINYINT(1)`: 1 = true, 0 = false |

### 1.5. NULL là gì?

**NULL = "không có giá trị / chưa biết"**, KHÔNG phải 0 và KHÔNG phải chuỗi rỗng.

| Giá trị | Nghĩa |
|---|---|
| `0` | Có giá trị, bằng không |
| `''` (rỗng) | Có giá trị, là chuỗi không ký tự |
| `NULL` | **Không biết / chưa có** |

Hai quy tắc phải thuộc:

```sql
SELECT 1 = NULL;        -- kết quả NULL (không phải TRUE/FALSE)
SELECT NULL = NULL;     -- kết quả NULL
SELECT 5 + NULL;        -- kết quả NULL (NULL "lây" sang phép tính)
```

1. Muốn kiểm tra NULL phải dùng `IS NULL` / `IS NOT NULL`, **không bao giờ** dùng `= NULL`.
2. Mọi phép tính với NULL cho ra NULL; các hàm tổng hợp (`SUM`, `AVG`, `COUNT(cột)`) **bỏ qua** NULL.

Ví dụ: khách 3 có `Email = NULL` nghĩa là "chưa có email", khác với `Email = ''`.

### 1.6. Các nhóm lệnh SQL

| Nhóm | Tên đầy đủ | Làm gì | Lệnh |
|---|---|---|---|
| **DDL** | Data Definition Language | Định nghĩa **cấu trúc** | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME` |
| **DML** | Data Manipulation Language | Thao tác **dữ liệu** | `INSERT`, `UPDATE`, `DELETE` |
| **DQL** | Data Query Language | **Truy vấn** dữ liệu | `SELECT` |
| **DCL** | Data Control Language | Phân quyền | `GRANT`, `REVOKE` |
| **TCL** | Transaction Control Language | Giao dịch | `COMMIT`, `ROLLBACK`, `START TRANSACTION` |

### 1.7. Quy tắc viết câu lệnh SQL

1. Kết thúc câu lệnh bằng dấu chấm phẩy `;`.
2. Từ khóa **không phân biệt hoa/thường** (`select` = `SELECT`), nhưng nên **viết HOA từ khóa** cho dễ đọc.
3. Tên bảng/cột: trên Linux MySQL **phân biệt hoa thường tên bảng**, trên Windows thì không. Quy ước: giữ đúng như lúc tạo.
4. Chuỗi và ngày đặt trong **dấu nháy đơn** `'...'`: `'Ha Noi'`, `'2025-01-05'`.
5. Chú thích: `-- một dòng` hoặc `/* nhiều dòng */`.
6. Xuống dòng, thụt lề thoải mái; mỗi mệnh đề (`FROM`, `WHERE`...) nên một dòng.

```sql
-- Đây là chú thích
SELECT CustName, City      -- lấy 2 cột
FROM CUSTOMER              -- từ bảng khách hàng
WHERE City = 'Ha Noi';     -- chỉ khách ở Hà Nội
```

> **So sánh khác biệt:** SQL Server dùng `[ten cot]` hoặc `"ten cot"`, MySQL dùng dấu **backtick** `` `ten cot` `` khi tên trùng từ khóa. PostgreSQL dùng `"ten cot"`.

---

## CHƯƠNG 2: CREATE DATABASE VÀ CREATE TABLE

> Anh đã chạy script ở phần Chuẩn bị. Chương này giải thích **từng lệnh trong script** và các lệnh định nghĩa khác. Các ví dụ dùng thêm bảng tạm `student_demo` để không làm hỏng `shop_db`.

### 2.1. CREATE DATABASE, USE, SHOW DATABASES

**1. Công dụng:** Tạo CSDL mới; chọn CSDL để làm việc.

**2. Cú pháp:**
```sql
CREATE DATABASE [IF NOT EXISTS] ten_csdl [CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci];
USE ten_csdl;
SHOW DATABASES;
DROP DATABASE [IF EXISTS] ten_csdl;
```

**3. Ví dụ:**
```sql
CREATE DATABASE IF NOT EXISTS school_demo CHARACTER SET utf8mb4;
USE school_demo;
```

**4. Giải thích:**
- `IF NOT EXISTS`: không báo lỗi nếu CSDL đã tồn tại.
- `CHARACTER SET utf8mb4`: lưu được tiếng Việt có dấu và emoji. **Luôn dùng utf8mb4**, đừng dùng `utf8` (thực chất chỉ 3 byte của MySQL).
- `USE`: từ lúc này mọi lệnh tác động lên CSDL này. Quên `USE` là nguyên nhân phổ biến của lỗi *"No database selected"*.

**Lỗi thường gặp:** `ERROR 1046: No database selected` → thêm `USE ten_csdl;` hoặc viết `ten_csdl.ten_bang`.

### 2.2. CREATE TABLE

**1. Công dụng:** Tạo bảng mới.

**2. Cú pháp tổng quát:**
```sql
CREATE TABLE ten_bang (
    ten_cot  KIEU_DU_LIEU  [rang_buoc ...],
    ...
    [rang_buoc_cap_bang ...]
);
```

**3. Ví dụ cơ bản:**
```sql
CREATE TABLE student_demo (
    StudentID INT,
    FullName  VARCHAR(100),
    Gpa       DECIMAL(3,2)
);
```
Bảng này **chưa có ràng buộc nào** → có thể trùng ID, có thể NULL. Thực tế nên có ràng buộc, xem tiếp.

**4. Ví dụ thực tế (có đủ ràng buộc):**
```sql
DROP TABLE IF EXISTS student_demo;
CREATE TABLE student_demo (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,           -- (1)
    FullName  VARCHAR(100) NOT NULL,                    -- (2)
    Email     VARCHAR(100) UNIQUE,                      -- (3)
    Gpa       DECIMAL(3,2) NOT NULL DEFAULT 0
              CHECK (Gpa BETWEEN 0 AND 4),              -- (4)
    Status    VARCHAR(20) DEFAULT 'STUDYING',           -- (5)
    BirthDate DATE
);
```

**5. Giải thích từng dòng:**

| Dòng | Giải thích |
|---|---|
| (1) | `PRIMARY KEY`: khóa chính (duy nhất, không NULL). `AUTO_INCREMENT`: MySQL tự tăng 1, 2, 3... khi thêm dòng, anh không cần tự điền |
| (2) | `NOT NULL`: bắt buộc phải có giá trị |
| (3) | `UNIQUE`: không được trùng, nhưng **cho phép NULL** (và nhiều NULL) |
| (4) | `DEFAULT 0`: nếu không điền thì bằng 0. `CHECK`: giá trị phải thỏa điều kiện, MySQL 8.0.16+ mới thực sự kiểm tra |
| (5) | `DEFAULT 'STUDYING'`: giá trị mặc định kiểu chuỗi |

### 2.3. Các ràng buộc chi tiết

| Ràng buộc | Công dụng | Ví dụ | Vi phạm thì sao |
|---|---|---|---|
| `PRIMARY KEY` | Định danh dòng | `CustID INT PRIMARY KEY` | Lỗi 1062 Duplicate entry |
| `FOREIGN KEY` | Liên kết bảng | `FOREIGN KEY (CustID) REFERENCES CUSTOMER(CustID)` | Lỗi 1452 |
| `NOT NULL` | Cấm NULL | `CustName VARCHAR(100) NOT NULL` | Lỗi 1048 |
| `UNIQUE` | Cấm trùng | `Phone VARCHAR(15) UNIQUE` | Lỗi 1062 |
| `DEFAULT` | Giá trị mặc định | `Stock INT DEFAULT 0` | (không lỗi) |
| `CHECK` | Điều kiện tùy ý | `CHECK (Price >= 0)` | Lỗi 3819 |
| `AUTO_INCREMENT` | Tự tăng | `OrderID INT AUTO_INCREMENT` | (không lỗi) |

**Đặt tên ràng buộc** (để dễ xóa/sửa sau này):
```sql
CREATE TABLE product_demo (
    ProdID INT AUTO_INCREMENT,
    Price  DECIMAL(12,2) NOT NULL,
    CONSTRAINT pk_product_demo PRIMARY KEY (ProdID),
    CONSTRAINT ck_price_demo   CHECK (Price >= 0)
);
```

### 2.4. Khóa chính gồm nhiều cột (composite key)

Dùng khi **một cột không đủ để định danh**. Trong `ORDER_DETAIL`, một đơn có nhiều sản phẩm, một sản phẩm nằm trong nhiều đơn; chỉ cặp `(OrderID, ProdID)` mới là duy nhất:

```sql
CREATE TABLE ORDER_DETAIL (
    OrderID   INT NOT NULL,
    ProdID    INT NOT NULL,
    Quantity  INT NOT NULL,
    UnitPrice DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (OrderID, ProdID)        -- khóa chính 2 cột
);
```
Hệ quả: **không thể** có hai dòng cùng `(OrderID=1, ProdID=1)`. Muốn mua thêm cùng sản phẩm trong đơn thì phải `UPDATE Quantity`.

### 2.5. FOREIGN KEY

```sql
CREATE TABLE SALEORDER (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    CustID  INT NOT NULL,
    FOREIGN KEY (CustID) REFERENCES CUSTOMER(CustID)
        ON DELETE RESTRICT      -- mặc định: cấm xóa khách còn đơn
        ON UPDATE CASCADE       -- đổi CustID bên CUSTOMER thì bên này đổi theo
);
```

| Tùy chọn `ON DELETE` | Ý nghĩa |
|---|---|
| `RESTRICT` / `NO ACTION` | Cấm xóa dòng cha nếu còn dòng con (mặc định) |
| `CASCADE` | Xóa dòng cha thì **xóa luôn** dòng con (nguy hiểm, cân nhắc!) |
| `SET NULL` | Gán FK = NULL (cột phải cho phép NULL) |

**Thứ tự tạo bảng:** bảng cha trước (CUSTOMER, EMPLOYEE, PRODUCT), bảng con sau (SALEORDER, ORDER_DETAIL). **Thứ tự xóa** thì ngược lại. Sai thứ tự gặp lỗi 1215/3730.

### 2.6. Chọn kiểu dữ liệu: quy tắc nhanh

| Dữ liệu | Nên chọn | Tránh |
|---|---|---|
| Khóa chính tự tăng | `INT AUTO_INCREMENT` | |
| Tiền | `DECIMAL(12,2)` | `FLOAT`, `DOUBLE` |
| Số điện thoại | `VARCHAR(15)` | `INT` (mất số 0 đầu, và không tính toán với nó) |
| Tên, email | `VARCHAR(100)` | `TEXT` |
| Ngày sinh, ngày đặt hàng | `DATE` | `VARCHAR` |
| Thời điểm xảy ra | `DATETIME` | |
| Đúng/sai | `BOOLEAN` | Chuỗi `'yes'/'no'` |

### 2.7. ALTER TABLE

**Công dụng:** Sửa cấu trúc bảng đã có.

```sql
-- Thêm cột
ALTER TABLE student_demo ADD COLUMN Phone VARCHAR(15);
ALTER TABLE student_demo ADD COLUMN Class VARCHAR(10) NOT NULL DEFAULT 'N/A' AFTER FullName;

-- Sửa kiểu dữ liệu / ràng buộc của cột
ALTER TABLE student_demo MODIFY COLUMN Phone VARCHAR(20) NOT NULL DEFAULT '';

-- Đổi tên cột (MySQL 8.0)
ALTER TABLE student_demo RENAME COLUMN Phone TO Mobile;

-- Xóa cột
ALTER TABLE student_demo DROP COLUMN Mobile;

-- Thêm / xóa ràng buộc
ALTER TABLE student_demo ADD CONSTRAINT uq_fullname UNIQUE (FullName);
ALTER TABLE student_demo DROP INDEX uq_fullname;          -- xóa UNIQUE trong MySQL

-- Thêm khóa ngoại
ALTER TABLE SALEORDER
  ADD CONSTRAINT fk_order_cust FOREIGN KEY (CustID) REFERENCES CUSTOMER(CustID);
ALTER TABLE SALEORDER DROP FOREIGN KEY fk_order_cust;
```

**Lỗi thường gặp:**
- `MODIFY` mà quên giữ lại `NOT NULL`/`DEFAULT` → ràng buộc cũ bị **mất** (MODIFY ghi đè toàn bộ định nghĩa cột).
- Thêm cột `NOT NULL` vào bảng đã có dữ liệu mà không có `DEFAULT` → lỗi hoặc dữ liệu cũ bị gán giá trị rỗng.
- Xóa UNIQUE bằng `DROP CONSTRAINT` kiểu PostgreSQL: MySQL cần `DROP INDEX`.

### 2.8. DROP TABLE, TRUNCATE TABLE, RENAME TABLE

| Lệnh | Tác dụng | Xóa dữ liệu? | Xóa cấu trúc? | Hoàn tác (ROLLBACK)? |
|---|---|---|---|---|
| `DELETE FROM t` | Xóa từng dòng (có thể kèm WHERE) | Có | Không | Có (nếu trong transaction) |
| `TRUNCATE TABLE t` | Xóa **toàn bộ** dòng, reset AUTO_INCREMENT | Có | Không | **Không** |
| `DROP TABLE t` | Xóa cả bảng | Có | **Có** | **Không** |

```sql
TRUNCATE TABLE student_demo;                 -- sạch dữ liệu, giữ bảng
DROP TABLE IF EXISTS student_demo;           -- bỏ bảng
RENAME TABLE student_demo TO students_demo;  -- đổi tên bảng
ALTER TABLE students_demo RENAME TO student_demo;  -- cách khác
```

**Lỗi thường gặp:** `TRUNCATE` bảng đang được tham chiếu bởi khóa ngoại → lỗi 1701. Cách xử lý: xóa bảng con trước, hoặc `SET FOREIGN_KEY_CHECKS = 0;` (chỉ dùng khi biết rõ mình làm gì, nhớ bật lại `= 1`).

### 2.9. DESCRIBE và SHOW

```sql
SHOW TABLES;                    -- danh sách bảng trong CSDL hiện tại
DESCRIBE CUSTOMER;              -- hoặc DESC CUSTOMER; xem cấu trúc cột
SHOW CREATE TABLE CUSTOMER;     -- xem lệnh CREATE TABLE đầy đủ
SHOW COLUMNS FROM CUSTOMER;     -- giống DESCRIBE
```

Kết quả `DESCRIBE CUSTOMER`:

| Field | Type | Null | Key | Default | Extra |
|---|---|---|---|---|---|
| CustID | int | NO | PRI | NULL | auto_increment |
| CustName | varchar(100) | NO | | NULL | |
| City | varchar(50) | NO | | NULL | |
| Phone | varchar(15) | NO | UNI | NULL | |
| Email | varchar(100) | YES | | NULL | |
| JoinDate | date | NO | | NULL | |

Cột `Key`: `PRI` = khóa chính, `UNI` = unique, `MUL` = có thể trùng (thường là khóa ngoại).

### 2.10. Bài tập tự luyện Chương 2

1. Tạo bảng `SUPPLIER` gồm `SupplierID` (khóa chính tự tăng), `SupplierName` (bắt buộc), `Phone` (duy nhất), `Country` (mặc định `'Vietnam'`).
2. Thêm khóa ngoại: thêm cột `SupplierID` vào `PRODUCT` và liên kết với `SUPPLIER`.
3. Tạo bảng `ENROLLMENT(StudentID, CourseID, Grade)` khóa chính gồm 2 cột, `Grade` từ 0 đến 10.

<details><summary>Đáp án</summary>

```sql
-- 1
CREATE TABLE SUPPLIER (
    SupplierID   INT AUTO_INCREMENT PRIMARY KEY,
    SupplierName VARCHAR(100) NOT NULL,
    Phone        VARCHAR(15) UNIQUE,
    Country      VARCHAR(50) DEFAULT 'Vietnam'
);
-- 2
ALTER TABLE PRODUCT ADD COLUMN SupplierID INT NULL;
ALTER TABLE PRODUCT
  ADD CONSTRAINT fk_prod_supplier FOREIGN KEY (SupplierID) REFERENCES SUPPLIER(SupplierID);
-- 3
CREATE TABLE ENROLLMENT (
    StudentID INT NOT NULL,
    CourseID  INT NOT NULL,
    Grade     DECIMAL(4,2) CHECK (Grade BETWEEN 0 AND 10),
    PRIMARY KEY (StudentID, CourseID)
);
```
Lưu ý ở câu 2: cột mới phải cho phép `NULL`, vì các sản phẩm hiện có chưa có nhà cung cấp. Nếu để `NOT NULL` thì dữ liệu cũ vi phạm.
</details>

> Sau bài này nếu anh đã thêm `SupplierID` vào PRODUCT, hãy `ALTER TABLE PRODUCT DROP FOREIGN KEY fk_prod_supplier; ALTER TABLE PRODUCT DROP COLUMN SupplierID; DROP TABLE SUPPLIER;` để `shop_db` trở lại đúng như tài liệu.

---

### 2.11. CHI TIẾT TỪNG LỆNH CỦA CHƯƠNG 2 (mẫu 10 mục + bài tự luyện)

> Để không làm hỏng `shop_db`, các ví dụ dưới đây dùng bảng có tiền tố `DEMO_`. Cuối mục có lệnh dọn dẹp.
> Mỗi lệnh: **1.Công dụng · 2.Cú pháp · 3.Ví dụ cơ bản · 4.Ví dụ thực tế + kết quả · 5.Giải thích · 6.Cách dùng khác · 7.Lỗi thường gặp · 8.Khi nào dùng · 9.Bài tự luyện.**

#### 2.11.1. CREATE DATABASE
1. **Công dụng:** tạo một CSDL (một "tủ hồ sơ") mới.
2. **Cú pháp:** `CREATE DATABASE [IF NOT EXISTS] ten [CHARACTER SET utf8mb4 [COLLATE utf8mb4_unicode_ci]];`
3. **Cơ bản:** `CREATE DATABASE demo_db;`
4. **Thực tế:**
```sql
CREATE DATABASE IF NOT EXISTS demo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
```
→ danh sách có thêm dòng `demo_db`.
5. **Giải thích:** `IF NOT EXISTS` tránh lỗi khi đã tồn tại; `utf8mb4` lưu được tiếng Việt có dấu; `COLLATE` quy định cách so sánh/sắp xếp chuỗi (`_ci` = không phân biệt hoa/thường).
6. **Khác:** `CREATE SCHEMA` là từ đồng nghĩa; `SHOW CREATE DATABASE demo_db;` xem lại cách tạo.
7. **Lỗi:** `ERROR 1007 Can't create database; database exists` → thêm `IF NOT EXISTS`. Thiếu quyền → lỗi 1044.
8. **Khi nào dùng:** bắt đầu một dự án/ứng dụng mới.
9. **Bài tự luyện:** tạo CSDL `library_demo` hỗ trợ tiếng Việt, rồi chuyển sang dùng nó.
   *Đáp án:* `CREATE DATABASE library_demo CHARACTER SET utf8mb4; USE library_demo;`

#### 2.11.2. USE
1. **Công dụng:** chọn CSDL mặc định cho các lệnh sau đó.
2. **Cú pháp:** `USE ten_csdl;`
3. **Cơ bản:** `USE shop_db;`
4. **Thực tế:** `USE shop_db; SELECT DATABASE();` → `shop_db`.
5. **Giải thích:** `SELECT DATABASE()` cho biết CSDL đang chọn (NULL nếu chưa chọn).
6. **Khác:** không `USE` thì viết tên đầy đủ: `SELECT * FROM shop_db.CUSTOMER;`.
7. **Lỗi:** `ERROR 1046: No database selected` → thêm `USE`. Chuyển sang CSDL khác mà quên `USE` → thao tác nhầm CSDL.
8. **Khi nào dùng:** đầu mỗi phiên làm việc/script.
9. **Bài tự luyện:** viết truy vấn đếm khách hàng mà **không** dùng `USE`. *Đáp án:* `SELECT COUNT(*) FROM shop_db.CUSTOMER;` → 6.

#### 2.11.3. CREATE TABLE
1. **Công dụng:** tạo bảng.
2. **Cú pháp:** `CREATE TABLE [IF NOT EXISTS] ten (cot kieu [rang_buoc], ..., [rang_buoc_bang]);`
3. **Cơ bản:** `CREATE TABLE DEMO_CLASS (ClassID INT PRIMARY KEY, ClassName VARCHAR(50) NOT NULL);`
4. **Thực tế (bảng có đủ ràng buộc):**
```sql
CREATE TABLE DEMO_STUDENT (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,
    FullName  VARCHAR(100) NOT NULL,
    Email     VARCHAR(100) UNIQUE,
    ClassID   INT,
    Gpa       DECIMAL(3,2) NOT NULL DEFAULT 0 CHECK (Gpa BETWEEN 0 AND 4),
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ClassID) REFERENCES DEMO_CLASS(ClassID)
);
DESCRIBE DEMO_STUDENT;
```
→ bảng 6 cột; `StudentID` là `PRI`, `Email` là `UNI`, `ClassID` là `MUL`.
5. **Giải thích:** mỗi dòng cột = *tên + kiểu + ràng buộc*; ràng buộc cấp bảng (`FOREIGN KEY`) đặt cuối; bảng cha (`DEMO_CLASS`) phải tạo **trước**.
6. **Khác:** `CREATE TABLE b LIKE a;` (sao chép cấu trúc); `CREATE TABLE b AS SELECT ...`; `CREATE TEMPORARY TABLE` (tồn tại trong phiên).
7. **Lỗi:** 1050 *Table already exists* → `IF NOT EXISTS`; 1215/3780 không tạo được khóa ngoại (bảng cha chưa có, hoặc kiểu cột khác nhau); quên dấu phẩy giữa các cột.
8. **Khi nào dùng:** thiết kế cấu trúc lưu một loại dữ liệu mới.
9. **Bài tự luyện:** tạo `DEMO_BOOK(BookID tự tăng, Title bắt buộc, Price ≥ 0, Pages mặc định 100).`
   *Đáp án:*
```sql
CREATE TABLE DEMO_BOOK (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    Title  VARCHAR(200) NOT NULL,
    Price  DECIMAL(10,2) CHECK (Price >= 0),
    Pages  INT DEFAULT 100
);
```

#### 2.11.4. PRIMARY KEY
1. **Công dụng:** định danh duy nhất mỗi dòng (không trùng, không NULL); mỗi bảng chỉ có **một** khóa chính.
2. **Cú pháp:** `cot kieu PRIMARY KEY` hoặc `PRIMARY KEY (cot1 [, cot2])` hoặc `CONSTRAINT ten PRIMARY KEY (...)`.
3. **Cơ bản:** `ClassID INT PRIMARY KEY`
4. **Thực tế:**
```sql
INSERT INTO DEMO_CLASS VALUES (1, 'IT-K1'), (2, 'IT-K2');
INSERT INTO DEMO_CLASS VALUES (1, 'DUP');     -- ERROR 1062: Duplicate entry '1' for key 'PRIMARY'
INSERT INTO DEMO_CLASS VALUES (NULL, 'X');    -- ERROR 1048: Column 'ClassID' cannot be null
```
5. **Giải thích:** khóa chính vừa `UNIQUE` vừa `NOT NULL`, tự động có chỉ mục (tra cứu nhanh).
6. **Khác:** khóa chính gồm nhiều cột (mục 2.4); thêm sau: `ALTER TABLE t ADD PRIMARY KEY (id);`.
7. **Lỗi:** hai khóa chính trong một bảng (1068 Multiple primary key); dùng cột có thể trùng (như tên) làm khóa chính.
8. **Khi nào dùng:** **mọi bảng** nên có khóa chính.
9. **Bài tự luyện:** vì sao `Phone` không nên là khóa chính của `CUSTOMER`? *Đáp án:* số điện thoại có thể đổi/thiếu/dùng chung; khóa chính nên **ổn định, không ý nghĩa nghiệp vụ** (ví dụ ID tự tăng).

#### 2.11.5. FOREIGN KEY
1. **Công dụng:** ràng buộc giá trị một cột phải **tồn tại** trong khóa chính của bảng khác.
2. **Cú pháp:** `FOREIGN KEY (cot) REFERENCES bang_cha(cot_cha) [ON DELETE ...] [ON UPDATE ...]`
3. **Cơ bản:** `FOREIGN KEY (ClassID) REFERENCES DEMO_CLASS(ClassID)`
4. **Thực tế:**
```sql
INSERT INTO DEMO_STUDENT (FullName, ClassID) VALUES ('An', 1);     -- OK
INSERT INTO DEMO_STUDENT (FullName, ClassID) VALUES ('Binh', 99);  -- ERROR 1452: lớp 99 không tồn tại
INSERT INTO DEMO_STUDENT (FullName, ClassID) VALUES ('Cuong', NULL); -- OK: NULL được phép (chưa xếp lớp)
DELETE FROM DEMO_CLASS WHERE ClassID = 1;                          -- ERROR 1451: còn sinh viên thuộc lớp 1
```
5. **Giải thích:** bảo đảm toàn vẹn dữ liệu: không có "con mồ côi". Kiểu và độ dài hai cột phải **giống nhau**.
6. **Khác:** `ON DELETE CASCADE` (xóa cha → xóa con), `SET NULL`, `RESTRICT` (mặc định); `ON UPDATE CASCADE`.
7. **Lỗi:** 1452 (chèn giá trị không có ở cha); 1451 (xóa cha còn con); 3780 (kiểu cột không khớp).
8. **Khi nào dùng:** mọi quan hệ 1–n (khách–đơn, lớp–sinh viên).
9. **Bài tự luyện:** `DEMO_STUDENT` hiện tại làm gì khi xóa lớp mà có sinh viên, và sửa để sinh viên tự chuyển về "chưa xếp lớp"? *Đáp án:* báo lỗi 1451; dùng `ON DELETE SET NULL` (cột `ClassID` phải cho phép NULL).

#### 2.11.6. NOT NULL
1. **Công dụng:** cấm giá trị NULL. 2. **Cú pháp:** `cot kieu NOT NULL`
3. **Cơ bản:** `FullName VARCHAR(100) NOT NULL`
4. **Thực tế:** `INSERT INTO DEMO_STUDENT (Email) VALUES ('x@mail.com');` → `ERROR 1364: Field 'FullName' doesn't have a default value`.
5. **Giải thích:** không điền cột `NOT NULL` và không có `DEFAULT` → lỗi (chế độ strict, mặc định của MySQL 8).
6. **Khác:** `ALTER TABLE t MODIFY col VARCHAR(100) NOT NULL;`; kết hợp `NOT NULL DEFAULT ''`.
7. **Lỗi:** thêm `NOT NULL` cho cột đã có dòng NULL → lỗi 1138; thay trước bằng `UPDATE ... SET col = '' WHERE col IS NULL`.
8. **Khi nào dùng:** thông tin bắt buộc phải có (tên, ngày, số tiền).
9. **Bài tự luyện:** `Email` của `CUSTOMER` cho phép NULL. Vì sao hợp lý? *Đáp án:* không phải khách nào cũng có email; bắt buộc sẽ ép nhập dữ liệu giả.

#### 2.11.7. UNIQUE
1. **Công dụng:** cấm giá trị trùng (nhưng **cho phép nhiều NULL**).
2. **Cú pháp:** `cot kieu UNIQUE` hoặc `UNIQUE (cot1, cot2)` hoặc `CONSTRAINT ten UNIQUE (cot)`.
3. **Cơ bản:** `Email VARCHAR(100) UNIQUE`
4. **Thực tế:**
```sql
INSERT INTO DEMO_STUDENT (FullName, Email) VALUES ('Dung', 'dung@mail.com');   -- OK
INSERT INTO DEMO_STUDENT (FullName, Email) VALUES ('Em',   'dung@mail.com');   -- ERROR 1062
INSERT INTO DEMO_STUDENT (FullName, Email) VALUES ('G1', NULL), ('G2', NULL);  -- OK (hai NULL)
```
5. **Giải thích:** NULL "không biết" nên hai NULL không bị coi là trùng.
6. **Khác:** UNIQUE nhiều cột: `UNIQUE (ClassID, FullName)` cấm trùng **tổ hợp**; xóa: `ALTER TABLE t DROP INDEX ten;`.
7. **Lỗi:** 1062 *Duplicate entry*; nhầm UNIQUE với PRIMARY KEY (bảng chỉ có một PK nhưng nhiều UNIQUE).
8. **Khi nào dùng:** email, số điện thoại, mã sinh viên: không trùng nhưng không phải khóa chính.
9. **Bài tự luyện:** chỉ cho phép một sinh viên cùng tên trong một lớp. *Đáp án:* `ALTER TABLE DEMO_STUDENT ADD CONSTRAINT uq_class_name UNIQUE (ClassID, FullName);`

#### 2.11.8. DEFAULT
1. **Công dụng:** giá trị tự điền khi không cung cấp. 2. **Cú pháp:** `cot kieu DEFAULT gia_tri`
3. **Cơ bản:** `Pages INT DEFAULT 100`
4. **Thực tế:**
```sql
INSERT INTO DEMO_STUDENT (FullName) VALUES ('Hoa');
SELECT FullName, Gpa, CreatedAt FROM DEMO_STUDENT WHERE FullName = 'Hoa';
```
→ `Hoa | 0.00 | <thời điểm hiện tại>` (nhờ `DEFAULT 0` và `DEFAULT CURRENT_TIMESTAMP`).
5. **Giải thích:** chỉ áp dụng khi **không liệt kê cột** (hoặc dùng từ khóa `DEFAULT`); ghi `NULL` rõ ràng vẫn là NULL (nếu cột cho phép).
6. **Khác:** `INSERT ... VALUES ('Hoa', DEFAULT)`; `ALTER TABLE t ALTER COLUMN col SET DEFAULT 5;`.
7. **Lỗi:** `DEFAULT` kiểu `TEXT/BLOB` không dùng giá trị thường (cần ngoặc đơn dạng biểu thức); đặt default sai kiểu.
8. **Khi nào dùng:** trạng thái ban đầu (`'PENDING'`), thời điểm tạo, số 0.
9. **Bài tự luyện:** thêm cột `IsActive` kiểu BOOLEAN mặc định đang hoạt động. *Đáp án:* `ALTER TABLE DEMO_STUDENT ADD COLUMN IsActive BOOLEAN NOT NULL DEFAULT TRUE;`

#### 2.11.9. CHECK
1. **Công dụng:** ràng buộc giá trị phải thỏa một điều kiện (MySQL ≥ 8.0.16 thực sự kiểm tra).
2. **Cú pháp:** `CHECK (dieu_kien)` hoặc `CONSTRAINT ten CHECK (dieu_kien)`
3. **Cơ bản:** `Price DECIMAL(10,2) CHECK (Price >= 0)`
4. **Thực tế:**
```sql
INSERT INTO DEMO_STUDENT (FullName, Gpa) VALUES ('Khoa', 3.5);   -- OK
INSERT INTO DEMO_STUDENT (FullName, Gpa) VALUES ('Lam', 5.0);    -- ERROR 3819: Check constraint violated
```
5. **Giải thích:** điều kiện đánh giá cho **từng dòng** khi `INSERT`/`UPDATE`.
6. **Khác:** CHECK nhiều cột: `CHECK (EndDate >= StartDate)`; thêm sau: `ALTER TABLE t ADD CONSTRAINT ck CHECK (...)`.
7. **Lỗi:** dùng MySQL 5.7 (bị bỏ qua mà không báo lỗi); CHECK không tham chiếu bảng khác.
8. **Khi nào dùng:** miền giá trị cố định (điểm 0–10, số lượng > 0, trạng thái trong danh sách).
9. **Bài tự luyện:** chỉ cho `Position` thuộc `'Manager'`, `'Sales'`. *Đáp án:* `ALTER TABLE EMPLOYEE ADD CONSTRAINT ck_pos CHECK (Position IN ('Manager','Sales'));` (với dữ liệu hiện có đều hợp lệ; chức vụ `Senior Sales` ở bài 8.2 sẽ vi phạm).

#### 2.11.10. AUTO_INCREMENT
1. **Công dụng:** MySQL tự đánh số tăng dần. 2. **Cú pháp:** `cot INT AUTO_INCREMENT PRIMARY KEY` (cột phải là khóa/chỉ mục).
3. **Cơ bản:** `StudentID INT AUTO_INCREMENT PRIMARY KEY`
4. **Thực tế:**
```sql
INSERT INTO DEMO_CLASS (ClassID, ClassName) VALUES (10, 'A');
CREATE TABLE DEMO_LOG (LogID INT AUTO_INCREMENT PRIMARY KEY, Msg VARCHAR(50));
INSERT INTO DEMO_LOG (Msg) VALUES ('a'), ('b'), ('c');   -- LogID = 1, 2, 3
DELETE FROM DEMO_LOG WHERE LogID = 3;
INSERT INTO DEMO_LOG (Msg) VALUES ('d');                 -- LogID = 4 (không dùng lại 3)
SELECT LAST_INSERT_ID();                                 -- 4
```
5. **Giải thích:** bộ đếm chỉ tăng, **không** tái sử dụng số đã xóa; `LAST_INSERT_ID()` cho ID vừa chèn trong phiên hiện tại.
6. **Khác:** `ALTER TABLE t AUTO_INCREMENT = 100;` đặt số bắt đầu; `TRUNCATE` đưa bộ đếm về 1.
7. **Lỗi:** tự điền giá trị cho cột này gây trùng; dùng `AUTO_INCREMENT` cho cột không phải khóa (1075).
8. **Khi nào dùng:** khóa chính nhân tạo.
9. **Bài tự luyện:** sau `TRUNCATE TABLE DEMO_LOG;` chèn một dòng, `LogID` bằng bao nhiêu? *Đáp án:* `1`.

#### 2.11.11. Khóa chính nhiều cột
1. **Công dụng:** định danh dòng bằng **tổ hợp** nhiều cột. 2. **Cú pháp:** `PRIMARY KEY (cot1, cot2)`
3. **Cơ bản:** `PRIMARY KEY (OrderID, ProdID)`
4. **Thực tế:**
```sql
CREATE TABLE DEMO_ENROLL (
    StudentID INT, CourseID INT, Grade DECIMAL(4,2),
    PRIMARY KEY (StudentID, CourseID)
);
INSERT INTO DEMO_ENROLL VALUES (1, 101, 8.5), (1, 102, 7.0), (2, 101, 9.0);   -- OK
INSERT INTO DEMO_ENROLL VALUES (1, 101, 6.0);   -- ERROR 1062 (cặp (1,101) đã có)
```
5. **Giải thích:** từng cột có thể lặp, nhưng **cặp** không được lặp; mọi cột trong khóa là `NOT NULL`.
6. **Khác:** bảng trung gian của quan hệ nhiều-nhiều (như `ORDER_DETAIL`).
7. **Lỗi:** tham chiếu bằng khóa ngoại phải liệt kê **đủ cặp** cột.
8. **Khi nào dùng:** bảng nối nhiều-nhiều.
9. **Bài tự luyện:** viết lệnh thêm điểm mới cho sinh viên 1 môn 101 nếu đã có thì cập nhật. *Đáp án:* `INSERT INTO DEMO_ENROLL VALUES (1,101,6.0) ON DUPLICATE KEY UPDATE Grade = VALUES(Grade);`

#### 2.11.12. ALTER TABLE
1. **Công dụng:** sửa cấu trúc bảng đã có. 2. **Cú pháp:** `ALTER TABLE t ADD/MODIFY/RENAME/DROP ...` (mục 2.7)
3. **Cơ bản:** `ALTER TABLE DEMO_BOOK ADD COLUMN Author VARCHAR(100);`
4. **Thực tế:**
```sql
ALTER TABLE DEMO_BOOK ADD COLUMN Author VARCHAR(100) NOT NULL DEFAULT 'N/A' AFTER Title;
ALTER TABLE DEMO_BOOK MODIFY COLUMN Title VARCHAR(255) NOT NULL;
ALTER TABLE DEMO_BOOK RENAME COLUMN Pages TO PageCount;
ALTER TABLE DEMO_BOOK DROP COLUMN Author;
DESCRIBE DEMO_BOOK;
```
5. **Giải thích:** `AFTER Title` chọn vị trí cột; `MODIFY` **ghi đè toàn bộ** định nghĩa cột (phải nhắc lại `NOT NULL`...); có thể gộp nhiều thay đổi, ngăn cách bằng dấu phẩy.
6. **Khác:** `ADD INDEX`, `ADD CONSTRAINT`, `DROP FOREIGN KEY`, `ENGINE=InnoDB`.
7. **Lỗi:** `MODIFY` làm mất `NOT NULL`/`DEFAULT` cũ; thu nhỏ kiểu (VARCHAR(255) → (10)) có thể cắt mất dữ liệu; `ALTER` bảng lớn có thể khóa bảng lâu.
8. **Khi nào dùng:** yêu cầu mới cần thêm cột/ràng buộc mà không mất dữ liệu.
9. **Bài tự luyện:** thêm cột `Publisher VARCHAR(100)` rồi đổi thành `VARCHAR(150) NOT NULL DEFAULT ''`. *Đáp án:* `ALTER TABLE DEMO_BOOK ADD COLUMN Publisher VARCHAR(100); ALTER TABLE DEMO_BOOK MODIFY COLUMN Publisher VARCHAR(150) NOT NULL DEFAULT '';`

#### 2.11.13. DROP TABLE
1. **Công dụng:** xóa hẳn bảng (cấu trúc + dữ liệu). 2. **Cú pháp:** `DROP TABLE [IF EXISTS] t1 [, t2];`
3. **Cơ bản:** `DROP TABLE DEMO_LOG;`
4. **Thực tế:** `DROP TABLE IF EXISTS DEMO_STUDENT, DEMO_CLASS;` (bảng con trước, hoặc cùng một lệnh).
5. **Giải thích:** không hoàn tác được; `IF EXISTS` tránh lỗi 1051.
6. **Khác:** `DROP DATABASE` xóa cả CSDL.
7. **Lỗi:** 3730 *Cannot drop table referenced by a foreign key* → xóa bảng con trước.
8. **Khi nào dùng:** bỏ bảng không còn dùng, dọn bảng thử nghiệm.
9. **Bài tự luyện:** xóa `DEMO_BOOK` và `DEMO_ENROLL` an toàn. *Đáp án:* `DROP TABLE IF EXISTS DEMO_BOOK, DEMO_ENROLL;`

#### 2.11.14. TRUNCATE TABLE
1. **Công dụng:** xóa **mọi dòng**, giữ cấu trúc, reset `AUTO_INCREMENT`. 2. **Cú pháp:** `TRUNCATE TABLE t;`
3. **Cơ bản:** `TRUNCATE TABLE DEMO_LOG;`
4. **Thực tế:** `SELECT COUNT(*) FROM DEMO_LOG;` (3) → `TRUNCATE TABLE DEMO_LOG;` → `SELECT COUNT(*) ...` (0), dòng mới có `LogID = 1`.
5. **Giải thích:** nhanh hơn `DELETE` toàn bảng vì không xóa từng dòng; không có `WHERE`.
6. **Khác:** tương đương `DELETE FROM t;` nhưng khác ở tốc độ, reset ID, và không rollback được.
7. **Lỗi:** 1701 khi bảng bị khóa ngoại tham chiếu; không dùng được để xóa **một phần**.
8. **Khi nào dùng:** làm sạch bảng tạm/bảng staging.
9. **Bài tự luyện:** khi nào phải dùng `DELETE` thay `TRUNCATE`? *Đáp án:* khi cần `WHERE`, cần rollback, hoặc bảng đang được khóa ngoại tham chiếu.

#### 2.11.15. RENAME TABLE
1. **Công dụng:** đổi tên bảng. 2. **Cú pháp:** `RENAME TABLE cu TO moi [, cu2 TO moi2];`
3. **Cơ bản:** `RENAME TABLE DEMO_LOG TO DEMO_LOG2;`
4. **Thực tế:** hoán đổi bảng an toàn: `RENAME TABLE t TO t_old, t_new TO t;` (một thao tác nguyên tử).
5. **Giải thích:** khóa ngoại tham chiếu bảng được đổi tên tự cập nhật theo.
6. **Khác:** `ALTER TABLE cu RENAME TO moi;`
7. **Lỗi:** tên mới đã tồn tại → 1050; code ứng dụng còn dùng tên cũ.
8. **Khi nào dùng:** chuẩn hóa tên, thay thế bảng (swap).
9. **Bài tự luyện:** đổi `DEMO_LOG2` về `DEMO_LOG`. *Đáp án:* `RENAME TABLE DEMO_LOG2 TO DEMO_LOG;`

#### 2.11.16. DESCRIBE, SHOW TABLES, SHOW CREATE TABLE
1. **Công dụng:** xem danh sách bảng và cấu trúc bảng. 2. **Cú pháp:** `SHOW TABLES; DESCRIBE t; SHOW CREATE TABLE t;`
3. **Cơ bản:** `SHOW TABLES;` → CUSTOMER, EMPLOYEE, ORDER_DETAIL, PRODUCT, SALEORDER (cùng các bảng `DEMO_*` nếu đã tạo).
4. **Thực tế:** `DESCRIBE SALEORDER;`

| Field | Type | Null | Key | Default |
|---|---|---|---|---|
| OrderID | int | NO | PRI | NULL |
| CustID | int | NO | MUL | NULL |
| EmpID | int | NO | MUL | NULL |
| OrderDate | date | NO | | NULL |
| Status | varchar(20) | NO | | PENDING |
| TotalAmount | decimal(12,2) | NO | | 0.00 |

5. **Giải thích:** `Key = MUL` là cột có chỉ mục không duy nhất (khóa ngoại); `SHOW CREATE TABLE` in ra lệnh `CREATE TABLE` đầy đủ, gồm cả ràng buộc.
6. **Khác:** `SHOW COLUMNS FROM t;` (giống `DESCRIBE`); `SHOW INDEX FROM t;`; `SHOW TABLES LIKE 'DEMO%';`.
7. **Lỗi:** 1146 *Table doesn't exist* (sai tên hoặc quên `USE`).
8. **Khi nào dùng:** khám phá CSDL lạ, kiểm tra sau `ALTER`.
9. **Bài tự luyện:** liệt kê chỉ các bảng bắt đầu bằng `DEMO`. *Đáp án:* `SHOW TABLES LIKE 'DEMO%';`

#### 2.11.17. Chọn kiểu dữ liệu: bài tự luyện
Chọn kiểu cho: (a) giá bán; (b) số điện thoại; (c) ngày sinh; (d) trạng thái đúng/sai; (e) mô tả sản phẩm dài.
*Đáp án:* (a) `DECIMAL(12,2)`; (b) `VARCHAR(15)`; (c) `DATE`; (d) `BOOLEAN`; (e) `TEXT`.

**Dọn dẹp sau khi thực hành:**
```sql
DROP TABLE IF EXISTS DEMO_ENROLL, DEMO_LOG, DEMO_BOOK, DEMO_STUDENT, DEMO_CLASS;
DROP DATABASE IF EXISTS demo_db;
DROP DATABASE IF EXISTS library_demo;
```

---

## CHƯƠNG 3: INSERT, UPDATE VÀ DELETE

> ⚠️ **Quy tắc sống còn:** Trước khi chạy `UPDATE`/`DELETE`, hãy (1) viết `SELECT` với **cùng điều kiện WHERE** để xem dòng nào sẽ bị ảnh hưởng, (2) khi thử nghiệm, bọc trong transaction để có thể hoàn tác:
>
> ```sql
> START TRANSACTION;
> UPDATE ...;           -- thử
> SELECT ...;           -- kiểm tra kết quả
> ROLLBACK;             -- hoàn tác (hoặc COMMIT; để giữ lại)
> ```
> Cách này dùng được với `INSERT`/`UPDATE`/`DELETE` (bảng InnoDB, mặc định của MySQL 8). **Không** dùng được với `TRUNCATE`, `DROP`, `ALTER`.

### 3.1. INSERT INTO ... VALUES

**1. Công dụng:** Thêm dòng mới vào bảng.

**2. Cú pháp:**
```sql
INSERT INTO ten_bang (cot1, cot2, ...) VALUES (gia_tri1, gia_tri2, ...);
INSERT INTO ten_bang VALUES (gia_tri_cot_1, gia_tri_cot_2, ...);   -- phải đủ MỌI cột, đúng thứ tự
```

**3. Ví dụ cơ bản:**
```sql
INSERT INTO CUSTOMER (CustName, City, Phone, Email, JoinDate)
VALUES ('Dang Van Giang', 'Can Tho', '0901000007', 'giang@mail.com', '2025-08-01');
```
Kết quả: bảng `CUSTOMER` có thêm dòng `CustID = 7` (do `AUTO_INCREMENT` tự điền).

**4. Giải thích từng dòng:**
- `INSERT INTO CUSTOMER (CustName, City, ...)`: nói rõ sẽ điền **những cột nào**.
- `VALUES (...)`: các giá trị **theo đúng thứ tự cột** đã liệt kê. Chuỗi và ngày dùng nháy đơn.
- Không liệt kê `CustID` vì cột tự tăng.

**5. Các cách dùng khác:**

*a) Chỉ điền một số cột (các cột còn lại lấy DEFAULT hoặc NULL):*
```sql
INSERT INTO CUSTOMER (CustName, City, Phone, JoinDate)
VALUES ('Bui Thi Hoa', 'Hue', '0901000008', CURDATE());   -- Email sẽ là NULL
```

*b) Chèn nhiều dòng một lần (nhanh hơn chèn từng dòng):*
```sql
INSERT INTO PRODUCT (ProdName, Category, Price, Stock) VALUES
('Speaker',  'Accessories', 1500, 10),
('Tablet',   'Electronics', 7000, 12),
('Charger',  'Accessories',  200, 80);
```

*c) Dùng DEFAULT:* `INSERT INTO SALEORDER (CustID, EmpID, OrderDate) VALUES (1, 2, '2025-08-10');` → `Status = 'PENDING'`, `TotalAmount = 0` nhờ DEFAULT.

*d) `INSERT ... SELECT`:* xem [Chương 11](#chương-11-insert-into--select).

**6. Lỗi thường gặp:**

| Lệnh sai | Lỗi | Cách sửa |
|---|---|---|
| `INSERT INTO CUSTOMER VALUES ('A','Ha Noi')` | 1136: số giá trị không khớp số cột | Liệt kê cột hoặc điền đủ giá trị |
| `INSERT ... Phone = '0901000001'` (đã tồn tại) | 1062 Duplicate entry | Dùng số khác, hoặc `INSERT IGNORE` / `ON DUPLICATE KEY UPDATE` |
| `INSERT INTO SALEORDER (CustID,...) VALUES (99, ...)` | 1452: khóa ngoại – khách 99 không tồn tại | Thêm khách trước |
| `INSERT ... VALUES ('2025/13/45')` | 1292: ngày sai | Dùng `'YYYY-MM-DD'` hợp lệ |
| Quên nháy đơn quanh chuỗi | Lỗi cú pháp / hiểu nhầm là tên cột | `'Ha Noi'` |

**Bonus: UPSERT** (thêm, nếu trùng khóa thì cập nhật):
```sql
INSERT INTO PRODUCT (ProdID, ProdName, Category, Price, Stock)
VALUES (2, 'Mouse Logitech', 'Accessories', 350, 100)
ON DUPLICATE KEY UPDATE Price = VALUES(Price);
```
Vì `ProdID = 2` đã tồn tại nên MySQL chuyển sang `UPDATE Price = 350`.

### 3.2. UPDATE

**1. Công dụng:** Sửa giá trị của các dòng đã có.

**2. Cú pháp:**
```sql
UPDATE ten_bang
SET cot1 = gia_tri1, cot2 = gia_tri2, ...
[WHERE dieu_kien];
```

> 🚨 **THIẾU `WHERE` = SỬA TẤT CẢ CÁC DÒNG.** `UPDATE EMPLOYEE SET Salary = 0;` đưa lương của **cả công ty** về 0. MySQL Workbench mặc định bật "Safe Updates" để chặn việc này (lỗi 1175), nhưng đừng trông chờ vào đó.

**3. Ví dụ cơ bản (một cột):**
```sql
-- Đổi giá Mouse Logitech thành 350
UPDATE PRODUCT SET Price = 350 WHERE ProdID = 2;
```
Trước: `ProdID=2, Price=300` → Sau: `Price=350`. Chỉ 1 dòng thay đổi.

**4. Nhiều cột cùng lúc:**
```sql
UPDATE CUSTOMER
SET City = 'Can Tho', Email = 'cuong@mail.com'
WHERE CustID = 3;
```

**5. Biểu thức tính toán:** giá trị mới có thể dựa trên giá trị cũ.
```sql
-- Tăng lương 5% cho nhân viên Sales vào làm trước 2023
UPDATE EMPLOYEE
SET Salary = Salary * 1.05
WHERE Position = 'Sales' AND HireDate < '2023-01-01';
```
Dòng bị ảnh hưởng: EmpID 2 (2021) và 3 (2022). EmpID 4 vào làm 2023-02-20 nên **không** đổi.

| EmpID | Salary trước | Salary sau |
|---|---|---|
| 2 | 15000000 | 15750000 |
| 3 | 14000000 | 14700000 |
| 4 | 13000000 | 13000000 (giữ) |

Quy trình an toàn:
```sql
SELECT EmpID, EmpName, Salary FROM EMPLOYEE
WHERE Position = 'Sales' AND HireDate < '2023-01-01';   -- xem trước
-- Thấy đúng 2 dòng thì mới đổi SELECT thành UPDATE ... SET
```

**6. UPDATE kết hợp CASE WHEN:** sửa **nhiều giá trị khác nhau** trong một lệnh.

Dạng bài kinh điển: *cập nhật trạng thái sinh viên theo điểm trung bình.* Tạo bảng minh họa:
```sql
CREATE TABLE student_demo (
    StudentID INT PRIMARY KEY,
    FullName  VARCHAR(100),
    Gpa       DECIMAL(3,2),
    Status    VARCHAR(20)
);
INSERT INTO student_demo VALUES
(1, 'An',   3.60, NULL),
(2, 'Binh', 2.80, NULL),
(3, 'Cuong',1.90, NULL),
(4, 'Dung', 3.20, NULL);

UPDATE student_demo
SET Status = CASE
                WHEN Gpa >= 3.6 THEN 'EXCELLENT'
                WHEN Gpa >= 3.2 THEN 'GOOD'
                WHEN Gpa >= 2.0 THEN 'AVERAGE'
                ELSE 'WARNING'
             END;
```
Giải thích: không có `WHERE` nhưng **chủ ý** (cần xét mọi sinh viên). `CASE` xét từng dòng từ trên xuống, gặp điều kiện đúng đầu tiên thì dừng.

| StudentID | Gpa | Status (sau) |
|---|---|---|
| 1 | 3.60 | EXCELLENT |
| 2 | 2.80 | AVERAGE |
| 3 | 1.90 | WARNING |
| 4 | 3.20 | GOOD |

> Thứ tự `WHEN` quan trọng: nếu đặt `Gpa >= 2.0` lên đầu thì mọi người từ 2.0 trở lên đều thành `AVERAGE`.

**7. UPDATE dựa trên bảng khác – cách 1: JOIN (đặc trưng MySQL):**
```sql
-- Tính lại TotalAmount của từng đơn từ ORDER_DETAIL
UPDATE SALEORDER o
JOIN (
    SELECT OrderID, SUM(Quantity * UnitPrice) AS Total
    FROM ORDER_DETAIL
    GROUP BY OrderID
) d ON d.OrderID = o.OrderID
SET o.TotalAmount = d.Total;
```
Giải thích: bảng con `d` gom chi tiết thành 1 dòng/đơn (tổng tiền); `JOIN` ghép với đơn tương ứng; `SET` ghi tổng vào `TotalAmount`. Với dữ liệu mẫu, kết quả **không đổi** vì dữ liệu đã khớp.

Ví dụ khác, trừ tồn kho theo số lượng đã bán trong đơn **COMPLETED**:
```sql
UPDATE PRODUCT p
JOIN (
    SELECT od.ProdID, SUM(od.Quantity) AS Sold
    FROM ORDER_DETAIL od
    JOIN SALEORDER o ON o.OrderID = od.OrderID
    WHERE o.Status = 'COMPLETED'
    GROUP BY od.ProdID
) s ON s.ProdID = p.ProdID
SET p.Stock = p.Stock - s.Sold;
```
> **Khác biệt:** SQL Server dùng `UPDATE t SET ... FROM t JOIN ...`; PostgreSQL dùng `UPDATE t SET ... FROM other WHERE ...`. MySQL đặt `JOIN` **ngay sau tên bảng**, trước `SET`.

**8. UPDATE dựa trên bảng khác – cách 2: truy vấn con:**
```sql
-- Đặt Stock = 0 cho sản phẩm chưa từng bán
UPDATE PRODUCT
SET Stock = 0
WHERE ProdID NOT IN (SELECT DISTINCT ProdID FROM ORDER_DETAIL);
```
Chỉ `ProdID = 8` (Webcam) chưa từng bán nên bị ảnh hưởng. (Chi tiết ở Chương 8.)

**9. Lỗi thường gặp:**
- Quên `WHERE` (đã cảnh báo).
- `UPDATE ... SET a = 1 AND b = 2` ❌ — dấu `AND` ở đây là phép logic, không phải dấu ngăn cách. Đúng: `SET a = 1, b = 2`.
- Lỗi 1093 *"You can't specify target table for update in FROM clause"*: `UPDATE T ... WHERE x IN (SELECT ... FROM T)`. Cách sửa: bọc truy vấn con trong một subquery nữa (`FROM (SELECT ...) AS tmp`) hoặc dùng JOIN.
- Lỗi 1175 (Safe Update): thêm `WHERE` theo khóa chính, hoặc `SET SQL_SAFE_UPDATES = 0;` (cân nhắc kỹ).

### 3.3. DELETE

**1. Công dụng:** Xóa các dòng.

**2. Cú pháp:**
```sql
DELETE FROM ten_bang [WHERE dieu_kien];
```
> 🚨 **Thiếu `WHERE` = xóa HẾT dữ liệu bảng** (cấu trúc bảng vẫn còn).

**3. Ví dụ:**
```sql
-- Khách hàng 6 chưa có đơn hàng nào → xóa được
DELETE FROM CUSTOMER WHERE CustID = 6;
```

**4. DELETE với điều kiện phức tạp:**
```sql
-- Xóa khách chưa từng mua hàng VÀ không có email
DELETE FROM CUSTOMER
WHERE Email IS NULL
  AND CustID NOT IN (SELECT CustID FROM SALEORDER);
```
(Trên dữ liệu mẫu: khách 3, 5 có email NULL nhưng đã có đơn → không bị xóa.)

**5. Xóa dữ liệu "cha" – "con" (khóa ngoại):**
```sql
DELETE FROM SALEORDER WHERE Status = 'CANCELLED';
-- ERROR 1451: Cannot delete or update a parent row: a foreign key constraint fails
```
Vì `ORDER_DETAIL` còn tham chiếu đơn 4. Phải xóa **con trước, cha sau**:
```sql
DELETE FROM ORDER_DETAIL
WHERE OrderID IN (SELECT OrderID FROM SALEORDER WHERE Status = 'CANCELLED');

DELETE FROM SALEORDER WHERE Status = 'CANCELLED';
```
Kết quả: mất dòng chi tiết `(4,1,1,15000)` và đơn 4.

**6. DELETE với JOIN (MySQL):**
```sql
DELETE od
FROM ORDER_DETAIL od
JOIN SALEORDER o ON o.OrderID = od.OrderID
WHERE o.Status = 'CANCELLED';
```
`DELETE od` chỉ rõ xóa dòng của bảng nào (`od`), `o` chỉ dùng để lọc.

**7. Phân biệt DELETE / TRUNCATE / DROP:** xem bảng ở mục 2.8. Tóm tắt: *muốn xóa một số dòng* → `DELETE ... WHERE`; *muốn làm sạch bảng nhanh, reset ID* → `TRUNCATE`; *muốn bỏ hẳn bảng* → `DROP`.

**8. Lỗi thường gặp:** thiếu WHERE; xóa cha trước con (1451); dùng `DELETE * FROM t` ❌ (đúng: `DELETE FROM t`).

### 3.4. Các dạng bài đặc trưng của Chương 3

| Dạng bài | Hướng làm | Xem |
|---|---|---|
| Cập nhật trạng thái theo điểm TB | `UPDATE ... SET col = CASE WHEN ... END` | 3.2 mục 6 |
| Tăng lương theo điều kiện | `UPDATE ... SET Salary = Salary * x WHERE ...` | 3.2 mục 5 |
| Cập nhật theo tổng doanh thu | `UPDATE ... WHERE id IN (SELECT ... GROUP BY ... HAVING SUM(...) > n)` | Chương 8 |
| Chèn từ bảng này sang bảng khác | `INSERT INTO ... SELECT` | Chương 11 |
| Xóa dữ liệu theo điều kiện | `DELETE FROM ... WHERE ...` (xóa con trước) | 3.3 |

### 3.5. Bài tập tự luyện Chương 3

1. Thêm sản phẩm `Flash Drive`, Accessories, giá 400, tồn kho 60.
2. Giảm 10% giá tất cả sản phẩm thuộc `Electronics`.
3. Đặt `Status = 'CANCELLED'` cho các đơn `PENDING` có `OrderDate` trước `2025-05-01`.
4. Xóa sản phẩm chưa từng được bán.

<details><summary>Đáp án</summary>

```sql
-- 1
INSERT INTO PRODUCT (ProdName, Category, Price, Stock) VALUES ('Flash Drive','Accessories',400,60);
-- 2
UPDATE PRODUCT SET Price = Price * 0.9 WHERE Category = 'Electronics';
-- 3 (đơn 6: PENDING, 2025-04-01 → bị đổi; đơn 10: 2025-06-08 → giữ nguyên)
UPDATE SALEORDER SET Status = 'CANCELLED'
WHERE Status = 'PENDING' AND OrderDate < '2025-05-01';
-- 4 (Webcam và Flash Drive vừa thêm)
DELETE FROM PRODUCT
WHERE ProdID NOT IN (SELECT ProdID FROM ORDER_DETAIL);
```
Với câu 4: nếu `ORDER_DETAIL.ProdID` có NULL thì `NOT IN` trả về rỗng (xem Chương 8). Ở đây `ProdID` là NOT NULL nên an toàn.

Nhớ chạy lại script CSDL nếu muốn quay lại dữ liệu gốc.
</details>

---

### 3.6. CHI TIẾT TỪNG DẠNG LỆNH CỦA CHƯƠNG 3 (mẫu 10 mục + bài tự luyện)

> Giả định `shop_db` ở trạng thái gốc trước mỗi mục. Khi thử `UPDATE`/`DELETE`, bọc trong `START TRANSACTION; ... ROLLBACK;`.
> Mẫu: **1.Công dụng · 2.Cú pháp · 3.Cơ bản · 4.Thực tế + dữ liệu thay đổi · 5.Giải thích · 6.Cách dùng khác · 7.Lỗi · 8.Khi nào dùng · 9.Bài tự luyện.**

#### 3.6.1. INSERT INTO ... VALUES (một dòng)
1. **Công dụng:** thêm một dòng mới.
2. **Cú pháp:** `INSERT INTO t (c1, c2, ...) VALUES (v1, v2, ...);`
3. **Cơ bản:** `INSERT INTO CUSTOMER (CustName, City, Phone, JoinDate) VALUES ('Dang Van Giang', 'Can Tho', '0901000007', '2025-08-01');`
4. **Thực tế:** thêm nhân viên mới dưới quyền nhân viên 2:
```sql
INSERT INTO EMPLOYEE (EmpName, Position, Salary, HireDate, ManagerID)
VALUES ('Vo Thanh Tung', 'Sales', 11000000, '2025-09-01', 2);
```
→ `EMPLOYEE` có thêm dòng `EmpID = 6` (tự tăng), `ManagerID = 2`; các dòng khác không đổi.
5. **Giải thích:** liệt kê cột nào thì `VALUES` phải đúng thứ tự và số lượng đó; cột `EmpID` bỏ qua vì `AUTO_INCREMENT`.
6. **Khác:** `INSERT IGNORE` (bỏ qua dòng lỗi trùng); `REPLACE INTO` (xóa dòng trùng khóa rồi chèn); `ON DUPLICATE KEY UPDATE`.
7. **Lỗi:** 1136 (sai số giá trị); 1062 (trùng `Phone` UNIQUE); 1452 (`ManagerID` không tồn tại); 1364 (thiếu cột NOT NULL không có DEFAULT).
8. **Khi nào dùng:** nhập vài bản ghi cụ thể.
9. **Bài tự luyện:** thêm sản phẩm `Charger`, Accessories, giá 200, tồn kho 80.
   *Đáp án:* `INSERT INTO PRODUCT (ProdName, Category, Price, Stock) VALUES ('Charger','Accessories',200,80);` → `ProdID = 9`.

#### 3.6.2. INSERT nhiều dòng
1. **Công dụng:** thêm nhiều dòng trong một lệnh (nhanh hơn từng lệnh). 2. **Cú pháp:** `INSERT INTO t (cols) VALUES (...), (...), (...);`
3. **Cơ bản:** `INSERT INTO PRODUCT (ProdName, Category, Price, Stock) VALUES ('Speaker','Accessories',1500,10), ('Tablet','Electronics',7000,12);`
4. **Thực tế:** thêm hai khách:
```sql
INSERT INTO CUSTOMER (CustName, City, Phone, Email, JoinDate) VALUES
('Bui Thi Hoa',  'Hue',   '0901000008', 'hoa@mail.com', '2025-08-05'),
('Dinh Van Khoa','Vinh',  '0901000009', NULL,           '2025-08-06');
```
→ thêm 2 dòng (`CustID` 7 và 8); lỗi ở **một** dòng làm hỏng **cả lệnh** (không dòng nào được thêm).
5. **Giải thích:** các bộ giá trị cách nhau bằng dấu phẩy; dùng `NULL` tường minh cho cột không có dữ liệu.
6. **Khác:** chèn hàng nghìn dòng nên chia lô 500–1000 dòng/lệnh.
7. **Lỗi:** thiếu dấu phẩy giữa các bộ; dùng dấu `;` giữa các bộ.
8. **Khi nào dùng:** dữ liệu mẫu, nhập lô.
9. **Bài tự luyện:** thêm 3 phụ kiện giá 100, 200, 300 (tên tùy ý) bằng một lệnh. *Đáp án:* một `INSERT ... VALUES (...), (...), (...)`.

#### 3.6.3. INSERT chỉ định một số cột
1. **Công dụng:** điền một phần cột, phần còn lại lấy `DEFAULT`/`NULL`/tự tăng. 2. **Cú pháp:** `INSERT INTO t (c1, c3) VALUES (...);`
3. **Cơ bản:** `INSERT INTO SALEORDER (CustID, EmpID, OrderDate) VALUES (1, 2, '2025-08-10');`
4. **Thực tế:** dòng mới có `Status = 'PENDING'` và `TotalAmount = 0` nhờ `DEFAULT`; `OrderID = 13`.
5. **Giải thích:** cột không liệt kê dùng giá trị mặc định của bảng.
6. **Khác:** `VALUES (1, 2, '2025-08-10', DEFAULT, DEFAULT)`.
7. **Lỗi:** bỏ qua cột `NOT NULL` không có `DEFAULT` → lỗi 1364.
8. **Khi nào dùng:** thông thường — chỉ điền những gì cần.
9. **Bài tự luyện:** thêm khách không có email, ngày đăng ký là hôm nay. *Đáp án:* `INSERT INTO CUSTOMER (CustName, City, Phone, JoinDate) VALUES ('X','Ha Noi','0901000010',CURDATE());`

#### 3.6.4. INSERT INTO ... SELECT
1. **Công dụng:** thêm dữ liệu lấy từ một truy vấn. 2. **Cú pháp:** `INSERT INTO t (cols) SELECT ...;`
3. **Cơ bản:** `INSERT INTO PRODUCT_ELEC (ProdID, ProdName, Price) SELECT ProdID, ProdName, Price FROM PRODUCT WHERE Category='Electronics';`
4. **Thực tế:** xem **Chương 11** (copy, WHERE, JOIN, GROUP BY, HAVING).
5–8. Xem Chương 11, mục 11.1–11.8 (ghép cột theo **vị trí**).
9. **Bài tự luyện:** xem mục 11.10.

#### 3.6.5. UPDATE một cột
1. **Công dụng:** sửa một cột của các dòng chọn. 2. **Cú pháp:** `UPDATE t SET c = v WHERE dk;`
3. **Cơ bản:** `UPDATE PRODUCT SET Price = 350 WHERE ProdID = 2;`
4. **Thực tế:** đổi số điện thoại khách 1: `UPDATE CUSTOMER SET Phone = '0988000001' WHERE CustID = 1;` → chỉ 1 dòng đổi (`Phone` từ `0901000001`).
5. **Giải thích:** `WHERE` theo **khóa chính** để chắc chắn một dòng.
6. **Khác:** `SET c = NULL`; `SET c = DEFAULT`.
7. **Lỗi:** thiếu `WHERE` (sửa tất cả); trùng UNIQUE (1062); safe-update mode (1175).
8. **Khi nào dùng:** sửa một thông tin.
9. **Bài tự luyện:** đặt email khách 3 là `cuong@mail.com`. *Đáp án:* `UPDATE CUSTOMER SET Email='cuong@mail.com' WHERE CustID=3;`

#### 3.6.6. UPDATE nhiều cột
1. **Công dụng:** sửa nhiều cột một lần. 2. **Cú pháp:** `UPDATE t SET c1 = v1, c2 = v2 WHERE dk;`
3. **Cơ bản:** `UPDATE CUSTOMER SET City = 'Can Tho', Email = 'x@mail.com' WHERE CustID = 3;`
4. **Thực tế:** `UPDATE EMPLOYEE SET Position = 'Senior Sales', Salary = 18000000 WHERE EmpID = 2;` → NV 2 đổi cả chức vụ và lương trong một lệnh.
5. **Giải thích:** các cặp `cột = giá trị` ngăn cách bằng dấu **phẩy**, không phải `AND`.
6. **Khác:** các biểu thức trong `SET` đọc giá trị **trước khi** sửa theo thứ tự trái sang phải trong MySQL (cẩn thận khi `SET a = b, b = a`).
7. **Lỗi:** `SET a = 1 AND b = 2` (thành `a = (1 AND b = 2)`).
8. **Khi nào dùng:** cập nhật hồ sơ.
9. **Bài tự luyện:** đổi giá Laptop thành 14500 và tồn kho thành 18. *Đáp án:* `UPDATE PRODUCT SET Price=14500, Stock=18 WHERE ProdID=1;`

#### 3.6.7. UPDATE kết hợp WHERE (điều kiện nhiều dòng)
1. **Công dụng:** sửa hàng loạt các dòng thỏa điều kiện. 2. **Cú pháp:** `UPDATE t SET ... WHERE dk1 AND dk2;`
3. **Cơ bản:** `UPDATE PRODUCT SET Stock = 0 WHERE Stock < 20;`
4. **Thực tế:** `UPDATE SALEORDER SET Status = 'CANCELLED' WHERE Status = 'PENDING' AND OrderDate < '2025-05-01';` → đơn 6 đổi sang CANCELLED; đơn 10 (ngày 06-08) giữ nguyên.
5. **Giải thích:** **luôn** thử bằng `SELECT` cùng `WHERE` trước.
6. **Khác:** `WHERE ... IN (...)`, `BETWEEN`, `LIKE`.
7. **Lỗi:** thiếu ngoặc khi trộn `AND/OR`; so sánh ngày sai kiểu.
8. **Khi nào dùng:** thay đổi hàng loạt theo quy tắc.
9. **Bài tự luyện:** tăng tồn kho 10 cho phụ kiện có tồn kho dưới 50. *Đáp án:* `UPDATE PRODUCT SET Stock = Stock + 10 WHERE Category='Accessories' AND Stock < 50;` (Headphone 40 → 50, Webcam 15 → 25).

#### 3.6.8. UPDATE kết hợp biểu thức tính toán
1. **Công dụng:** giá mới tính từ giá cũ. 2. **Cú pháp:** `SET c = c * 1.1`, `c + 5`, `ROUND(c * 0.9, 0)`...
3. **Cơ bản:** `UPDATE EMPLOYEE SET Salary = Salary * 1.05 WHERE Position = 'Sales' AND HireDate < '2023-01-01';`
4. **Thực tế:** giảm 10% và làm tròn hàng trăm: `UPDATE PRODUCT SET Price = ROUND(Price * 0.9, -2) WHERE Category = 'Electronics';` → Laptop 13500 (15000 × 0.9 = 13500), Monitor 3600, Smartphone 8100.
5. **Giải thích:** vế phải dùng **giá trị cũ** của dòng.
6. **Khác:** `SET Stock = GREATEST(Stock - 5, 0)` (không để âm).
7. **Lỗi:** chạy hai lần nhân thêm lần nữa; kết quả vượt kiểu dữ liệu (DECIMAL tràn).
8. **Khi nào dùng:** tăng/giảm theo tỷ lệ.
9. **Bài tự luyện:** tăng lương 3% cho mọi nhân viên **không phải** quản lý. *Đáp án:* `UPDATE EMPLOYEE SET Salary = Salary * 1.03 WHERE Position <> 'Manager';`

#### 3.6.9. UPDATE kết hợp CASE WHEN
1. **Công dụng:** mỗi nhóm dòng nhận giá trị khác nhau. 2. **Cú pháp:** `SET c = CASE WHEN dk THEN v1 ... ELSE v END`
3. **Cơ bản:** (cập nhật trạng thái sinh viên theo GPA) xem mục 3.2 mục 6.
4. **Thực tế (tăng lương theo bậc):**
```sql
UPDATE EMPLOYEE
SET Salary = CASE
                WHEN Salary < 12000000 THEN Salary * 1.10
                WHEN Salary < 15000000 THEN Salary * 1.05
                ELSE Salary
             END;
```
→ NV 5: 10,000,000 → 11,000,000; NV 4: 13,000,000 → 13,650,000; NV 3: 14,000,000 → 14,700,000; NV 2 (15,000,000) và NV 1 (30,000,000) giữ nguyên.
5. **Giải thích:** nhánh `ELSE Salary` giữ nguyên các dòng còn lại (nếu bỏ → NULL).
6. **Khác:** `CASE col WHEN 'a' THEN ...`.
7. **Lỗi:** đặt thứ tự `WHEN` sai (nhánh rộng trước); quên `ELSE`.
8. **Khi nào dùng:** "nếu ... thì ... còn nếu ...".
9. **Bài tự luyện:** tồn kho dưới 20 → +50; từ 20 đến 49 → +20; còn lại giữ. *Đáp án:* `UPDATE PRODUCT SET Stock = CASE WHEN Stock < 20 THEN Stock + 50 WHEN Stock < 50 THEN Stock + 20 ELSE Stock END;`

#### 3.6.10. UPDATE dựa trên dữ liệu bảng khác (JOIN)
1. **Công dụng:** sửa bảng A theo dữ liệu bảng B. 2. **Cú pháp:** `UPDATE A JOIN B ON ... SET A.c = B.c [WHERE ...];`
3. **Cơ bản:** (tổng hợp từ SALEORDER) xem mục 3.2 mục 7.
4. **Thực tế:** đồng bộ đơn giá dòng chi tiết với giá hiện tại của sản phẩm:
```sql
UPDATE PRODUCT SET Price = 350 WHERE ProdID = 2;          -- Mouse đổi giá
UPDATE ORDER_DETAIL od
JOIN PRODUCT p ON p.ProdID = od.ProdID
SET od.UnitPrice = p.Price
WHERE od.OrderID = 6;
```
→ dòng `(6, 2)` (Mouse) `UnitPrice` 300 → 350; dòng `(6, 6)` (USB 250) giữ 250.
5. **Giải thích:** `JOIN` đứng ngay sau tên bảng được sửa, **trước** `SET`.
6. **Khác:** `UPDATE ... SET a.x = (SELECT ...)`.
7. **Lỗi:** JOIN nhân dòng (một dòng A khớp nhiều dòng B → giá trị gán không xác định); quên `ON`.
8. **Khi nào dùng:** đồng bộ/tính lại dữ liệu từ bảng khác.
9. **Bài tự luyện:** đặt `UnitPrice` của các dòng chi tiết đơn 12 bằng giá hiện tại của sản phẩm. *Đáp án:* tương tự ví dụ, với `WHERE od.OrderID = 12`.

#### 3.6.11. UPDATE kết hợp truy vấn con
1. **Công dụng:** điều kiện hoặc giá trị lấy từ subquery. 2. **Cú pháp:** `UPDATE t SET ... WHERE c IN (SELECT ...)`.
3. **Cơ bản:** UPDATE lương theo doanh thu (mục 8.11).
4. **Thực tế (cùng bảng → lỗi 1093 và cách sửa):**
```sql
-- ❌ lỗi 1093: bảng EMPLOYEE vừa được sửa vừa nằm trong subquery
UPDATE EMPLOYEE SET Salary = Salary * 1.02
WHERE Salary < (SELECT AVG(Salary) FROM EMPLOYEE);

-- ✔ bọc thêm một lớp bảng dẫn xuất
UPDATE EMPLOYEE SET Salary = Salary * 1.02
WHERE Salary < (SELECT a FROM (SELECT AVG(Salary) AS a FROM EMPLOYEE) t);
```
→ lương trung bình 16,400,000; bốn nhân viên dưới mức đó: NV 2: 15,300,000; NV 3: 14,280,000; NV 4: 13,260,000; NV 5: 10,200,000. NV 1 giữ nguyên.
5. **Giải thích:** bảng dẫn xuất `t` được **vật hóa** (tính trước) nên MySQL cho phép.
6. **Khác:** `UPDATE t JOIN (SELECT ...) x ON ... SET ...`.
7. **Lỗi:** 1093; subquery trả nhiều dòng với `=` (1242).
8. **Khi nào dùng:** cập nhật theo kết quả thống kê.
9. **Bài tự luyện:** giảm giá 5% cho sản phẩm đắt hơn giá trung bình. *Đáp án:* `UPDATE PRODUCT SET Price = Price * 0.95 WHERE Price > (SELECT a FROM (SELECT AVG(Price) AS a FROM PRODUCT) t);` → Laptop, Monitor, Smartphone.

#### 3.6.12. DELETE kết hợp WHERE
1. **Công dụng:** xóa các dòng thỏa điều kiện. 2. **Cú pháp:** `DELETE FROM t WHERE dk;`
3. **Cơ bản:** `DELETE FROM CUSTOMER WHERE CustID = 6;`
4. **Thực tế:** `DELETE FROM PRODUCT WHERE Category = 'Accessories' AND Stock < 20;` → xóa Webcam (tồn 15) nếu không bị khóa ngoại chặn (Webcam chưa bán nên xóa được).
5. **Giải thích:** `DELETE` xóa **dòng**, không xóa bảng.
6. **Khác:** `DELETE ... ORDER BY ... LIMIT n` (xóa n dòng đầu).
7. **Lỗi:** thiếu `WHERE` (xóa sạch); khóa ngoại (1451).
8. **Khi nào dùng:** dọn dữ liệu sai/hết hạn.
9. **Bài tự luyện:** xóa các đơn CANCELLED (gồm cả chi tiết). *Đáp án:* xem bài 11.2.

#### 3.6.13. DELETE với điều kiện phức tạp
1. **Công dụng:** xóa theo điều kiện phụ thuộc bảng khác/nhiều tiêu chí. 2. **Cú pháp:** `DELETE FROM t WHERE ... IN/EXISTS (subquery)` hoặc `DELETE t FROM t JOIN ...`.
3. **Cơ bản:** `DELETE FROM CUSTOMER WHERE CustID NOT IN (SELECT CustID FROM SALEORDER);`
4. **Thực tế:** xóa dòng chi tiết có số lượng 1 của các đơn PENDING:
```sql
DELETE FROM ORDER_DETAIL
WHERE Quantity = 1
  AND OrderID IN (SELECT OrderID FROM SALEORDER WHERE Status = 'PENDING');
```
→ xóa 1 dòng: `(OrderID 10, ProdID 7, Quantity 1)`; các dòng của đơn 6 (số lượng 4 và 2) giữ nguyên.
5. **Giải thích:** hai điều kiện `AND`: số lượng + thuộc đơn PENDING (subquery).
6. **Khác:** `DELETE od FROM ORDER_DETAIL od JOIN SALEORDER o ON ... WHERE ...`.
7. **Lỗi:** 1093 (xóa và subquery cùng bảng); `NOT IN` gặp NULL.
8. **Khi nào dùng:** dọn dữ liệu theo quy tắc nghiệp vụ.
9. **Bài tự luyện:** xóa các đơn PENDING (kể cả chi tiết). *Đáp án:* xóa chi tiết trước (`WHERE OrderID IN (SELECT ... 'PENDING')`) rồi xóa `SALEORDER` (xem mục 12.6).

#### 3.6.14. DELETE, TRUNCATE và DROP: phân biệt bằng ví dụ
1. **Công dụng:** ba mức xóa: dòng / toàn bộ dòng / cả bảng. 2. **Cú pháp:** xem bảng 2.8.
3. **Cơ bản:** `DELETE FROM DEMO_LOG WHERE LogID = 2;` / `TRUNCATE TABLE DEMO_LOG;` / `DROP TABLE DEMO_LOG;`
4. **Thực tế (ba kịch bản):**

| Muốn | Dùng | Sau lệnh |
|---|---|---|
| Xóa đơn 4 | `DELETE FROM SALEORDER WHERE OrderID = 4;` (xóa chi tiết trước) | còn 11 đơn, ID vẫn tiếp tục tăng |
| Làm sạch bảng tạm | `TRUNCATE TABLE DEMO_LOG;` | bảng rỗng, ID về 1, không rollback |
| Bỏ hẳn bảng | `DROP TABLE DEMO_LOG;` | bảng biến mất |

5. **Giải thích:** `DELETE` ghi log từng dòng (chậm với bảng lớn, rollback được); `TRUNCATE` và `DROP` là DDL (tự commit).
6. **Khác:** `DELETE FROM t;` (không `WHERE`) ≈ `TRUNCATE` nhưng chậm và không reset ID.
7. **Lỗi:** dùng `TRUNCATE` trên bảng cha có khóa ngoại (1701); nhầm `DROP` với `DELETE`.
8. **Khi nào dùng:** theo bảng trên.
9. **Bài tự luyện:** muốn xóa đơn hàng cũ trước 2025-03-01 nhưng giữ cấu trúc: dùng lệnh nào? *Đáp án:* `DELETE ... WHERE OrderDate < '2025-03-01'` (xóa chi tiết trước); không dùng `TRUNCATE` vì cần điều kiện.

#### 3.6.15. Cảnh báo thiếu WHERE: minh họa
```sql
START TRANSACTION;
UPDATE EMPLOYEE SET Salary = 0;               -- ❌ thiếu WHERE
SELECT EmpName, Salary FROM EMPLOYEE;         -- cả 5 nhân viên có Salary = 0 (nếu không có CHECK Salary > 0)
ROLLBACK;                                     -- hoàn tác
```
Với bảng `EMPLOYEE` của chúng ta, ràng buộc `CHECK (Salary > 0)` sẽ chặn lệnh (lỗi 3819), nhưng **đa số bảng không có CHECK như vậy**. Thói quen bảo vệ: (1) `SELECT` cùng `WHERE` trước, (2) dùng transaction, (3) bật `SQL_SAFE_UPDATES` khi học.

---

## CHƯƠNG 4: SELECT TỪ CƠ BẢN ĐẾN NÂNG CAO

### 4.1. SELECT: lấy dữ liệu

**1. Công dụng:** Đọc dữ liệu, **không làm thay đổi** bảng.

**2. Cú pháp đầy đủ (đọc từ trên xuống, nhưng SQL xử lý theo thứ tự khác, xem Chương 7):**
```sql
SELECT [DISTINCT] cot1, cot2, bieu_thuc AS bi_danh
FROM ten_bang
[WHERE dieu_kien_dong]
[GROUP BY ...]
[HAVING ...]
[ORDER BY cot [ASC|DESC]]
[LIMIT n [OFFSET m]];
```

**3. Lấy mọi cột / một số cột:**
```sql
SELECT * FROM CUSTOMER;                     -- mọi cột, mọi dòng
SELECT CustName, City FROM CUSTOMER;        -- chỉ 2 cột
```
| CustName | City |
|---|---|
| Nguyen Van An | Ha Noi |
| Tran Thi Binh | Ho Chi Minh |
| Le Van Cuong | Da Nang |
| Pham Thi Dung | Ha Noi |
| Hoang Van Em | Ho Chi Minh |
| Vu Thi Phuong | Hai Phong |

> `SELECT *` tiện khi khám phá dữ liệu. Trong code thật nên liệt kê cột cần thiết (nhanh hơn, ổn định khi bảng đổi cấu trúc).

**SELECT không có FROM:** `SELECT 1 + 1, NOW(), 'xin chao';` dùng để thử hàm/biểu thức.

### 4.2. DISTINCT: loại trùng

```sql
SELECT DISTINCT City FROM CUSTOMER;
```
| City |
|---|
| Ha Noi |
| Ho Chi Minh |
| Da Nang |
| Hai Phong |

6 khách nhưng chỉ có 4 thành phố khác nhau. `DISTINCT` áp dụng cho **cả tổ hợp các cột**:
```sql
SELECT DISTINCT City, JoinDate FROM CUSTOMER;   -- cặp (City, JoinDate) không trùng → vẫn 6 dòng
SELECT DISTINCT Status FROM SALEORDER;          -- COMPLETED, CANCELLED, PENDING
SELECT DISTINCT CustID FROM SALEORDER;          -- 1,2,3,4,5 (khách nào đã từng mua)
```
**Lỗi:** viết `SELECT DISTINCT City, DISTINCT Status` ❌. `DISTINCT` chỉ đặt **một lần** ngay sau `SELECT`.

### 4.3. AS: bí danh (alias)

```sql
SELECT ProdName AS TenSanPham,
       Price,
       Stock * Price AS GiaTriTonKho
FROM PRODUCT
LIMIT 3;
```
| TenSanPham | Price | GiaTriTonKho |
|---|---|---|
| Laptop Dell | 15000.00 | 300000.00 |
| Mouse Logitech | 300.00 | 30000.00 |
| Keyboard Mechanical | 1200.00 | 60000.00 |

- Bí danh cột đổi **tên hiển thị**. `AS` có thể bỏ nhưng nên giữ cho rõ.
- Bí danh có khoảng trắng phải đặt trong backtick: `` AS `Gia tri ton kho` ``.
- **Bí danh bảng** giúp viết ngắn khi JOIN: `FROM CUSTOMER c`, `FROM SALEORDER o`.
- **Lỗi:** dùng bí danh cột trong `WHERE` ❌ (`WHERE GiaTriTonKho > 1000` báo lỗi vì WHERE chạy **trước** SELECT). Dùng được trong `ORDER BY`, và trong `HAVING`/`GROUP BY` ở MySQL.

### 4.4. WHERE và các toán tử so sánh

**Công dụng:** Lọc **từng dòng** – chỉ giữ dòng thỏa điều kiện.

| Toán tử | Nghĩa | Ví dụ |
|---|---|---|
| `=` | bằng (chỉ **một** dấu `=`) | `City = 'Ha Noi'` |
| `<>` hoặc `!=` | khác | `Status <> 'CANCELLED'` |
| `<` `>` `<=` `>=` | so sánh | `Price >= 1000` |
| `<=>` | bằng, **an toàn với NULL** (chỉ MySQL) | `Email <=> NULL` |

```sql
SELECT * FROM PRODUCT WHERE Price > 1000;
```
| ProdID | ProdName | Category | Price | Stock |
|---|---|---|---|---|
| 1 | Laptop Dell | Electronics | 15000.00 | 20 |
| 3 | Keyboard Mechanical | Accessories | 1200.00 | 50 |
| 4 | Monitor 24 inch | Electronics | 4000.00 | 30 |
| 7 | Smartphone | Electronics | 9000.00 | 25 |

Thêm ví dụ:
```sql
SELECT CustName FROM CUSTOMER WHERE City = 'Ha Noi';            -- An, Dung
SELECT OrderID FROM SALEORDER WHERE Status <> 'COMPLETED';      -- 4, 6, 10
SELECT * FROM SALEORDER WHERE OrderDate >= '2025-06-01';        -- đơn 10, 11, 12
```
**Lỗi:** `WHERE City == 'Ha Noi'` ❌ (đó là cú pháp Python). So sánh chuỗi trong MySQL mặc định **không phân biệt hoa/thường**: `'ha noi' = 'Ha Noi'` là đúng.

### 4.5. AND, OR, NOT và lỗi ưu tiên toán tử

| Toán tử | Ý nghĩa |
|---|---|
| `AND` | cả hai điều kiện đúng |
| `OR` | ít nhất một đúng |
| `NOT` | đảo ngược |

**Thứ tự ưu tiên: `NOT` > `AND` > `OR`.** Đây là nguồn lỗi nhiều nhất.

```sql
-- Đơn COMPLETED và tổng > 15000
SELECT OrderID, TotalAmount FROM SALEORDER
WHERE Status = 'COMPLETED' AND TotalAmount > 15000;
```
| OrderID | TotalAmount |
|---|---|
| 1 | 15600.00 |
| 3 | 18800.00 |
| 5 | 30300.00 |
| 9 | 19000.00 |
| 12 | 24000.00 |

**Cái bẫy AND/OR – so sánh hai câu:**
```sql
-- (A) Không dấu ngoặc
SELECT CustName, City, JoinDate FROM CUSTOMER
WHERE City = 'Ha Noi' OR City = 'Ho Chi Minh' AND JoinDate > '2024-05-31';

-- (B) Có dấu ngoặc
SELECT CustName, City, JoinDate FROM CUSTOMER
WHERE (City = 'Ha Noi' OR City = 'Ho Chi Minh') AND JoinDate > '2024-05-31';
```
- (A) hiểu là: `Ha Noi` **hoặc** (`HCM` **và** join sau 31/5). Kết quả: An, Dung, Em (3 dòng).
- (B) hiểu là: (Hà Nội hoặc HCM) **và** join sau 31/5. Kết quả: chỉ Em (1 dòng).

> **Quy tắc vàng:** khi trộn `AND` và `OR`, **luôn dùng dấu ngoặc** dù không bắt buộc.

`NOT`:
```sql
SELECT CustName FROM CUSTOMER WHERE NOT City = 'Ha Noi';   -- tương đương City <> 'Ha Noi'
SELECT CustName FROM CUSTOMER WHERE City NOT IN ('Ha Noi', 'Da Nang');
```

### 4.6. BETWEEN

`BETWEEN a AND b` = `>= a AND <= b` (**gồm cả hai đầu mút**).
```sql
SELECT ProdName, Price FROM PRODUCT WHERE Price BETWEEN 500 AND 5000;
```
| ProdName | Price |
|---|---|
| Keyboard Mechanical | 1200.00 |
| Monitor 24 inch | 4000.00 |
| Headphone | 800.00 |
| Webcam | 700.00 |

```sql
-- Đơn trong khoảng ngày
SELECT OrderID, OrderDate FROM SALEORDER
WHERE OrderDate BETWEEN '2025-02-01' AND '2025-03-31';     -- đơn 2, 3, 4, 5
-- Phủ định
SELECT ProdName FROM PRODUCT WHERE Price NOT BETWEEN 500 AND 5000;
```
**Lỗi:** viết ngược `BETWEEN 5000 AND 500` → không có dòng nào. Với cột `DATETIME`, `BETWEEN '2025-02-01' AND '2025-02-28'` **bỏ sót** các giờ sau 00:00:00 ngày 28 → nên dùng `>= '2025-02-01' AND < '2025-03-01'`.

### 4.7. IN và NOT IN

`IN (a, b, c)` = `= a OR = b OR = c`. Giống `x in [a, b, c]` trong Python.
```sql
SELECT CustName, City FROM CUSTOMER WHERE City IN ('Ha Noi', 'Da Nang');   -- An, Cuong, Dung
SELECT ProdName FROM PRODUCT WHERE ProdID IN (1, 4, 7);                    -- Laptop, Monitor, Smartphone
SELECT OrderID, Status FROM SALEORDER WHERE Status NOT IN ('COMPLETED');   -- 4, 6, 10
```
**Cái bẫy `NOT IN` với NULL:** nếu danh sách chứa NULL thì `NOT IN` **không trả về dòng nào**:
```sql
SELECT 1 FROM DUAL WHERE 1 NOT IN (2, 3);        -- trả về 1
SELECT 1 FROM DUAL WHERE 1 NOT IN (2, NULL);     -- RỖNG! vì không biết 1 có bằng NULL hay không
```
Khi truy vấn con có thể sinh NULL, dùng `NOT EXISTS` (Chương 8).

### 4.8. LIKE và ký tự đại diện

| Ký tự | Nghĩa |
|---|---|
| `%` | **bất kỳ chuỗi nào** (kể cả rỗng) |
| `_` | **đúng một** ký tự |

```sql
SELECT CustName FROM CUSTOMER WHERE CustName LIKE 'Nguyen%';   -- bắt đầu bằng Nguyen → An
SELECT CustName FROM CUSTOMER WHERE CustName LIKE '%Van%';     -- chứa "Van" → An, Cuong, Em
SELECT CustName FROM CUSTOMER WHERE CustName LIKE '%Thi%';     -- Binh, Dung, Phuong
SELECT CustName FROM CUSTOMER WHERE CustName LIKE '%g';        -- kết thúc bằng g
```
Kết quả: Le Van Cuong và Vu Thi Phuong (cùng kết thúc bằng `g`); Hoang Van Em kết thúc bằng `m` nên không có.

```sql
SELECT CustName FROM CUSTOMER WHERE CustName LIKE '_e%';       -- ký tự thứ 2 là 'e' → Le Van Cuong
SELECT Phone FROM CUSTOMER WHERE Phone LIKE '090100000_';      -- 10 ký tự, tận cùng bất kỳ
SELECT ProdName FROM PRODUCT WHERE ProdName NOT LIKE '%o%';    -- không chứa chữ o
```
Tìm đúng ký tự `%` hay `_`: dùng `ESCAPE`: `LIKE '50\%%'`.

**Ghi chú:** `LIKE '%abc'` (bắt đầu bằng `%`) không tận dụng được chỉ mục nên chậm trên bảng lớn. `LIKE` trong MySQL mặc định không phân biệt hoa/thường; PostgreSQL phân biệt (dùng `ILIKE` để không phân biệt).

### 4.9. IS NULL và IS NOT NULL

```sql
SELECT CustName FROM CUSTOMER WHERE Email IS NULL;       -- Cuong, Em
SELECT CustName FROM CUSTOMER WHERE Email IS NOT NULL;   -- An, Binh, Dung, Phuong
SELECT EmpName FROM EMPLOYEE WHERE ManagerID IS NULL;    -- Do Minh Quan (sếp)
```
**Lỗi kinh điển:**
```sql
SELECT * FROM CUSTOMER WHERE Email = NULL;     -- ❌ luôn rỗng
SELECT * FROM CUSTOMER WHERE Email = '';       -- ❌ khác nghĩa: tìm chuỗi rỗng, không phải NULL
SELECT * FROM CUSTOMER WHERE Email <> 'a@b.c'; -- ⚠️ KHÔNG trả về dòng Email NULL
```
Dòng cuối: so sánh với NULL luôn cho "không biết" → bị loại. Muốn lấy cả NULL:
`WHERE Email <> 'a@b.c' OR Email IS NULL`.

### 4.10. ORDER BY

```sql
SELECT ProdName, Price FROM PRODUCT ORDER BY Price DESC;
```
| ProdName | Price |
|---|---|
| Laptop Dell | 15000.00 |
| Smartphone | 9000.00 |
| Monitor 24 inch | 4000.00 |
| Keyboard Mechanical | 1200.00 |
| Headphone | 800.00 |
| Webcam | 700.00 |
| Mouse Logitech | 300.00 |
| USB 64GB | 250.00 |

- `ASC` = tăng dần (mặc định), `DESC` = giảm dần.
- **Nhiều cột:** `ORDER BY City ASC, CustName DESC` → sắp theo thành phố, trong cùng thành phố sắp theo tên giảm dần.
- Sắp theo **bí danh** hoặc **vị trí cột**: `ORDER BY 2 DESC` (cột thứ 2 trong SELECT).
- Sắp theo biểu thức: `ORDER BY Stock * Price DESC`.
- NULL: MySQL coi NULL là **nhỏ nhất** → đứng đầu khi `ASC`, cuối khi `DESC`.
- Không có ORDER BY thì thứ tự kết quả **không được đảm bảo**.

### 4.11. LIMIT và OFFSET

```sql
SELECT ProdName, Price FROM PRODUCT ORDER BY Price DESC LIMIT 3;             -- top 3 giá cao nhất
SELECT ProdName, Price FROM PRODUCT ORDER BY Price DESC LIMIT 3 OFFSET 3;    -- bỏ 3 dòng đầu, lấy 3 tiếp
SELECT ProdName, Price FROM PRODUCT ORDER BY Price DESC LIMIT 3, 3;          -- cách viết tắt: LIMIT offset, count
```
| Lệnh | Kết quả |
|---|---|
| `LIMIT 3` | Laptop, Smartphone, Monitor |
| `LIMIT 3 OFFSET 3` | Keyboard, Headphone, Webcam |

- Phân trang: trang `p`, mỗi trang `n` dòng → `LIMIT n OFFSET (p-1)*n`.
- `ORDER BY ... DESC LIMIT 1` = bản ghi lớn nhất. (Cẩn thận khi có đồng hạng: LIMIT 1 chỉ lấy 1 dòng.)
- **Khác biệt:** SQL Server dùng `TOP 3` hoặc `OFFSET ... FETCH`; MySQL/PostgreSQL dùng `LIMIT`.

### 4.12. Kết hợp nhiều điều kiện: ví dụ tổng hợp

```sql
-- Các sản phẩm Accessories, giá từ 250 đến 1000, tên không chứa 'USB', sắp theo giá giảm, lấy 3 sản phẩm
SELECT ProdName, Price
FROM PRODUCT
WHERE Category = 'Accessories'
  AND Price BETWEEN 250 AND 1000
  AND ProdName NOT LIKE '%USB%'
ORDER BY Price DESC
LIMIT 3;
```
| ProdName | Price |
|---|---|
| Headphone | 800.00 |
| Webcam | 700.00 |
| Mouse Logitech | 300.00 |

Cách xây dựng: lọc `Category` → thêm khoảng giá → loại USB → sắp → cắt top 3. USB 64GB (250) bị loại bởi `NOT LIKE`.

### 4.13. Bài tập tự luyện Chương 4

1. Danh sách khách hàng ở Hồ Chí Minh có email, sắp theo tên.
2. Các đơn hàng COMPLETED trong quý 2 năm 2025 (tháng 4–6), sắp theo `TotalAmount` giảm dần.
3. Sản phẩm có tên bắt đầu bằng `M` hoặc kết thúc bằng `e`, giá dưới 5000.
4. 2 nhân viên lương cao nhất (không tính quản lý).

<details><summary>Đáp án</summary>

```sql
-- 1  → Tran Thi Binh
SELECT CustName FROM CUSTOMER
WHERE City = 'Ho Chi Minh' AND Email IS NOT NULL
ORDER BY CustName;

-- 2  → đơn 9 (19000), 7 (13000), 8 (4500), 11 (1700)
SELECT OrderID, TotalAmount FROM SALEORDER
WHERE Status = 'COMPLETED' AND OrderDate BETWEEN '2025-04-01' AND '2025-06-30'
ORDER BY TotalAmount DESC;

-- 3  → Mouse Logitech, Monitor 24 inch, Headphone
SELECT ProdName, Price FROM PRODUCT
WHERE (ProdName LIKE 'M%' OR ProdName LIKE '%e') AND Price < 5000;

-- 4  → Nguyen Thu Ha (15000000), Tran Quoc Huy (14000000)
SELECT EmpName, Salary FROM EMPLOYEE
WHERE Position <> 'Manager'
ORDER BY Salary DESC
LIMIT 2;
```
Lưu ý ở câu 3: dấu ngoặc quanh `OR` là bắt buộc, nếu thiếu thì điều kiện `Price < 5000` chỉ gắn với vế sau. Kiểm tra: "Smartphone" kết thúc bằng `e` nhưng giá 9000 nên bị loại bởi `Price < 5000`; "Headphone" kết thúc `e` và giá 800 nên có mặt.
</details>

---

### 4.14. Thêm ví dụ cho từng toán tử (mỗi toán tử ≥ 3 ví dụ)

**SELECT biểu thức / nhiều cột**
```sql
SELECT ProdName, Price * Stock AS GiaTri FROM PRODUCT WHERE Price * Stock > 100000;
```
→ Laptop Dell 300000.00; Monitor 24 inch 120000.00; Smartphone 225000.00.
```sql
SELECT CustName, City, JoinDate FROM CUSTOMER WHERE JoinDate < '2024-04-01';     -- An, Binh, Cuong
SELECT OrderID, TotalAmount / 1000 AS NghinDong FROM SALEORDER WHERE OrderID = 1; -- 15.6000
```

**DISTINCT**
```sql
SELECT DISTINCT Category FROM PRODUCT;                 -- Electronics, Accessories
SELECT DISTINCT YEAR(JoinDate) FROM CUSTOMER;          -- 2024 (cả 6 khách cùng năm)
SELECT COUNT(DISTINCT City) FROM CUSTOMER;             -- 4
```

**ORDER BY**
```sql
SELECT ProdName, Category, Price FROM PRODUCT ORDER BY Category DESC, Price;
```
→ Electronics trước (Monitor 4000, Smartphone 9000, Laptop 15000), rồi Accessories theo giá tăng (USB 250, Mouse 300, Webcam 700, Headphone 800, Keyboard 1200).
```sql
SELECT CustName FROM CUSTOMER ORDER BY JoinDate DESC;   -- Phuong, Em, Dung, Cuong, Binh, An
SELECT OrderID, TotalAmount FROM SALEORDER ORDER BY 2 DESC LIMIT 3;   -- 5 (30300), 12 (24000), 9 (19000)
```

**LIMIT / OFFSET**
```sql
SELECT ProdName, Price FROM PRODUCT ORDER BY Price LIMIT 2;                 -- USB 250, Mouse 300
SELECT ProdID, ProdName FROM PRODUCT ORDER BY ProdID LIMIT 3 OFFSET 3;      -- 4 Monitor, 5 Headphone, 6 USB
SELECT OrderID FROM SALEORDER ORDER BY OrderDate DESC LIMIT 1;              -- 12 (đơn mới nhất)
```

**BETWEEN**
```sql
SELECT CustName, JoinDate FROM CUSTOMER WHERE JoinDate BETWEEN '2024-02-01' AND '2024-05-31';
```
→ Binh (2024-02-15), Cuong (2024-03-20), Dung (2024-05-05).
```sql
SELECT ProdName FROM PRODUCT WHERE Stock BETWEEN 20 AND 50;     -- Laptop (20), Keyboard (50), Monitor (30), Headphone (40), Smartphone (25)
SELECT OrderID FROM SALEORDER WHERE TotalAmount NOT BETWEEN 2000 AND 20000;   -- 5, 6, 11, 12
```
(Dòng cuối: các đơn có tiền < 2000 hoặc > 20000: đơn 5 (30300), 6 (1600), 11 (1700), 12 (24000).)

**IN / NOT IN**
```sql
SELECT OrderID FROM SALEORDER WHERE Status IN ('PENDING', 'CANCELLED');   -- 4, 6, 10
SELECT ProdName FROM PRODUCT WHERE ProdID NOT IN (1, 2, 3);                -- Monitor, Headphone, USB, Smartphone, Webcam
SELECT CustName FROM CUSTOMER WHERE CustID IN (SELECT CustID FROM SALEORDER WHERE Status = 'PENDING');  -- Cuong, Em
```

**LIKE**
```sql
SELECT ProdName FROM PRODUCT WHERE ProdName LIKE 'Key%';        -- Keyboard Mechanical
SELECT ProdName FROM PRODUCT WHERE ProdName LIKE '%phone';      -- Headphone, Smartphone
SELECT ProdName FROM PRODUCT WHERE ProdName LIKE '%24%';        -- Monitor 24 inch
SELECT CustName FROM CUSTOMER WHERE Phone LIKE '%5';            -- Hoang Van Em (0901000005)
SELECT CustName FROM CUSTOMER WHERE Email LIKE '%@mail.com';    -- An, Binh, Dung, Phuong
```

**IS NULL / IS NOT NULL**
```sql
SELECT CustName FROM CUSTOMER WHERE Email IS NULL AND City = 'Ho Chi Minh';   -- Hoang Van Em
SELECT COUNT(*) FROM CUSTOMER WHERE Email IS NOT NULL;                        -- 4
SELECT CustName FROM CUSTOMER WHERE Email <=> NULL;                           -- Cuong, Em (toán tử an toàn với NULL)
```

**AND / OR / NOT**
```sql
SELECT ProdName FROM PRODUCT WHERE NOT (Price > 1000);        -- Mouse, Headphone, USB, Webcam
SELECT ProdName, Price, Stock FROM PRODUCT
WHERE (Category = 'Electronics' AND Price < 10000) OR Stock >= 100;
```
→ Monitor (4000), Smartphone (9000), Mouse (tồn 100), USB (tồn 200). Laptop (15000, tồn 20) không thỏa cả hai vế.

### 4.15. Khi nào dùng toán tử nào (nhận dạng đề)

| Đề nói... | Dùng |
|---|---|
| "khác nhau", "không trùng" | `DISTINCT` |
| "từ ... đến ..." | `BETWEEN` |
| "một trong các", "thuộc danh sách" | `IN` |
| "không thuộc", "ngoại trừ" | `NOT IN` / `<>` |
| "bắt đầu bằng", "chứa", "kết thúc bằng" | `LIKE 'x%'`, `'%x%'`, `'%x'` |
| "chưa có", "để trống", "không có email" | `IS NULL` |
| "đã có" | `IS NOT NULL` |
| "đồng thời", "và" | `AND` |
| "hoặc" | `OR` (nhớ ngoặc khi trộn với `AND`) |
| "N đầu tiên", "mới nhất" | `ORDER BY ... DESC LIMIT N` |
| "trang thứ p" | `LIMIT n OFFSET (p-1)*n` |

### 4.16. Bài tập tự luyện bổ sung Chương 4

1. Sản phẩm có tên chứa `phone` **hoặc** giá từ 4000 đến 9000, sắp theo giá giảm dần.
2. Khách chưa có email và đăng ký sau 2024-04-01.
3. Đơn không phải COMPLETED và có tổng từ 5000 trở lên.
4. Trang thứ 2 (mỗi trang 3 dòng) của danh sách sản phẩm sắp theo `ProdID`.

<details><summary>Đáp án</summary>

```sql
-- 1  → Smartphone 9000, Monitor 4000, Headphone 800
SELECT ProdName, Price FROM PRODUCT
WHERE ProdName LIKE '%phone%' OR Price BETWEEN 4000 AND 9000
ORDER BY Price DESC;

-- 2  → Hoang Van Em (2024-06-18). Le Van Cuong (2024-03-20) không thỏa ngày.
SELECT CustName, JoinDate FROM CUSTOMER
WHERE Email IS NULL AND JoinDate > '2024-04-01';

-- 3  → đơn 4 (CANCELLED, 15000) và đơn 10 (PENDING, 9000); đơn 6 (1600) bị loại
SELECT OrderID, Status, TotalAmount FROM SALEORDER
WHERE Status <> 'COMPLETED' AND TotalAmount >= 5000;

-- 4  → Monitor (4), Headphone (5), USB (6)
SELECT ProdID, ProdName FROM PRODUCT ORDER BY ProdID LIMIT 3 OFFSET 3;
```
</details>

---

## CHƯƠNG 5: CÁC HÀM TRONG MYSQL

**Hàm (function)** là một "cái máy nhỏ": đưa vào giá trị, nhận ra giá trị mới. Ví dụ `UPPER('an')` → `'AN'`.

Hàm dùng được ở `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY`, `HAVING`, `UPDATE ... SET`. Có thể **lồng hàm vào nhau**: hàm trong cùng chạy trước.

Để thử nhanh mọi hàm không cần bảng: `SELECT UPPER('an');`.

### 5.A. HÀM XỬ LÝ CHUỖI

| Hàm | Công dụng | Ví dụ | Kết quả |
|---|---|---|---|
| `CONCAT(a, b, ...)` | Nối chuỗi | `CONCAT('Nguyen', ' ', 'An')` | `Nguyen An` |
| `CONCAT_WS(sep, a, b, ...)` | Nối với dấu ngăn cách, **bỏ qua NULL** | `CONCAT_WS(', ', 'Ha Noi', NULL, 'VN')` | `Ha Noi, VN` |
| `UPPER(s)` / `LOWER(s)` | Viết hoa / thường | `UPPER('an')` | `AN` |
| `LEFT(s, n)` | n ký tự đầu | `LEFT('Laptop Dell', 6)` | `Laptop` |
| `RIGHT(s, n)` | n ký tự cuối | `RIGHT('0901000001', 4)` | `0001` |
| `SUBSTRING(s, vị_trí, độ_dài)` | Cắt chuỗi (vị trí tính từ **1**) | `SUBSTRING('Laptop Dell', 8, 4)` | `Dell` |
| `LENGTH(s)` | Độ dài tính bằng **byte** | `LENGTH('Việt')` | `6` |
| `CHAR_LENGTH(s)` | Độ dài tính bằng **ký tự** | `CHAR_LENGTH('Việt')` | `4` |
| `TRIM(s)` / `LTRIM` / `RTRIM` | Bỏ khoảng trắng 2 đầu / trái / phải | `TRIM('  abc  ')` | `abc` |
| `REPLACE(s, cũ, mới)` | Thay thế | `REPLACE('Ha Noi', ' ', '-')` | `Ha-Noi` |
| `LOCATE(tìm, s)` | Vị trí xuất hiện đầu tiên (0 nếu không có) | `LOCATE('Van', 'Nguyen Van An')` | `8` |
| `SUBSTRING_INDEX(s, sep, n)` | Lấy phần trước dấu phân cách thứ n (n âm: lấy từ cuối) | `SUBSTRING_INDEX('an@mail.com', '@', 1)` | `an` |

**Ví dụ thực tế:**
```sql
SELECT CustName,
       UPPER(CustName)                      AS TenHoa,
       SUBSTRING_INDEX(CustName, ' ', -1)   AS Ten,
       COALESCE(SUBSTRING_INDEX(Email, '@', -1), 'N/A') AS TenMien
FROM CUSTOMER;
```
| CustName | TenHoa | Ten | TenMien |
|---|---|---|---|
| Nguyen Van An | NGUYEN VAN AN | An | mail.com |
| Tran Thi Binh | TRAN THI BINH | Binh | mail.com |
| Le Van Cuong | LE VAN CUONG | Cuong | N/A |
| Pham Thi Dung | PHAM THI DUNG | Dung | mail.com |
| Hoang Van Em | HOANG VAN EM | Em | N/A |
| Vu Thi Phuong | VU THI PHUONG | Phuong | mail.com |

Giải thích: `SUBSTRING_INDEX(CustName, ' ', -1)` lấy phần **sau dấu cách cuối cùng** = tên riêng. Với khách không có email, `SUBSTRING_INDEX(NULL, ...)` là `NULL`, nên `COALESCE` thay bằng `'N/A'`.

**Kết hợp:** tách họ: `LEFT(CustName, LOCATE(' ', CustName) - 1)` → `Nguyen`, `Tran`, `Le`, `Pham`, `Hoang`, `Vu`.

**Lỗi / hiểu nhầm phổ biến:**
- `CONCAT('A', NULL, 'B')` → **NULL** (một NULL làm hỏng cả chuỗi). Dùng `CONCAT_WS` hoặc `CONCAT('A', IFNULL(x,''), 'B')`.
- `'a' + 'b'` ❌ **không nối chuỗi** trong MySQL (nó cộng số, ra 0). Phải dùng `CONCAT`. (SQL Server thì `+` nối được.)
- `SUBSTRING` đếm từ **1**, không phải 0 như Python.
- `LENGTH` cho tiếng Việt có dấu ra số byte, thường lớn hơn số ký tự. Muốn đếm chữ dùng `CHAR_LENGTH`.
- Muốn tìm kiếm không phân biệt khoảng trắng thừa: `WHERE TRIM(CustName) = 'An'`.

### 5.B. HÀM SỐ HỌC

| Hàm | Công dụng | Ví dụ | Kết quả |
|---|---|---|---|
| `ABS(x)` | Giá trị tuyệt đối | `ABS(-5)` | `5` |
| `ROUND(x, d)` | Làm tròn d chữ số thập phân | `ROUND(3.14159, 2)` | `3.14` |
| `ROUND(x)` | Làm tròn nguyên | `ROUND(1234.5)` | `1235` |
| `ROUND(x, -2)` | Làm tròn hàng trăm | `ROUND(1234, -2)` | `1200` |
| `CEIL(x)` | Làm tròn **lên** | `CEIL(4.1)` | `5` |
| `FLOOR(x)` | Làm tròn **xuống** | `FLOOR(4.9)` | `4` |
| `MOD(a, b)` hoặc `a % b` | Chia lấy dư | `MOD(10, 3)` | `1` |
| `POWER(a, b)` | Lũy thừa | `POWER(2, 10)` | `1024` |
| `SQRT(x)` | Căn bậc hai | `SQRT(144)` | `12` |

**Ví dụ thực tế:**
```sql
-- Giá sau khi tăng VAT 8%, làm tròn đến hàng đơn vị
SELECT ProdName, Price, ROUND(Price * 1.08) AS PriceVAT
FROM PRODUCT
WHERE Category = 'Electronics';
```
| ProdName | Price | PriceVAT |
|---|---|---|
| Laptop Dell | 15000.00 | 16200 |
| Monitor 24 inch | 4000.00 | 4320 |
| Smartphone | 9000.00 | 9720 |

**Phép chia:** `7 / 2` ra `3.5000`; muốn chia nguyên dùng `7 DIV 2` → `3`. **Khác biệt:** SQL Server `7/2` = 3 (chia nguyên với số nguyên).

**Hiểu nhầm:** `CEIL(-4.1)` = `-4` (lên về phía dương), `FLOOR(-4.1)` = `-5`. `ROUND` với số `.5`: số chính xác (DECIMAL) làm tròn **ra xa số 0** (`2.5 → 3`), còn FLOAT/DOUBLE có thể khác.

Dạng bài hay gặp dùng `MOD`: tìm số chẵn/lẻ: `WHERE MOD(OrderID, 2) = 0` → đơn 2, 4, 6, 8, 10, 12.

### 5.C. HÀM TỔNG HỢP (AGGREGATE)

Hàm tổng hợp **nén nhiều dòng thành một giá trị**.

| Hàm | Công dụng | Bỏ qua NULL? |
|---|---|---|
| `COUNT(*)` | Đếm **số dòng** | Không (đếm cả dòng toàn NULL) |
| `COUNT(cột)` | Đếm số dòng mà `cột` **không NULL** | Có |
| `COUNT(DISTINCT cột)` | Đếm số giá trị **khác nhau** (không NULL) | Có |
| `SUM(cột)` | Tổng | Có |
| `AVG(cột)` | Trung bình = SUM / số giá trị không NULL | Có |
| `MIN(cột)` / `MAX(cột)` | Nhỏ nhất / lớn nhất | Có |

```sql
SELECT COUNT(*)              AS SoKhach,
       COUNT(Email)          AS CoEmail,
       COUNT(DISTINCT City)  AS SoThanhPho
FROM CUSTOMER;
```
| SoKhach | CoEmail | SoThanhPho |
|---|---|---|
| 6 | 4 | 4 |

```sql
SELECT COUNT(*) AS SoDon, SUM(TotalAmount) AS TongTien, AVG(TotalAmount) AS TrungBinh,
       MIN(TotalAmount) AS NhoNhat, MAX(TotalAmount) AS LonNhat
FROM SALEORDER;
```
| SoDon | TongTien | TrungBinh | NhoNhat | LonNhat |
|---|---|---|---|---|
| 12 | 161700.00 | 13475.000000 | 1600.00 | 30300.00 |

Chỉ tính đơn đã hoàn thành: `WHERE Status = 'COMPLETED'` → `SoDon = 9`, `TongTien = 136100.00`.

**Bẫy quan trọng:**
1. **Không dùng hàm tổng hợp trong `WHERE`** (`WHERE SUM(x) > 5` ❌). Dùng `HAVING` (Chương 7).
2. Không trộn cột thường với hàm tổng hợp nếu không có `GROUP BY`: `SELECT CustName, COUNT(*) FROM CUSTOMER` ❌ (lỗi 1140 với `ONLY_FULL_GROUP_BY` mặc định).
3. `SUM` của tập rỗng là **NULL**, không phải 0 → dùng `COALESCE(SUM(x), 0)`. `COUNT` của tập rỗng là 0.
4. `AVG` bỏ qua NULL: nếu 4 người có điểm và 2 người NULL thì chia cho 4, không phải 6.

### 5.D. HÀM XỬ LÝ NULL

| Hàm | Công dụng | Ví dụ | Kết quả |
|---|---|---|---|
| `IFNULL(a, b)` | Nếu a NULL thì lấy b | `IFNULL(NULL, 'N/A')` | `N/A` |
| `COALESCE(a, b, c, ...)` | Lấy giá trị **đầu tiên không NULL** | `COALESCE(NULL, NULL, 5)` | `5` |
| `NULLIF(a, b)` | Nếu a = b thì NULL, ngược lại a | `NULLIF(0, 0)` | `NULL` |

```sql
SELECT CustName, COALESCE(Email, Phone) AS LienHe FROM CUSTOMER;
```
| CustName | LienHe |
|---|---|
| Nguyen Van An | an@mail.com |
| Le Van Cuong | 0901000003 |
| Hoang Van Em | 0901000005 |
| ... | ... |

`NULLIF` thường dùng để **tránh chia cho 0**: `Price / NULLIF(Stock, 0)` trả NULL thay vì lỗi/NULL ngầm khi `Stock = 0`.

`IFNULL` chỉ nhận 2 tham số và là hàm riêng của MySQL; `COALESCE` là chuẩn SQL, nhận nhiều tham số, dùng được ở mọi hệ → **nên ưu tiên COALESCE**.

### 5.E. HÀM ĐIỀU KIỆN: IF và CASE WHEN

**IF(điều_kiện, giá_trị_đúng, giá_trị_sai)** (riêng MySQL):
```sql
SELECT ProdName, IF(Price >= 5000, 'Cao cap', 'Binh dan') AS PhanKhuc FROM PRODUCT;
```

**CASE WHEN** (chuẩn SQL, mạnh hơn):

Dạng 1: điều kiện tổng quát
```sql
CASE WHEN dk1 THEN kq1
     WHEN dk2 THEN kq2
     ELSE kq_mac_dinh
END
```
Dạng 2: so sánh bằng một biểu thức
```sql
CASE Status WHEN 'COMPLETED' THEN 'Hoan thanh' WHEN 'PENDING' THEN 'Cho xu ly' ELSE 'Huy' END
```

**a) CASE trong SELECT – phân loại đơn hàng:**
```sql
SELECT OrderID, TotalAmount,
       CASE WHEN TotalAmount >= 20000 THEN 'LON'
            WHEN TotalAmount >= 10000 THEN 'VUA'
            ELSE 'NHO' END AS LoaiDon
FROM SALEORDER;
```
| OrderID | TotalAmount | LoaiDon |
|---|---|---|
| 1 | 15600.00 | VUA |
| 2 | 9200.00 | NHO |
| 3 | 18800.00 | VUA |
| 4 | 15000.00 | VUA |
| 5 | 30300.00 | LON |
| 6 | 1600.00 | NHO |
| 7 | 13000.00 | VUA |
| 8 | 4500.00 | NHO |
| 9 | 19000.00 | VUA |
| 10 | 9000.00 | NHO |
| 11 | 1700.00 | NHO |
| 12 | 24000.00 | LON |

**b) CASE trong ORDER BY – thứ tự tùy chỉnh:**
```sql
SELECT OrderID, Status FROM SALEORDER
ORDER BY CASE Status WHEN 'COMPLETED' THEN 1 WHEN 'PENDING' THEN 2 ELSE 3 END, OrderID;
```
Đơn COMPLETED xếp trước, rồi PENDING, cuối cùng CANCELLED.

**c) CASE trong UPDATE:** xem Chương 3, mục 3.2.

**d) CASE bên trong hàm tổng hợp (kỹ thuật cực hữu ích – "tổng có điều kiện"):**
```sql
SELECT SUM(CASE WHEN Status = 'COMPLETED' THEN TotalAmount ELSE 0 END) AS DoanhThuHoanThanh,
       SUM(CASE WHEN Status = 'PENDING'   THEN TotalAmount ELSE 0 END) AS DangCho,
       COUNT(CASE WHEN Status = 'CANCELLED' THEN 1 END)                AS SoDonHuy
FROM SALEORDER;
```
| DoanhThuHoanThanh | DangCho | SoDonHuy |
|---|---|---|
| 136100.00 | 10600.00 | 1 |

Giải thích: `CASE` biến mỗi dòng thành số (hoặc NULL); `SUM`/`COUNT` cộng lại. `COUNT(CASE WHEN ... THEN 1 END)` đếm các dòng thỏa (vì nhánh không thỏa trả NULL, `COUNT` bỏ qua NULL).

**Lỗi thường gặp:** quên `END`; quên `ELSE` (không khớp nhánh nào → NULL); điều kiện chồng lấp nên đặt nhánh **hẹp nhất lên trước**.

### 5.F. HÀM NGÀY THÁNG

| Hàm | Công dụng | Ví dụ | Kết quả |
|---|---|---|---|
| `NOW()` | Ngày giờ hiện tại | `NOW()` | `2026-10-22 09:30:00` (tùy lúc chạy) |
| `CURDATE()` | Ngày hiện tại | `CURDATE()` | `2026-10-22` |
| `CURTIME()` | Giờ hiện tại | `CURTIME()` | `09:30:00` |
| `YEAR(d)` `MONTH(d)` `DAY(d)` | Lấy năm / tháng / ngày | `MONTH('2025-07-07')` | `7` |
| `DATEDIFF(d1, d2)` | Số **ngày** d1 − d2 | `DATEDIFF('2025-07-07','2025-01-05')` | `183` |
| `TIMESTAMPDIFF(đơn_vị, d1, d2)` | d2 − d1 theo đơn vị (YEAR, MONTH, DAY, HOUR...) | `TIMESTAMPDIFF(YEAR,'2000-05-20','2025-05-19')` | `24` |
| `DATE_ADD(d, INTERVAL n đơn_vị)` | Cộng thời gian | `DATE_ADD('2025-01-31', INTERVAL 1 MONTH)` | `2025-02-28` |
| `DATE_SUB(d, INTERVAL n đơn_vị)` | Trừ thời gian | `DATE_SUB('2025-03-01', INTERVAL 7 DAY)` | `2025-02-22` |
| `DATE_FORMAT(d, định_dạng)` | Định dạng hiển thị | `DATE_FORMAT('2025-07-07','%d/%m/%Y')` | `07/07/2025` |

Ký hiệu định dạng thường dùng: `%Y` năm 4 số, `%y` 2 số, `%m` tháng 01–12, `%d` ngày 01–31, `%H` giờ 0–23, `%i` phút, `%s` giây, `%M` tên tháng, `%W` tên thứ.

**Ví dụ thực tế:**
```sql
-- Đơn hàng tháng 5/2025 (cách dễ đọc, nhưng chậm trên bảng lớn)
SELECT OrderID, OrderDate FROM SALEORDER
WHERE YEAR(OrderDate) = 2025 AND MONTH(OrderDate) = 5;     -- đơn 8, 9

-- Cách tốt hơn: dùng khoảng, tận dụng được chỉ mục
SELECT OrderID, OrderDate FROM SALEORDER
WHERE OrderDate >= '2025-05-01' AND OrderDate < '2025-06-01';

-- Hiển thị ngày kiểu Việt Nam + số ngày từ lúc đặt đến 01/08/2025
SELECT OrderID,
       DATE_FORMAT(OrderDate, '%d/%m/%Y')       AS NgayDat,
       DATEDIFF('2025-08-01', OrderDate)         AS SoNgayDaQua
FROM SALEORDER
WHERE OrderID = 12;
```
| OrderID | NgayDat | SoNgayDaQua |
|---|---|---|
| 12 | 07/07/2025 | 25 |

**Lỗi / hiểu nhầm:**
- `DATEDIFF(a, b)` = **a − b**; đảo thứ tự ra số âm.
- Tính tuổi bằng `YEAR(NOW()) - YEAR(BirthDate)` **sai** nếu chưa tới sinh nhật. Dùng `TIMESTAMPDIFF(YEAR, BirthDate, CURDATE())` (tính đủ năm trọn).
- `DATE_ADD('2025-01-31', INTERVAL 1 MONTH)` ra `2025-02-28` (MySQL tự lùi về ngày cuối tháng).
- **Khác biệt:** SQL Server dùng `GETDATE()`, `DATEADD()`, `DATEDIFF(day, a, b)` (thứ tự tham số khác!). PostgreSQL dùng `CURRENT_DATE`, `AGE()`.

### 5.G. CÁC HÀM HỮU ÍCH KHÁC

| Hàm | Công dụng | Ví dụ | Kết quả |
|---|---|---|---|
| `CAST(x AS kiểu)` | Ép kiểu (chuẩn SQL) | `CAST('123' AS UNSIGNED)` | `123` |
| `CAST(x AS DATE)` | Chuỗi → ngày | `CAST('2025-01-05' AS DATE)` | `2025-01-05` |
| `CAST(x AS DECIMAL(10,2))` | Ép sang số thập phân | `CAST('12.345' AS DECIMAL(10,2))` | `12.35` |
| `CONVERT(x, kiểu)` | Ép kiểu (cú pháp MySQL/SQL Server) | `CONVERT('123', SIGNED)` | `123` |
| `GREATEST(a, b, ...)` | Lớn nhất trong danh sách giá trị | `GREATEST(3, 9, 5)` | `9` |
| `LEAST(a, b, ...)` | Nhỏ nhất trong danh sách | `LEAST(3, 9, 5)` | `3` |

Kiểu dùng được trong `CAST`/`CONVERT` của MySQL: `SIGNED`, `UNSIGNED`, `DECIMAL(p,s)`, `CHAR`, `DATE`, `DATETIME`, `TIME`.

**Phân biệt hàm tổng hợp và `GREATEST/LEAST`:** `MAX/MIN` so sánh **giữa các dòng** của một cột; `GREATEST/LEAST` so sánh **giữa các cột/giá trị trên cùng một dòng**.
```sql
SELECT ProdName, GREATEST(Price, 1000) AS GiaToiThieu1000 FROM PRODUCT LIMIT 3;
```
| ProdName | GiaToiThieu1000 |
|---|---|
| Laptop Dell | 15000.00 |
| Mouse Logitech | 1000.00 |
| Keyboard Mechanical | 1200.00 |

**Lỗi:** `GREATEST(1, NULL, 3)` → **NULL** (một NULL làm cả kết quả NULL). `CAST('abc' AS UNSIGNED)` → 0 kèm cảnh báo (không lỗi); `CAST('12abc' AS UNSIGNED)` → 12.

### 5.H. Khi nào dùng hàm nào (nhận dạng đề bài)

| Đề bài nói... | Gợi ý hàm |
|---|---|
| "ghép họ và tên", "địa chỉ đầy đủ" | `CONCAT`, `CONCAT_WS` |
| "lấy 3 ký tự đầu", "tên miền email" | `LEFT`, `SUBSTRING_INDEX` |
| "làm tròn", "lên/xuống số nguyên" | `ROUND`, `CEIL`, `FLOOR` |
| "chưa có giá trị thì hiển thị..." | `COALESCE`, `IFNULL` |
| "phân loại", "xếp hạng thành nhóm", "nếu ... thì ..." | `CASE WHEN` |
| "trong tháng/năm", "N ngày gần nhất" | `YEAR/MONTH`, `DATE_SUB`, `CURDATE` |
| "đã bao nhiêu ngày/tuổi" | `DATEDIFF`, `TIMESTAMPDIFF` |
| "số lượng", "tổng", "trung bình" | `COUNT`, `SUM`, `AVG` |

### 5.I. Bài tập tự luyện Chương 5

1. Hiển thị mỗi khách: tên viết hoa, và 4 số cuối điện thoại.
2. Hiển thị `ProdName`, `Price`, và cột `NhomGia`: `'Re'` (<500), `'Trung binh'` (500–5000), `'Dat'` (>5000).
3. Đếm số đơn `COMPLETED` đặt vào tháng 2/2025.
4. Với mỗi nhân viên, hiển thị tên và số năm làm việc tính đến `2025-12-31` (năm trọn).

<details><summary>Đáp án</summary>

```sql
-- 1
SELECT UPPER(CustName) AS Ten, RIGHT(Phone, 4) AS DuoiSDT FROM CUSTOMER;

-- 2  (Webcam 700 → Trung binh; Keyboard 1200 → Trung binh; Smartphone 9000 → Dat)
SELECT ProdName, Price,
       CASE WHEN Price < 500   THEN 'Re'
            WHEN Price <= 5000 THEN 'Trung binh'
            ELSE 'Dat' END AS NhomGia
FROM PRODUCT;

-- 3  → 2 (đơn 2 và đơn 3)
SELECT COUNT(*) AS SoDon FROM SALEORDER
WHERE Status = 'COMPLETED'
  AND OrderDate >= '2025-02-01' AND OrderDate < '2025-03-01';

-- 4  → Quan 5, Ha 4, Huy 3, Lan 2, Minh 1
SELECT EmpName, TIMESTAMPDIFF(YEAR, HireDate, '2025-12-31') AS SoNam FROM EMPLOYEE;
```
Kiểm tra câu 4: Quan vào làm 2020-01-15 → đến 2025-12-31 là 5 năm trọn; Ha (2021-03-01) → 4; Huy (2022-06-10) → 3; Lan (2023-02-20) → 2; Minh (2024-01-08) → 1.
</details>

---

### 5.J. CHI TIẾT TỪNG HÀM (đủ công dụng, cú pháp, ví dụ đơn giản, ví dụ kết hợp, kết quả, lỗi, khi nào dùng)

> Mỗi hàm theo mẫu: **Công dụng · Cú pháp · Ví dụ đơn giản · Ví dụ kết hợp · Lỗi/hiểu nhầm · Khi nào dùng.** Ví dụ chạy được trên `shop_db`.

#### A. Hàm chuỗi

**CONCAT**
- **Công dụng:** nối nhiều chuỗi thành một.
- **Cú pháp:** `CONCAT(chuoi1, chuoi2, ...)`
- **Đơn giản:** `SELECT CONCAT('Nguyen', ' ', 'An');` → `Nguyen An`
- **Kết hợp:** `SELECT CONCAT(CustName, ' (', City, ')') FROM CUSTOMER WHERE CustID = 1;` → `Nguyen Van An (Ha Noi)`
- **Lỗi:** chỉ cần **một** đối số NULL thì cả kết quả NULL (`CONCAT('A', NULL)` → `NULL`); số được tự đổi sang chuỗi.
- **Khi nào dùng:** ghép họ + tên, địa chỉ đầy đủ, tạo mã/nhãn hiển thị.

**CONCAT_WS**
- **Công dụng:** nối có dấu ngăn cách, **bỏ qua NULL**.
- **Cú pháp:** `CONCAT_WS(dau_ngan, chuoi1, chuoi2, ...)`
- **Đơn giản:** `SELECT CONCAT_WS(', ', 'Ha Noi', 'VN');` → `Ha Noi, VN`
- **Kết hợp:** `SELECT CONCAT_WS(' - ', CustName, Email, City) FROM CUSTOMER WHERE CustID = 3;` → `Le Van Cuong - Da Nang` (Email NULL bị bỏ, không dư dấu ngăn cách)
- **Lỗi:** NULL ở **dấu ngăn cách** (tham số đầu) thì kết quả NULL.
- **Khi nào dùng:** ghép các trường có thể thiếu (địa chỉ nhiều phần, họ-đệm-tên).

**UPPER / LOWER**
- **Công dụng:** đổi toàn bộ sang chữ hoa / chữ thường.
- **Cú pháp:** `UPPER(s)`, `LOWER(s)`
- **Đơn giản:** `SELECT UPPER('an'), LOWER('AN');` → `AN`, `an`
- **Kết hợp:** `SELECT UPPER(LEFT(ProdName, 3)) FROM PRODUCT WHERE ProdID = 1;` → `LAP`
- **Lỗi:** so sánh `=` trong MySQL mặc định **không phân biệt hoa/thường**, không cần `LOWER()` để so khớp. Dùng `LOWER` để **hiển thị/chuẩn hóa**.
- **Khi nào dùng:** chuẩn hóa dữ liệu, tạo mã viết hoa.

**LEFT / RIGHT**
- **Công dụng:** lấy n ký tự đầu / cuối.
- **Cú pháp:** `LEFT(s, n)`, `RIGHT(s, n)`
- **Đơn giản:** `SELECT LEFT('Laptop Dell', 6), RIGHT('0901000001', 4);` → `Laptop`, `0001`
- **Kết hợp (che số điện thoại):** `SELECT CONCAT(LEFT(Phone, 4), '***', RIGHT(Phone, 3)) FROM CUSTOMER WHERE CustID = 1;` → `0901***001`
- **Lỗi:** n lớn hơn độ dài chuỗi thì trả cả chuỗi (không lỗi); n = 0 trả chuỗi rỗng.
- **Khi nào dùng:** lấy tiền tố/hậu tố cố định (mã vùng, 4 số cuối).

**SUBSTRING**
- **Công dụng:** cắt một đoạn chuỗi.
- **Cú pháp:** `SUBSTRING(s, vi_tri [, do_dai])`; vị trí tính từ **1**; vị trí âm đếm từ cuối.
- **Đơn giản:** `SUBSTRING('Laptop Dell', 8, 4)` → `Dell`; `SUBSTRING('Laptop', -3)` → `top`
- **Kết hợp (lấy phần sau dấu cách đầu):** `SELECT SUBSTRING(ProdName, LOCATE(' ', ProdName) + 1) FROM PRODUCT WHERE ProdID = 3;` → `Mechanical`
- **Lỗi:** quen index từ 0 như Python → lệch 1 ký tự; vị trí 0 trả chuỗi rỗng.
- **Khi nào dùng:** tách một đoạn theo vị trí.

**LENGTH / CHAR_LENGTH**
- **Công dụng:** độ dài tính bằng **byte** / bằng **ký tự**.
- **Cú pháp:** `LENGTH(s)`, `CHAR_LENGTH(s)`
- **Đơn giản:** `SELECT LENGTH('Hà Nội'), CHAR_LENGTH('Hà Nội');` → `9`, `6`
- **Kết hợp:** `SELECT CustName FROM CUSTOMER WHERE CHAR_LENGTH(CustName) > 12;` → An, Binh, Dung, Phuong (tên 13 ký tự)
- **Lỗi:** dùng `LENGTH` cho tiếng Việt có dấu ra số lớn hơn số chữ.
- **Khi nào dùng:** kiểm tra độ dài hợp lệ (`CHAR_LENGTH`), ước lượng dung lượng (`LENGTH`).

**TRIM / LTRIM / RTRIM**
- **Công dụng:** bỏ khoảng trắng (hoặc ký tự chỉ định) ở hai đầu / đầu / cuối.
- **Cú pháp:** `TRIM(s)`, `LTRIM(s)`, `RTRIM(s)`, `TRIM(LEADING '0' FROM s)`
- **Đơn giản:** `TRIM('  Ha Noi  ')` → `Ha Noi`; `TRIM(LEADING '0' FROM '000123')` → `123`
- **Kết hợp:** `SELECT * FROM CUSTOMER WHERE TRIM(City) = 'Ha Noi';` (khớp cả khi dữ liệu có khoảng trắng thừa)
- **Lỗi:** `TRIM` không bỏ khoảng trắng ở **giữa** chuỗi (dùng `REPLACE`).
- **Khi nào dùng:** làm sạch dữ liệu nhập tay trước khi so sánh/nhóm.

**REPLACE**
- **Công dụng:** thay mọi lần xuất hiện của chuỗi con.
- **Cú pháp:** `REPLACE(s, cu, moi)`
- **Đơn giản:** `REPLACE('Ha Noi', ' ', '-')` → `Ha-Noi`
- **Kết hợp:** `SELECT REPLACE(LOWER(City), ' ', '-') FROM CUSTOMER WHERE CustID = 2;` → `ho-chi-minh`
- **Lỗi:** phân biệt hoa/thường theo collation; thay **mọi** vị trí, không chỉ vị trí đầu.
- **Khi nào dùng:** đổi định dạng, xóa ký tự (`REPLACE(s, ' ', '')`).

**LOCATE**
- **Công dụng:** vị trí xuất hiện đầu tiên của chuỗi con (0 nếu không có).
- **Cú pháp:** `LOCATE(tim, s [, bat_dau_tu])`
- **Đơn giản:** `LOCATE('Van', 'Nguyen Van An')` → `8`; `LOCATE('a', 'banana', 3)` → `4`; `LOCATE('z', 'Hoang')` → `0`
- **Kết hợp (lấy họ):** `LEFT(CustName, LOCATE(' ', CustName) - 1)` → `Nguyen` cho khách 1
- **Lỗi:** thứ tự tham số là (cần tìm, trong chuỗi) — **ngược** với `INSTR(s, tim)`; không tìm thấy thì ra 0, `LEFT(..., 0 - 1)` sẽ lỗi logic.
- **Khi nào dùng:** xác định vị trí để cắt chuỗi, kiểm tra có chứa hay không (`LOCATE(...) > 0`).

**SUBSTRING_INDEX**
- **Công dụng:** lấy phần chuỗi trước (n dương) / sau (n âm) dấu phân cách thứ n.
- **Cú pháp:** `SUBSTRING_INDEX(s, dau_phan_cach, n)`
- **Đơn giản:** `SUBSTRING_INDEX('an@mail.com', '@', 1)` → `an`; `SUBSTRING_INDEX('an@mail.com', '@', -1)` → `mail.com`
- **Kết hợp:** `SUBSTRING_INDEX(CustName, ' ', 2)` → `Nguyen Van` (hai từ đầu); `SUBSTRING_INDEX(CustName, ' ', -1)` → `An` (từ cuối)
- **Lỗi:** không có dấu phân cách trong chuỗi thì trả **toàn bộ chuỗi**.
- **Khi nào dùng:** tách email, họ/tên theo dấu cách, tách đường dẫn.

#### B. Hàm số học

**ABS**
- **Công dụng:** giá trị tuyệt đối. **Cú pháp:** `ABS(x)`
- **Đơn giản:** `ABS(-300)` → `300`
- **Kết hợp (độ lệch giá so với mốc 1000):** `SELECT ProdName, ABS(Price - 1000) AS DoLech FROM PRODUCT WHERE ProdID IN (1, 3);` → Laptop 14000; Keyboard 200
- **Lỗi:** `ABS(NULL)` = NULL.
- **Khi nào dùng:** khoảng cách/độ lệch không quan tâm dấu.

**ROUND**
- **Công dụng:** làm tròn. **Cú pháp:** `ROUND(x [, so_chu_so])` (số âm làm tròn hàng chục/trăm...)
- **Đơn giản:** `ROUND(2.567, 1)` → `2.6`; `ROUND(1234, -2)` → `1200`
- **Kết hợp:** `SELECT ROUND(1200 / 7, 2);` → `171.43`; `SELECT ROUND(AVG(Price), 2) FROM PRODUCT;` → `3906.25`
- **Lỗi:** `ROUND` chỉ để **hiển thị/tính**, không đổi dữ liệu lưu; DECIMAL làm tròn ra xa số 0 (`2.5 → 3`), FLOAT có thể khác.
- **Khi nào dùng:** hiển thị tiền, phần trăm, trung bình.

**CEIL / FLOOR**
- **Công dụng:** làm tròn lên / xuống số nguyên. **Cú pháp:** `CEIL(x)`, `FLOOR(x)`
- **Đơn giản:** `CEIL(4.1)` → `5`; `FLOOR(4.9)` → `4`; `CEIL(-4.1)` → `-4`; `FLOOR(-4.1)` → `-5`
- **Kết hợp (số thùng 30 món để chứa hết tồn kho):** `SELECT ProdName, CEIL(Stock / 30) AS SoThung FROM PRODUCT WHERE ProdID IN (1, 2);` → Laptop 1; Mouse 4
- **Lỗi:** quên số âm (`CEIL` hướng về +∞, không phải "xa 0").
- **Khi nào dùng:** đề nói "làm tròn lên" (số trang, số xe, số thùng), "phần nguyên" (`FLOOR`).

**MOD**
- **Công dụng:** phần dư của phép chia. **Cú pháp:** `MOD(a, b)` hoặc `a % b`
- **Đơn giản:** `MOD(10, 3)` → `1`
- **Kết hợp:** `SELECT CustName FROM CUSTOMER WHERE MOD(CustID, 2) = 0;` → Binh, Dung, Phuong
- **Lỗi:** `MOD(x, 0)` trả NULL.
- **Khi nào dùng:** chẵn/lẻ, chia nhóm luân phiên, kiểm tra chia hết.

**POWER**
- **Công dụng:** lũy thừa. **Cú pháp:** `POWER(co_so, so_mu)`
- **Đơn giản:** `POWER(2, 3)` → `8`
- **Kết hợp (lãi kép 5%/năm, 2 năm):** `SELECT ROUND(10000 * POWER(1.05, 2), 2);` → `11025.00`
- **Lỗi:** số mũ phân số/âm ra số thực; số rất lớn có thể tràn.
- **Khi nào dùng:** lãi kép, bình phương.

**SQRT**
- **Công dụng:** căn bậc hai. **Cú pháp:** `SQRT(x)`
- **Đơn giản:** `SQRT(16)` → `4`
- **Kết hợp:** `SELECT ROUND(SQRT(POWER(3, 2) + POWER(4, 2)), 0);` → `5`
- **Lỗi:** `SQRT` số âm trả NULL.
- **Khi nào dùng:** khoảng cách, độ lệch chuẩn.

#### C. Hàm tổng hợp

**COUNT**
- **Công dụng:** đếm. **Cú pháp:** `COUNT(*)`, `COUNT(cot)`, `COUNT(DISTINCT cot)`
- **Đơn giản:** `SELECT COUNT(*) FROM SALEORDER;` → `12`; `SELECT COUNT(Email) FROM CUSTOMER;` → `4`
- **Kết hợp:** `SELECT COUNT(*) FROM SALEORDER WHERE Status = 'COMPLETED';` → `9`; `SELECT COUNT(DISTINCT CustID) FROM SALEORDER;` → `5`; `SELECT COUNT(DISTINCT Category) FROM PRODUCT;` → `2`
- **Lỗi:** `COUNT(cot)` bỏ NULL còn `COUNT(*)` thì không; `COUNT(DISTINCT a, b)` đếm tổ hợp.
- **Khi nào dùng:** "bao nhiêu", "số lượng", "có bao nhiêu loại".

**SUM**
- **Công dụng:** tổng. **Cú pháp:** `SUM(bieu_thuc)`
- **Đơn giản:** `SELECT SUM(Stock) FROM PRODUCT;` → `480`
- **Kết hợp:** `SELECT SUM(Price * Stock) FROM PRODUCT;` → `827500.00` (giá trị tồn kho)
- **Lỗi:** tập rỗng ra NULL (dùng `COALESCE(SUM(x), 0)`); bỏ qua NULL từng dòng; nhân dòng khi JOIN.
- **Khi nào dùng:** "tổng", "doanh thu", "tổng số lượng".

**AVG**
- **Công dụng:** trung bình cộng (bỏ NULL). **Cú pháp:** `AVG(bieu_thuc)`
- **Đơn giản:** `SELECT AVG(Price) FROM PRODUCT;` → `3906.250000`
- **Kết hợp:** `SELECT AVG(Price) FROM PRODUCT WHERE Category = 'Accessories';` → `650.000000`
- **Lỗi:** NULL không tính vào mẫu số; muốn coi NULL là 0 thì `AVG(COALESCE(x, 0))`.
- **Khi nào dùng:** "trung bình", "mức trung bình".

**MIN / MAX**
- **Công dụng:** nhỏ nhất / lớn nhất (số, chữ, ngày). **Cú pháp:** `MIN(cot)`, `MAX(cot)`
- **Đơn giản:** `SELECT MIN(JoinDate), MAX(JoinDate) FROM CUSTOMER;` → `2024-01-10`, `2024-07-01`
- **Kết hợp:** `SELECT MAX(Price) FROM PRODUCT WHERE Category = 'Accessories';` → `1200.00`
- **Lỗi:** muốn **dòng** chứa giá trị lớn nhất (không chỉ giá trị) phải dùng subquery/`ORDER BY ... LIMIT`/window; `SELECT ProdName, MAX(Price)` không đảm bảo ProdName tương ứng.
- **Khi nào dùng:** "cao nhất", "sớm nhất", "mới nhất".

**COUNT(DISTINCT ...)**: xem COUNT ở trên; dùng khi đề nói "bao nhiêu khách **khác nhau**".

#### D. Hàm xử lý NULL

**IFNULL**
- **Công dụng:** thay NULL bằng giá trị khác. **Cú pháp:** `IFNULL(a, b)`
- **Đơn giản:** `IFNULL(NULL, 'N/A')` → `N/A`
- **Kết hợp:** `SELECT CustName, IFNULL(Email, '(chua co)') FROM CUSTOMER WHERE CustID IN (1, 3);` → An: `an@mail.com`; Cuong: `(chua co)`
- **Lỗi:** chỉ 2 tham số, riêng MySQL (SQL Server: `ISNULL`).
- **Khi nào dùng:** hiển thị giá trị mặc định cho NULL.

**COALESCE**
- **Công dụng:** lấy giá trị đầu tiên **không NULL**. **Cú pháp:** `COALESCE(a, b, c, ...)`
- **Đơn giản:** `COALESCE(NULL, NULL, 5)` → `5`
- **Kết hợp:** `SELECT COALESCE(Email, Phone) FROM CUSTOMER WHERE CustID = 3;` → `0901000003`
- **Lỗi:** nếu **tất cả** đều NULL thì kết quả NULL; các tham số nên cùng kiểu.
- **Khi nào dùng:** thay thế NULL theo thứ tự ưu tiên; chuẩn SQL nên ưu tiên hơn `IFNULL`.

**NULLIF**
- **Công dụng:** trả NULL nếu hai giá trị bằng nhau, ngược lại trả giá trị đầu. **Cú pháp:** `NULLIF(a, b)`
- **Đơn giản:** `NULLIF(0, 0)` → `NULL`; `NULLIF(5, 0)` → `5`
- **Kết hợp (tránh chia cho 0):** `SELECT 100 / NULLIF(0, 0);` → `NULL` (thay vì lỗi/ cảnh báo)
- **Lỗi:** quên rằng kết quả NULL sẽ lan sang phép tính tiếp theo (bọc `COALESCE` nếu cần).
- **Khi nào dùng:** biến giá trị "đặc biệt" (0, chuỗi rỗng) thành NULL.

#### E. Hàm điều kiện

**IF**
- **Công dụng:** chọn một trong hai giá trị. **Cú pháp:** `IF(dieu_kien, neu_dung, neu_sai)`
- **Đơn giản:** `SELECT IF(5 > 3, 'Dung', 'Sai');` → `Dung`
- **Kết hợp:** `SELECT ProdName, IF(Price >= 5000, 'Cao', 'Thap') FROM PRODUCT;` → Laptop Cao, Mouse Thap, ...
- **Lỗi:** chỉ hai nhánh (nhiều nhánh → `CASE`); riêng MySQL.
- **Khi nào dùng:** nhãn đúng/sai đơn giản.

**CASE WHEN**: xem chi tiết mục 5.E (SELECT, ORDER BY, UPDATE, trong hàm tổng hợp).

#### F. Hàm ngày tháng

**NOW / CURDATE / CURTIME**
- **Công dụng:** ngày giờ / ngày / giờ hiện tại của máy chủ. **Cú pháp:** `NOW()`, `CURDATE()`, `CURTIME()`
- **Đơn giản:** `SELECT NOW(), CURDATE(), CURTIME();` → ví dụ `2026-10-22 09:30:00`, `2026-10-22`, `09:30:00` (khác nhau theo thời điểm chạy)
- **Kết hợp:** `SELECT * FROM CUSTOMER WHERE JoinDate >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR);` (khách đăng ký trong 1 năm gần nhất)
- **Lỗi:** `NOW()` có cả giờ; so `DATE` với `NOW()` có thể lệch; kết quả phụ thuộc múi giờ máy chủ.
- **Khi nào dùng:** gán thời điểm hiện tại, lọc "N ngày gần nhất".

**YEAR / MONTH / DAY**
- **Đơn giản:** `YEAR('2025-07-07')` → `2025`; `MONTH(...)` → `7`; `DAY(...)` → `7`
- **Kết hợp:** `SELECT YEAR(OrderDate) AS Nam, MONTH(OrderDate) AS Thang, COUNT(*) FROM SALEORDER GROUP BY YEAR(OrderDate), MONTH(OrderDate);` → 2025: tháng 1 (1), 2 (2), 3 (2), 4 (2), 5 (2), 6 (2), 7 (1)
- **Lỗi:** `WHERE YEAR(cot) = 2025` không dùng được chỉ mục (nên dùng khoảng ngày); `GROUP BY MONTH` mà dữ liệu nhiều năm sẽ gộp chung tháng của các năm.
- **Khi nào dùng:** thống kê theo năm/tháng/ngày.

**DATEDIFF**
- **Công dụng:** số ngày giữa hai ngày (`a - b`). **Cú pháp:** `DATEDIFF(a, b)`
- **Đơn giản:** `DATEDIFF('2025-07-07', '2025-01-05')` → `183`
- **Kết hợp:** `SELECT OrderID, DATEDIFF('2025-08-01', OrderDate) AS SoNgay FROM SALEORDER WHERE OrderID = 12;` → `25`
- **Lỗi:** đảo thứ tự → số âm; chỉ tính theo **ngày**, bỏ phần giờ.
- **Khi nào dùng:** "bao nhiêu ngày", tuổi đơn hàng, hạn thanh toán.

**TIMESTAMPDIFF**
- **Công dụng:** chênh lệch theo đơn vị bất kỳ (YEAR, MONTH, DAY, HOUR, ...) = `d2 - d1`, chỉ tính **đơn vị trọn**.
- **Cú pháp:** `TIMESTAMPDIFF(don_vi, d1, d2)`
- **Đơn giản:** `TIMESTAMPDIFF(YEAR, '2000-05-20', '2025-05-19')` → `24`
- **Kết hợp:** `SELECT CustName, TIMESTAMPDIFF(MONTH, JoinDate, '2025-01-01') FROM CUSTOMER WHERE CustID = 1;` → `11`
- **Lỗi:** thứ tự (d1 trước, d2 sau) khác `DATEDIFF`; tính tuổi bằng `YEAR(a) - YEAR(b)` sai khi chưa tới sinh nhật.
- **Khi nào dùng:** tuổi, số tháng/năm trọn.

**DATE_ADD / DATE_SUB**
- **Công dụng:** cộng / trừ khoảng thời gian. **Cú pháp:** `DATE_ADD(d, INTERVAL n don_vi)`, `DATE_SUB(...)`
- **Đơn giản:** `DATE_ADD('2025-01-31', INTERVAL 1 MONTH)` → `2025-02-28`; `DATE_SUB('2025-03-01', INTERVAL 7 DAY)` → `2025-02-22`
- **Kết hợp:** `SELECT OrderID, DATE_ADD(OrderDate, INTERVAL 30 DAY) AS HanThanhToan FROM SALEORDER WHERE OrderID = 1;` → `2025-02-04`
- **Lỗi:** quên chữ `INTERVAL`; đơn vị viết sai (`DAYS` → đúng `DAY`).
- **Khi nào dùng:** hạn, ngày hết hạn, khoảng "N ngày trước".

**DATE_FORMAT**
- **Công dụng:** định dạng ngày thành chuỗi. **Cú pháp:** `DATE_FORMAT(d, 'dinh_dang')`
- **Đơn giản:** `DATE_FORMAT('2025-07-07', '%d/%m/%Y')` → `07/07/2025`
- **Kết hợp:** `SELECT DATE_FORMAT('2025-07-07', '%W %d/%m/%Y');` → `Monday 07/07/2025`; `DATE_FORMAT(OrderDate, '%Y-%m')` để gom theo tháng
- **Lỗi:** `%m` (tháng) khác `%i` (phút); `%M` (tên tháng) khác `%m`; kết quả là **chuỗi** (sắp xếp theo chuỗi).
- **Khi nào dùng:** hiển thị ngày kiểu Việt Nam, gom nhóm theo `YYYY-MM`.

#### G. Hàm hữu ích khác

**CAST / CONVERT**
- **Công dụng:** ép kiểu dữ liệu. **Cú pháp:** `CAST(x AS kieu)`, `CONVERT(x, kieu)`
- **Đơn giản:** `CAST('123' AS UNSIGNED)` → `123`; `CAST('2025-01-05' AS DATE)` → `2025-01-05`
- **Kết hợp:** `SELECT CAST(TotalAmount AS SIGNED) FROM SALEORDER WHERE OrderID = 1;` → `15600`; `CAST(7 AS DECIMAL(5,2)) / 2` → `3.500000`
- **Lỗi:** `CAST('abc' AS UNSIGNED)` → 0 kèm cảnh báo; chuỗi `'12abc'` → 12; ép sai kiểu có thể làm mất phần thập phân.
- **Khi nào dùng:** đổi chuỗi sang số/ngày để so sánh, tính toán.

**GREATEST / LEAST**
- **Công dụng:** giá trị lớn nhất/nhỏ nhất trong **danh sách** (cùng một dòng). **Cú pháp:** `GREATEST(a, b, ...)`, `LEAST(a, b, ...)`
- **Đơn giản:** `GREATEST(3, 9, 5)` → `9`; `LEAST(3, 9, 5)` → `3`
- **Kết hợp:** `SELECT ProdName, LEAST(Price, 1000) AS GiaToiDa1000 FROM PRODUCT WHERE ProdID IN (1, 2);` → Laptop 1000; Mouse 300
- **Lỗi:** một đối số NULL thì kết quả NULL; khác `MAX/MIN` (so giữa nhiều dòng).
- **Khi nào dùng:** chặn trên/dưới giá trị, so sánh nhiều cột cùng dòng.

### 5.K. Bài tập tự luyện bổ sung theo nhóm hàm

| # | Nhóm | Đề | Gợi ý |
|---|---|---|---|
| 1 | Chuỗi | Hiển thị `CustName` ở dạng `AN, Nguyen Van` (tên riêng viết hoa, rồi họ đệm) | `SUBSTRING_INDEX`, `UPPER`, `CONCAT` |
| 2 | Số | Tính số thùng 25 món cần để chứa tồn kho của mỗi sản phẩm | `CEIL(Stock / 25)` |
| 3 | Tổng hợp | Giá trị trung bình, nhỏ nhất, lớn nhất của đơn COMPLETED | `AVG, MIN, MAX` + `WHERE` |
| 4 | NULL | Liệt kê khách kèm liên hệ ưu tiên email, không có thì SĐT | `COALESCE(Email, Phone)` |
| 5 | Ngày | Đơn nào đặt cách hôm `2025-08-01` quá 100 ngày? | `DATEDIFF('2025-08-01', OrderDate) > 100` |

<details><summary>Đáp án</summary>

```sql
-- 1  → AN, Nguyen Van (khách 1)
SELECT CONCAT(UPPER(SUBSTRING_INDEX(CustName, ' ', -1)), ', ',
              SUBSTRING_INDEX(CustName, ' ', 2)) AS Hien FROM CUSTOMER;

-- 2  → Laptop 1, Mouse 4, Keyboard 2, Monitor 2, Headphone 2, USB 8, Smartphone 1, Webcam 1
SELECT ProdName, CEIL(Stock / 25) AS SoThung FROM PRODUCT;

-- 3  → 15122.222222 | 1700.00 | 30300.00   (TB = 136100 / 9)
SELECT AVG(TotalAmount), MIN(TotalAmount), MAX(TotalAmount)
FROM SALEORDER WHERE Status = 'COMPLETED';

-- 4
SELECT CustName, COALESCE(Email, Phone) AS LienHe FROM CUSTOMER;

-- 5  → đơn 1 (208 ngày), 2 (172), 3 (168), 4 (151), 5 (142), 6 (122), 7 (108)
--      (đơn 8: 91 ngày → không). Kiểm tra đơn 7: 2025-04-15 → 2025-08-01 = 108.
SELECT OrderID, OrderDate, DATEDIFF('2025-08-01', OrderDate) AS SoNgay
FROM SALEORDER WHERE DATEDIFF('2025-08-01', OrderDate) > 100;
```
Kiểm tra vài số: đơn 1 (01-05 → 08-01): 31 + 28 + 31 + 30 + 31 + 30 + 27 + ... tính theo mốc: 2025-01-05 → 2025-07-05 là 181 ngày, thêm 27 ngày tới 08-01 = 208. Đơn 8 (05-02 → 08-01): 91 ngày, không > 100.
</details>

---

## CHƯƠNG 6: JOIN NHIỀU BẢNG

### 6.1. Vì sao cần JOIN?

Dữ liệu được **tách thành nhiều bảng** để không lặp lại. Bảng `SALEORDER` chỉ lưu `CustID = 1`, **không** lưu tên khách. Muốn biết "đơn 1 của ai?" phải **nối** `SALEORDER` với `CUSTOMER` qua `CustID`.

**Dữ liệu trước khi JOIN (trích 3 đơn đầu và các khách liên quan):**

`SALEORDER` (trích)

| OrderID | CustID | TotalAmount |
|---|---|---|
| 1 | 1 | 15600 |
| 2 | 1 | 9200 |
| 3 | 2 | 18800 |

`CUSTOMER` (trích)

| CustID | CustName |
|---|---|
| 1 | Nguyen Van An |
| 2 | Tran Thi Binh |
| 3 | Le Van Cuong |

**Cách JOIN hoạt động:** với mỗi dòng bên trái, tìm **mọi dòng bên phải** thỏa điều kiện `ON`, rồi ghép chúng thành dòng kết quả.

```sql
SELECT o.OrderID, c.CustName, o.TotalAmount
FROM SALEORDER o
INNER JOIN CUSTOMER c ON c.CustID = o.CustID
WHERE o.OrderID <= 3;
```
| OrderID | CustName | TotalAmount |
|---|---|---|
| 1 | Nguyen Van An | 15600.00 |
| 2 | Nguyen Van An | 9200.00 |
| 3 | Tran Thi Binh | 18800.00 |

Khách `Le Van Cuong` không xuất hiện vì (trong 3 đơn đầu) không có đơn nào khớp.

### 6.2. INNER JOIN

**Công dụng:** chỉ giữ các cặp dòng **khớp ở cả hai bên**. `JOIN` đứng một mình = `INNER JOIN`.

**Cú pháp:**
```sql
SELECT ...
FROM bang_A a
INNER JOIN bang_B b ON a.khoa = b.khoa;
```

**Ví dụ: tất cả đơn hàng kèm tên khách**
```sql
SELECT o.OrderID, c.CustName, o.OrderDate, o.TotalAmount
FROM SALEORDER o
JOIN CUSTOMER c ON c.CustID = o.CustID
ORDER BY o.OrderID;
```
| OrderID | CustName | OrderDate | TotalAmount |
|---|---|---|---|
| 1 | Nguyen Van An | 2025-01-05 | 15600.00 |
| 2 | Nguyen Van An | 2025-02-10 | 9200.00 |
| 3 | Tran Thi Binh | 2025-02-14 | 18800.00 |
| 4 | Tran Thi Binh | 2025-03-03 | 15000.00 |
| 5 | Le Van Cuong | 2025-03-12 | 30300.00 |
| 6 | Le Van Cuong | 2025-04-01 | 1600.00 |
| 7 | Pham Thi Dung | 2025-04-15 | 13000.00 |
| 8 | Pham Thi Dung | 2025-05-02 | 4500.00 |
| 9 | Hoang Van Em | 2025-05-20 | 19000.00 |
| 10 | Hoang Van Em | 2025-06-08 | 9000.00 |
| 11 | Nguyen Van An | 2025-06-25 | 1700.00 |
| 12 | Tran Thi Binh | 2025-07-07 | 24000.00 |

**Giải thích từng dòng:**
- `FROM SALEORDER o`: bảng chính, `o` là bí danh.
- `JOIN CUSTOMER c ON c.CustID = o.CustID`: ghép với khách; điều kiện ghép = **khóa ngoại bằng khóa chính**.
- `o.OrderID`, `c.CustName`: viết kèm bí danh để rõ cột thuộc bảng nào. Với cột có mặt ở cả hai bảng (như `CustID`) thì **bắt buộc** (nếu không: lỗi 1052 *Column 'CustID' in field list is ambiguous*).

Khách 6 (Phuong) **không có mặt** vì không có đơn nào.

### 6.3. LEFT JOIN

**Công dụng:** giữ **toàn bộ dòng bảng bên trái**; dòng nào không có đối tác bên phải thì các cột bên phải là **NULL**.

```sql
SELECT c.CustID, c.CustName, o.OrderID
FROM CUSTOMER c
LEFT JOIN SALEORDER o ON o.CustID = c.CustID
ORDER BY c.CustID, o.OrderID;
```
| CustID | CustName | OrderID |
|---|---|---|
| 1 | Nguyen Van An | 1 |
| 1 | Nguyen Van An | 2 |
| 1 | Nguyen Van An | 11 |
| 2 | Tran Thi Binh | 3 |
| 2 | Tran Thi Binh | 4 |
| 2 | Tran Thi Binh | 12 |
| 3 | Le Van Cuong | 5 |
| 3 | Le Van Cuong | 6 |
| 4 | Pham Thi Dung | 7 |
| 4 | Pham Thi Dung | 8 |
| 5 | Hoang Van Em | 9 |
| 5 | Hoang Van Em | 10 |
| 6 | Vu Thi Phuong | **NULL** |

Một khách có 3 đơn thì xuất hiện **3 dòng** (mỗi dòng một đơn). Khách 6 vẫn có mặt, `OrderID = NULL`.

**Kỹ thuật "tìm cái chưa có" (anti-join):** thêm `WHERE bên_phải.khóa IS NULL`.
```sql
-- Khách chưa từng mua hàng
SELECT c.CustID, c.CustName
FROM CUSTOMER c
LEFT JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.OrderID IS NULL;
```
→ `6 | Vu Thi Phuong`.

Tương tự:
```sql
-- Nhân viên chưa lập đơn nào → Do Minh Quan (1), Pham Duc Minh (5)
SELECT e.EmpID, e.EmpName
FROM EMPLOYEE e LEFT JOIN SALEORDER o ON o.EmpID = e.EmpID
WHERE o.OrderID IS NULL;

-- Sản phẩm chưa bán được → Webcam (8)
SELECT p.ProdID, p.ProdName
FROM PRODUCT p LEFT JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID
WHERE od.OrderID IS NULL;
```

**Ví dụ đếm đơn có cả khách 0 đơn:**
```sql
SELECT c.CustName, COUNT(o.OrderID) AS SoDon
FROM CUSTOMER c
LEFT JOIN SALEORDER o ON o.CustID = c.CustID
GROUP BY c.CustID, c.CustName;
```
| CustName | SoDon |
|---|---|
| Nguyen Van An | 3 |
| Tran Thi Binh | 3 |
| Le Van Cuong | 2 |
| Pham Thi Dung | 2 |
| Hoang Van Em | 2 |
| Vu Thi Phuong | **0** |

Dùng **`COUNT(o.OrderID)`** (đếm cột bên phải, bỏ NULL) chứ **không** `COUNT(*)`: nếu dùng `COUNT(*)` thì khách 6 ra `1` (vì vẫn có 1 dòng ghép).

### 6.4. RIGHT JOIN

Ngược lại với LEFT: giữ toàn bộ dòng **bên phải**. Thực tế **ít dùng**, vì luôn có thể đổi chỗ hai bảng rồi dùng LEFT JOIN. Hai câu dưới đây tương đương:
```sql
SELECT c.CustName, o.OrderID FROM SALEORDER o RIGHT JOIN CUSTOMER c ON o.CustID = c.CustID;
SELECT c.CustName, o.OrderID FROM CUSTOMER c LEFT  JOIN SALEORDER o ON o.CustID = c.CustID;
```
**Kết quả minh họa** (lọc `CustID >= 5` để ngắn):
```sql
SELECT c.CustName, o.OrderID
FROM SALEORDER o RIGHT JOIN CUSTOMER c ON o.CustID = c.CustID
WHERE c.CustID >= 5
ORDER BY c.CustID, o.OrderID;
```
| CustName | OrderID |
|---|---|
| Hoang Van Em | 9 |
| Hoang Van Em | 10 |
| Vu Thi Phuong | NULL |

Bảng bên **phải** (`CUSTOMER`) được giữ nguyên toàn bộ, nên khách Phuong (chưa có đơn) vẫn xuất hiện với `OrderID = NULL`.

Lời khuyên: chỉ dùng LEFT JOIN cho nhất quán, đọc code dễ hơn. (MySQL **không** có `FULL OUTER JOIN`; cần giả lập bằng `LEFT JOIN ... UNION ... RIGHT JOIN ...`.)

### 6.5. CROSS JOIN

**Công dụng:** tích Descartes — **mọi dòng bên trái ghép với mọi dòng bên phải**, không cần `ON`. Số dòng = m × n.
```sql
SELECT c.CustName, p.ProdName
FROM CUSTOMER c
CROSS JOIN PRODUCT p
WHERE c.CustID IN (1, 2) AND p.ProdID IN (1, 2);
```
| CustName | ProdName |
|---|---|
| Nguyen Van An | Laptop Dell |
| Nguyen Van An | Mouse Logitech |
| Tran Thi Binh | Laptop Dell |
| Tran Thi Binh | Mouse Logitech |

(2 × 2 = 4 dòng. Không lọc thì 6 × 8 = 48.)

**Khi nào dùng:** tạo mọi tổ hợp (nhân viên × tháng) để rồi `LEFT JOIN` doanh thu thực tế, nhờ đó tháng nào không có doanh thu vẫn hiện số 0.

**Lỗi nguy hiểm:** *quên mệnh đề ON* hoặc ghi `FROM A, B` mà quên `WHERE A.id = B.id` → vô tình tạo CROSS JOIN, kết quả bùng nổ (6 × 12 = 72 dòng nhưng toàn ghép sai).

### 6.6. SELF JOIN (tự nối)

**Công dụng:** một bảng nối với chính nó, dùng khi bảng có quan hệ đệ quy (nhân viên – quản lý). Bắt buộc dùng **hai bí danh khác nhau**.
```sql
SELECT e.EmpName AS NhanVien, m.EmpName AS QuanLy
FROM EMPLOYEE e
LEFT JOIN EMPLOYEE m ON m.EmpID = e.ManagerID;
```
| NhanVien | QuanLy |
|---|---|
| Do Minh Quan | NULL |
| Nguyen Thu Ha | Do Minh Quan |
| Tran Quoc Huy | Do Minh Quan |
| Le Thi Lan | Do Minh Quan |
| Pham Duc Minh | Nguyen Thu Ha |

Giải thích: `e` là "vai nhân viên", `m` là "vai quản lý" của cùng bảng. Điều kiện `m.EmpID = e.ManagerID`: quản lý của `e` là dòng `m` có `EmpID` bằng `e.ManagerID`. Dùng `LEFT JOIN` để sếp lớn nhất (`ManagerID = NULL`) vẫn có mặt; dùng `INNER JOIN` thì Quan biến mất.

Ví dụ khác: tìm cặp khách cùng thành phố:
```sql
SELECT a.CustName AS Khach1, b.CustName AS Khach2, a.City
FROM CUSTOMER a
JOIN CUSTOMER b ON a.City = b.City AND a.CustID < b.CustID;
```
→ `(An, Dung, Ha Noi)` và `(Binh, Em, Ho Chi Minh)`. Điều kiện `a.CustID < b.CustID` để mỗi cặp chỉ xuất hiện **một lần** và không ghép khách với chính mình.

### 6.7. JOIN nhiều bảng

Nối **từng bảng một**, mỗi `JOIN` có `ON` riêng. Mỗi bảng thêm vào phải nối được với **một bảng đã có** trong câu.

```sql
SELECT o.OrderID, c.CustName, e.EmpName, p.ProdName,
       od.Quantity, od.Quantity * od.UnitPrice AS ThanhTien
FROM SALEORDER o
JOIN CUSTOMER     c  ON c.CustID  = o.CustID
JOIN EMPLOYEE     e  ON e.EmpID   = o.EmpID
JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
JOIN PRODUCT      p  ON p.ProdID  = od.ProdID
WHERE o.OrderID IN (1, 3)
ORDER BY o.OrderID, p.ProdID;
```
| OrderID | CustName | EmpName | ProdName | Quantity | ThanhTien |
|---|---|---|---|---|---|
| 1 | Nguyen Van An | Nguyen Thu Ha | Laptop Dell | 1 | 15000.00 |
| 1 | Nguyen Van An | Nguyen Thu Ha | Mouse Logitech | 2 | 600.00 |
| 3 | Tran Thi Binh | Tran Quoc Huy | Headphone | 1 | 800.00 |
| 3 | Tran Thi Binh | Tran Quoc Huy | Smartphone | 2 | 18000.00 |

**Cách xây dựng:** bắt đầu từ bảng "trung tâm" (`SALEORDER`), rồi thêm lần lượt `CUSTOMER` (ai mua), `EMPLOYEE` (ai bán), `ORDER_DETAIL` (mua gì), `PRODUCT` (tên sản phẩm). Mỗi lần thêm một JOIN, **chạy thử** để chắc số dòng hợp lý.

**Đường nối giữa các bảng:**
```
CUSTOMER.CustID ── SALEORDER.CustID
EMPLOYEE.EmpID  ── SALEORDER.EmpID
SALEORDER.OrderID ── ORDER_DETAIL.OrderID
PRODUCT.ProdID  ── ORDER_DETAIL.ProdID
```

### 6.8. ON và WHERE: khác nhau thế nào?

- Với **INNER JOIN**: đặt điều kiện ở `ON` hay `WHERE` cho kết quả **giống nhau**.
- Với **LEFT JOIN**: **khác hẳn**.
  - `ON`: điều kiện để **quyết định ghép hay không**. Dòng bên trái luôn được giữ.
  - `WHERE`: lọc **sau khi** ghép xong. Dòng có NULL bên phải sẽ bị loại → LEFT JOIN **biến thành INNER JOIN**.

**Bài toán:** "Với mỗi khách, đếm số đơn **PENDING**."
```sql
-- (A) Điều kiện trong ON  ✔ đúng ý
SELECT c.CustName, COUNT(o.OrderID) AS DonCho
FROM CUSTOMER c
LEFT JOIN SALEORDER o ON o.CustID = c.CustID AND o.Status = 'PENDING'
GROUP BY c.CustID, c.CustName;

-- (B) Điều kiện trong WHERE  ✘ mất khách
SELECT c.CustName, COUNT(o.OrderID) AS DonCho
FROM CUSTOMER c
LEFT JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.Status = 'PENDING'
GROUP BY c.CustID, c.CustName;
```
| (A) CustName | DonCho | | (B) CustName | DonCho |
|---|---|---|---|---|
| Nguyen Van An | 0 | | Le Van Cuong | 1 |
| Tran Thi Binh | 0 | | Hoang Van Em | 1 |
| Le Van Cuong | 1 | | | |
| Pham Thi Dung | 0 | | | |
| Hoang Van Em | 1 | | | |
| Vu Thi Phuong | 0 | | | |

(A) đủ 6 khách, kể cả người có 0 đơn chờ. (B) chỉ còn 2 khách, vì `WHERE o.Status = 'PENDING'` loại hết các dòng mà `o.Status` là NULL hoặc khác PENDING.

> **Quy tắc:** với `LEFT JOIN`, điều kiện lọc **bảng bên phải** → đặt ở `ON`. Điều kiện lọc **bảng bên trái** → `WHERE`.

### 6.9. JOIN kết hợp GROUP BY và hàm tổng hợp

```sql
-- Doanh thu (đơn COMPLETED) của từng khách, cao đến thấp
SELECT c.CustID, c.CustName, SUM(o.TotalAmount) AS DoanhThu
FROM CUSTOMER c
JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.Status = 'COMPLETED'
GROUP BY c.CustID, c.CustName
ORDER BY DoanhThu DESC;
```
| CustID | CustName | DoanhThu |
|---|---|---|
| 2 | Tran Thi Binh | 42800.00 |
| 3 | Le Van Cuong | 30300.00 |
| 1 | Nguyen Van An | 26500.00 |
| 5 | Hoang Van Em | 19000.00 |
| 4 | Pham Thi Dung | 17500.00 |

(Chi tiết GROUP BY ở Chương 7.)

### 6.10. ⚠️ Bẫy lớn nhất: dữ liệu bị nhân lên khi JOIN

**Hiện tượng:** `SALEORDER` (1 dòng/đơn) JOIN `ORDER_DETAIL` (nhiều dòng/đơn) → mỗi đơn **lặp lại** theo số dòng chi tiết. Nếu cộng `TotalAmount` (cột của `SALEORDER`) thì bị cộng **nhiều lần**.

**Nhìn tận mắt, đơn 1 và 8:**
```sql
SELECT o.OrderID, o.TotalAmount, od.ProdID
FROM SALEORDER o JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
WHERE o.OrderID IN (1, 8);
```
| OrderID | TotalAmount | ProdID |
|---|---|---|
| 1 | 15600.00 | 1 |
| 1 | 15600.00 | 2 |
| 8 | 4500.00 | 3 |
| 8 | 4500.00 | 5 |
| 8 | 4500.00 | 6 |

Đơn 1 xuất hiện 2 lần, đơn 8 xuất hiện 3 lần, **`TotalAmount` bị lặp**.

**Cách tính SAI** (tổng tiền mỗi khách):
```sql
SELECT c.CustName, SUM(o.TotalAmount) AS TongSai, COUNT(*) AS SoDonSai
FROM CUSTOMER c
JOIN SALEORDER o     ON o.CustID = c.CustID
JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
GROUP BY c.CustID, c.CustName;
```
| CustName | TongSai | SoDonSai | Đúng phải là (tổng / số đơn) |
|---|---|---|---|
| Nguyen Van An | 53000.00 | 6 | 26500 / 3 |
| Tran Thi Binh | 100600.00 | 5 | 57800 / 3 |
| Le Van Cuong | 63800.00 | 4 | 31900 / 2 |
| Pham Thi Dung | 39500.00 | 5 | 17500 / 2 |
| Hoang Van Em | 47000.00 | 3 | 28000 / 2 |

**Ba cách sửa:**

*Cách 1 — Không JOIN bảng chi tiết nếu không cần* (cách đơn giản nhất):
```sql
SELECT c.CustName, SUM(o.TotalAmount) AS Tong, COUNT(*) AS SoDon
FROM CUSTOMER c JOIN SALEORDER o ON o.CustID = c.CustID
GROUP BY c.CustID, c.CustName;
```

*Cách 2 — Tính tổng từ chính bảng chi tiết* (đúng khi cần JOIN chi tiết):
```sql
SELECT c.CustName,
       SUM(od.Quantity * od.UnitPrice) AS Tong,
       COUNT(DISTINCT o.OrderID)       AS SoDon
FROM CUSTOMER c
JOIN SALEORDER o     ON o.CustID = c.CustID
JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
GROUP BY c.CustID, c.CustName;
```
`SUM` trên cột của bảng chi tiết (mỗi dòng chi tiết đếm một lần → đúng). `COUNT(DISTINCT o.OrderID)` để đếm đơn mà không bị nhân.

*Cách 3 — Gom nhóm trước, JOIN sau* (an toàn nhất khi có nhiều bảng "nhiều"):
```sql
SELECT c.CustName, d.Tong
FROM CUSTOMER c
JOIN (SELECT CustID, SUM(TotalAmount) AS Tong FROM SALEORDER GROUP BY CustID) d
     ON d.CustID = c.CustID;
```

**Quy tắc ghi nhớ:** *Trước khi cộng/đếm, hỏi "mỗi dòng trong kết quả JOIN đại diện cho cái gì?"* Nếu mỗi dòng là **một dòng chi tiết** thì chỉ được `SUM` các cột thuộc **mức chi tiết**; cột thuộc mức đơn (`TotalAmount`) phải xử lý bằng cách khác.

### 6.11. JOIN kết hợp truy vấn con (bảng dẫn xuất)

Truy vấn con trong `FROM` tạo ra một "bảng tạm" để JOIN:
```sql
-- Khách có kèm số đơn và tổng chi tiêu (khách chưa mua vẫn hiện, với 0)
SELECT c.CustName,
       COALESCE(d.SoDon, 0)  AS SoDon,
       COALESCE(d.Tong, 0)   AS Tong
FROM CUSTOMER c
LEFT JOIN (
    SELECT CustID, COUNT(*) AS SoDon, SUM(TotalAmount) AS Tong
    FROM SALEORDER
    GROUP BY CustID
) d ON d.CustID = c.CustID;
```
| CustName | SoDon | Tong |
|---|---|---|
| Nguyen Van An | 3 | 26500.00 |
| Tran Thi Binh | 3 | 57800.00 |
| Le Van Cuong | 2 | 31900.00 |
| Pham Thi Dung | 2 | 17500.00 |
| Hoang Van Em | 2 | 28000.00 |
| Vu Thi Phuong | 0 | 0 |

Bảng dẫn xuất **bắt buộc có bí danh** (`d`), nếu không lỗi 1248.

### 6.12. Khi nào KHÔNG cần JOIN?

| Tình huống | Làm thế nào |
|---|---|
| Mọi cột cần nằm trong **một bảng** | `SELECT` thẳng bảng đó |
| Chỉ cần ID (không cần tên) | Lấy `CustID` ngay từ `SALEORDER` |
| Chỉ cần **kiểm tra có tồn tại** (không cần lấy cột bảng kia) | `WHERE EXISTS` / `IN (SELECT ...)` (Chương 8), tránh nhân dòng |
| Chỉ lọc theo bảng kia, không hiển thị | Truy vấn con, ngắn gọn hơn |

Ví dụ: "danh sách khách đã từng đặt đơn COMPLETED" — chỉ cần cột của `CUSTOMER`, dùng `WHERE CustID IN (SELECT CustID FROM SALEORDER WHERE Status='COMPLETED')`. Nếu dùng JOIN sẽ phải `DISTINCT` vì khách nhiều đơn xuất hiện nhiều lần.

### 6.13. Xác định bảng cần JOIN từ đề bài

Liệt kê **các "danh từ" trong đề** và xem mỗi cái nằm ở bảng nào:

> *"Liệt kê tên khách hàng và tên sản phẩm họ đã mua trong các đơn COMPLETED."*

| Thông tin cần | Nằm ở bảng | Cột |
|---|---|---|
| tên khách hàng | CUSTOMER | CustName |
| đơn COMPLETED | SALEORDER | Status |
| sản phẩm trong đơn | ORDER_DETAIL | (nối đơn với sản phẩm) |
| tên sản phẩm | PRODUCT | ProdName |

→ Cần 4 bảng: `CUSTOMER – SALEORDER – ORDER_DETAIL – PRODUCT`. Mỗi bảng nối với bảng kế tiếp bằng khóa chung.

```sql
SELECT DISTINCT c.CustName, p.ProdName
FROM CUSTOMER c
JOIN SALEORDER o     ON o.CustID = c.CustID
JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
JOIN PRODUCT p       ON p.ProdID = od.ProdID
WHERE o.Status = 'COMPLETED'
ORDER BY c.CustName, p.ProdName;
```
(`DISTINCT` vì một khách có thể mua cùng sản phẩm ở nhiều đơn.) Ví dụ khách An mua Laptop (đơn 1), Mouse (1, 11 → 1 dòng nhờ DISTINCT), Monitor, Keyboard (2), Headphone (11).

### 6.14. Lỗi thường gặp với JOIN

| Lỗi | Triệu chứng | Cách sửa |
|---|---|---|
| Quên `ON` | Lỗi cú pháp hoặc CROSS JOIN | Luôn viết `ON` |
| Nối sai cột (`o.OrderID = c.CustID`) | Ra kết quả sai lặng lẽ | Nối **khóa ngoại với khóa chính** tương ứng |
| Cột mơ hồ | 1052 Ambiguous | Thêm tiền tố bí danh |
| Điều kiện bảng phải đặt ở WHERE trong LEFT JOIN | Mất dòng có NULL | Chuyển vào `ON` |
| Cộng cột cấp đơn sau khi JOIN chi tiết | Tổng bị nhân lên | Xem 6.10 |
| `COUNT(*)` trong LEFT JOIN | Đếm cả dòng NULL (ra 1 thay vì 0) | `COUNT(bảng_phải.khóa)` |

### 6.15. Bài tập tự luyện Chương 6

1. Liệt kê `OrderID`, `CustName`, `EmpName` của mọi đơn.
2. Liệt kê tên sản phẩm cùng **tổng số lượng đã bán** (mọi trạng thái); sản phẩm chưa bán hiện `0`.
3. Tìm khách hàng chưa có đơn `COMPLETED` nào.
4. Với mỗi nhân viên, hiển thị tên quản lý (hoặc `'(khong co)'`).

<details><summary>Đáp án</summary>

```sql
-- 1
SELECT o.OrderID, c.CustName, e.EmpName
FROM SALEORDER o
JOIN CUSTOMER c ON c.CustID = o.CustID
JOIN EMPLOYEE e ON e.EmpID = o.EmpID
ORDER BY o.OrderID;

-- 2  → Laptop 6, Mouse 8, Keyboard 3, Monitor 4, Headphone 4, USB 6, Smartphone 5, Webcam 0
SELECT p.ProdName, COALESCE(SUM(od.Quantity), 0) AS DaBan
FROM PRODUCT p
LEFT JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID
GROUP BY p.ProdID, p.ProdName;

-- 3  → Vu Thi Phuong (khách 1–5 đều có ít nhất một đơn COMPLETED)
SELECT c.CustName
FROM CUSTOMER c
LEFT JOIN SALEORDER o ON o.CustID = c.CustID AND o.Status = 'COMPLETED'
WHERE o.OrderID IS NULL;

-- 4
SELECT e.EmpName, COALESCE(m.EmpName, '(khong co)') AS QuanLy
FROM EMPLOYEE e LEFT JOIN EMPLOYEE m ON m.EmpID = e.ManagerID;
```
Chú ý câu 3: điều kiện `o.Status = 'COMPLETED'` phải ở `ON` (không phải `WHERE`) rồi mới lọc `IS NULL`, nếu đặt ở `WHERE` thì kết quả luôn rỗng.
</details>

---

### 6.16. Bài tập tự luyện theo từng loại JOIN (có đáp án)

| # | Loại | Đề |
|---|---|---|
| 1 | INNER JOIN | Liệt kê `OrderID` và tên khách của các đơn có tổng trên 20000. |
| 2 | LEFT JOIN | Mỗi khách kèm giá trị đơn lớn nhất của họ (khách chưa mua hiện NULL). |
| 3 | LEFT JOIN + ON | Mỗi nhân viên kèm doanh thu đơn COMPLETED (0 nếu không có). |
| 4 | RIGHT JOIN | Viết lại bằng LEFT JOIN: `SELECT p.ProdName, od.OrderID FROM ORDER_DETAIL od RIGHT JOIN PRODUCT p ON p.ProdID = od.ProdID`. |
| 5 | CROSS JOIN | Tạo mọi cặp (nhân viên, trạng thái đơn) và đếm số đơn của mỗi cặp (0 nếu không có). |
| 6 | Self JOIN | Liệt kê nhân viên có lương cao hơn nhân viên *Pham Duc Minh*. |
| 7 | Self JOIN (2 cấp) | Hiển thị nhân viên, quản lý trực tiếp và quản lý của quản lý. |
| 8 | JOIN nhiều bảng | Tên khách, tên nhân viên và tên sản phẩm của đơn 11. |
| 9 | ON và WHERE | Mỗi khách có bao nhiêu đơn CANCELLED (0 nếu không có)? |
| 10 | Tránh nhân dòng | Mỗi khách đã mua bao nhiêu sản phẩm **khác nhau**? |
| 11 | JOIN + subquery | Khách có tổng chi tiêu lớn hơn tổng chi tiêu của khách *Pham Thi Dung* (CustID 4). |

<details><summary>Đáp án</summary>

```sql
-- 1  → (5, Le Van Cuong), (12, Tran Thi Binh)
SELECT o.OrderID, c.CustName FROM SALEORDER o JOIN CUSTOMER c ON c.CustID = o.CustID WHERE o.TotalAmount > 20000;

-- 2  → An 15600, Binh 24000, Cuong 30300, Dung 13000, Em 19000, Phuong NULL
SELECT c.CustName, MAX(o.TotalAmount) AS DonLonNhat
FROM CUSTOMER c LEFT JOIN SALEORDER o ON o.CustID = c.CustID GROUP BY c.CustID, c.CustName;

-- 3  → Quan 0, Ha 98100, Huy 31800, Lan 6200, Minh 0
SELECT e.EmpName, COALESCE(SUM(o.TotalAmount), 0) AS DoanhThu
FROM EMPLOYEE e LEFT JOIN SALEORDER o ON o.EmpID = e.EmpID AND o.Status = 'COMPLETED'
GROUP BY e.EmpID, e.EmpName;

-- 4  (Webcam xuất hiện với OrderID NULL)
SELECT p.ProdName, od.OrderID FROM PRODUCT p LEFT JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID;

-- 5  → 15 dòng (5 nhân viên × 3 trạng thái). NV2: COMPLETED 5; NV3: COMPLETED 2, PENDING 1, CANCELLED 1;
--      NV4: COMPLETED 2, PENDING 1; NV1 và NV5: toàn 0
SELECT e.EmpName, s.Status, COUNT(o.OrderID) AS SoDon
FROM EMPLOYEE e
CROSS JOIN (SELECT 'COMPLETED' AS Status UNION ALL SELECT 'PENDING' UNION ALL SELECT 'CANCELLED') s
LEFT JOIN SALEORDER o ON o.EmpID = e.EmpID AND o.Status = s.Status
GROUP BY e.EmpID, e.EmpName, s.Status;

-- 6  → Do Minh Quan, Nguyen Thu Ha, Tran Quoc Huy, Le Thi Lan
SELECT e.EmpName FROM EMPLOYEE e JOIN EMPLOYEE m ON e.Salary > m.Salary WHERE m.EmpName = 'Pham Duc Minh';

-- 7  → chỉ Pham Duc Minh | Nguyen Thu Ha | Do Minh Quan (người khác không có quản lý cấp 2; dùng INNER JOIN nên chỉ giữ người có đủ 2 cấp)
SELECT e.EmpName, m.EmpName AS QuanLy, mm.EmpName AS QuanLyCuaQuanLy
FROM EMPLOYEE e
JOIN EMPLOYEE m  ON m.EmpID  = e.ManagerID
JOIN EMPLOYEE mm ON mm.EmpID = m.ManagerID;

-- 8  → (Nguyen Van An, Le Thi Lan, Headphone), (Nguyen Van An, Le Thi Lan, Mouse Logitech)
SELECT c.CustName, e.EmpName, p.ProdName
FROM SALEORDER o
JOIN CUSTOMER c ON c.CustID = o.CustID
JOIN EMPLOYEE e ON e.EmpID  = o.EmpID
JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
JOIN PRODUCT p ON p.ProdID = od.ProdID
WHERE o.OrderID = 11;

-- 9  → Binh 1, các khách còn lại 0 (điều kiện Status phải nằm trong ON)
SELECT c.CustName, COUNT(o.OrderID) AS DonHuy
FROM CUSTOMER c LEFT JOIN SALEORDER o ON o.CustID = c.CustID AND o.Status = 'CANCELLED'
GROUP BY c.CustID, c.CustName;

-- 10 → An 5, Binh 3, Cuong 3, Dung 5, Em 3 (khách chưa mua không xuất hiện vì dùng INNER JOIN)
SELECT c.CustName, COUNT(DISTINCT od.ProdID) AS SoSanPham
FROM CUSTOMER c
JOIN SALEORDER o ON o.CustID = c.CustID
JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
GROUP BY c.CustID, c.CustName;

-- 11 → An (26500), Binh (57800), Cuong (31900), Em (28000); Dung có 17500 nên không tự so với mình
SELECT c.CustName, t.Tong
FROM CUSTOMER c
JOIN (SELECT CustID, SUM(TotalAmount) AS Tong FROM SALEORDER GROUP BY CustID) t ON t.CustID = c.CustID
WHERE t.Tong > (SELECT SUM(TotalAmount) FROM SALEORDER WHERE CustID = 4);
```
</details>

---

## CHƯƠNG 7: GROUP BY VÀ HAVING

> Đây là chương anh bảo đang gặp khó, nên em đi **rất chậm và từng bước**. Đọc xong chương này, anh sẽ phân biệt `WHERE` và `HAVING` mà không cần nhớ mẹo, vì anh hiểu SQL xử lý theo thứ tự nào.

### 7.1. GROUP BY làm gì? "Gom các dòng theo một cột" nghĩa là gì?

**Hình dung:** anh có 12 lá thư đặt trên bàn, mỗi lá ghi tên người gửi. `GROUP BY NguoiGui` nghĩa là: **xếp thư vào các hộp, mỗi người gửi một hộp**. Sau đó anh có thể hỏi về từng hộp: *hộp có bao nhiêu thư* (`COUNT`), *tổng số tiền ghi trong thư* (`SUM`)...

Quy tắc cốt lõi:

> Sau `GROUP BY`, **mỗi nhóm chỉ còn lại ĐÚNG MỘT DÒNG** trong kết quả. Vì vậy trong `SELECT` chỉ được viết:
> 1. **cột dùng để gom nhóm** (cái ghi trên hộp), hoặc
> 2. **hàm tổng hợp** (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) tính trên cả hộp.
>
> Một cột khác thì **không biết lấy giá trị dòng nào** trong hộp → lỗi.

**Không có `GROUP BY`** thì hàm tổng hợp xem **toàn bộ bảng là một hộp duy nhất**:
```sql
SELECT COUNT(*), SUM(TotalAmount) FROM SALEORDER;     -- 1 dòng: 12 | 161700.00
```

### 7.2. Ví dụ đầu tiên: số đơn hàng của mỗi nhân viên

```sql
SELECT EmpID, COUNT(*) AS SoDon
FROM SALEORDER
GROUP BY EmpID;
```

**Bước 1 — Dữ liệu ban đầu** (12 dòng; chỉ hiện các cột cần):

| OrderID | EmpID | Status | TotalAmount |
|---|---|---|---|
| 1 | 2 | COMPLETED | 15600 |
| 2 | 2 | COMPLETED | 9200 |
| 3 | 3 | COMPLETED | 18800 |
| 4 | 3 | CANCELLED | 15000 |
| 5 | 2 | COMPLETED | 30300 |
| 6 | 4 | PENDING | 1600 |
| 7 | 3 | COMPLETED | 13000 |
| 8 | 4 | COMPLETED | 4500 |
| 9 | 2 | COMPLETED | 19000 |
| 10 | 3 | PENDING | 9000 |
| 11 | 4 | COMPLETED | 1700 |
| 12 | 2 | COMPLETED | 24000 |

**Bước 2 — GROUP BY EmpID: xếp vào 3 hộp**

| Hộp (EmpID) | Các đơn trong hộp |
|---|---|
| 2 | 1, 2, 5, 9, 12 |
| 3 | 3, 4, 7, 10 |
| 4 | 6, 8, 11 |

**Bước 3 — Tính COUNT(\*) cho từng hộp, mỗi hộp thành 1 dòng:**

| EmpID | SoDon |
|---|---|
| 2 | 5 |
| 3 | 4 |
| 4 | 3 |

Nhân viên 1 và 5 **không xuất hiện**: vì không có đơn nào thì không có hộp nào. Muốn thấy họ (với 0) phải `LEFT JOIN` từ `EMPLOYEE`:
```sql
SELECT e.EmpName, COUNT(o.OrderID) AS SoDon
FROM EMPLOYEE e LEFT JOIN SALEORDER o ON o.EmpID = e.EmpID
GROUP BY e.EmpID, e.EmpName;
```
| EmpName | SoDon |
|---|---|
| Do Minh Quan | 0 |
| Nguyen Thu Ha | 5 |
| Tran Quoc Huy | 4 |
| Le Thi Lan | 3 |
| Pham Duc Minh | 0 |

### 7.3. Các hàm tổng hợp trong từng nhóm

```sql
SELECT EmpID,
       COUNT(*)          AS SoDon,
       SUM(TotalAmount)  AS TongTien,
       AVG(TotalAmount)  AS TrungBinh,
       MIN(TotalAmount)  AS NhoNhat,
       MAX(TotalAmount)  AS LonNhat
FROM SALEORDER
GROUP BY EmpID;
```
| EmpID | SoDon | TongTien | TrungBinh | NhoNhat | LonNhat |
|---|---|---|---|---|---|
| 2 | 5 | 98100.00 | 19620.000000 | 9200.00 | 30300.00 |
| 3 | 4 | 55800.00 | 13950.000000 | 9000.00 | 18800.00 |
| 4 | 3 | 7800.00 | 2600.000000 | 1600.00 | 4500.00 |

Kiểm tra nhẩm: 98100 + 55800 + 7800 = 161700 = tổng toàn bảng. Luôn tự kiểm tra kiểu này, rất hiệu quả để bắt lỗi.

### 7.4. GROUP BY nhiều cột

Nhóm theo **tổ hợp** các cột: hai dòng cùng một hộp khi **tất cả các cột gom nhóm đều bằng nhau**.
```sql
SELECT CustID, Status, COUNT(*) AS SoDon, SUM(TotalAmount) AS Tong
FROM SALEORDER
GROUP BY CustID, Status
ORDER BY CustID, Status;
```
| CustID | Status | SoDon | Tong |
|---|---|---|---|
| 1 | COMPLETED | 3 | 26500.00 |
| 2 | CANCELLED | 1 | 15000.00 |
| 2 | COMPLETED | 2 | 42800.00 |
| 3 | COMPLETED | 1 | 30300.00 |
| 3 | PENDING | 1 | 1600.00 |
| 4 | COMPLETED | 2 | 17500.00 |
| 5 | COMPLETED | 1 | 19000.00 |
| 5 | PENDING | 1 | 9000.00 |

9 tổ hợp → 8 dòng kết quả (khách 1 và 4 chỉ có một loại trạng thái). Ví dụ khách 2 có hai hộp: `(2, CANCELLED)` chứa đơn 4 và `(2, COMPLETED)` chứa đơn 3, 12.

### 7.5. COUNT(\*), COUNT(cột), COUNT(DISTINCT cột)

| Dạng | Đếm cái gì |
|---|---|
| `COUNT(*)` | **số dòng** trong nhóm |
| `COUNT(cột)` | số dòng có `cột` **khác NULL** |
| `COUNT(DISTINCT cột)` | số giá trị **khác nhau**, không tính NULL |

**Ví dụ 1 — NULL:**
```sql
SELECT City, COUNT(*) AS SoKhach, COUNT(Email) AS CoEmail
FROM CUSTOMER GROUP BY City;
```
| City | SoKhach | CoEmail |
|---|---|---|
| Ha Noi | 2 | 2 |
| Ho Chi Minh | 2 | 1 |
| Da Nang | 1 | 0 |
| Hai Phong | 1 | 1 |

Ở `Ho Chi Minh`: 2 khách nhưng Em chưa có email → `COUNT(Email) = 1`.

**Ví dụ 2 — DISTINCT:** mỗi nhân viên phục vụ bao nhiêu đơn và bao nhiêu **khách khác nhau**?
```sql
SELECT EmpID, COUNT(*) AS SoDon, COUNT(DISTINCT CustID) AS SoKhachKhacNhau
FROM SALEORDER GROUP BY EmpID;
```
| EmpID | SoDon | SoKhachKhacNhau |
|---|---|---|
| 2 | 5 | 4 |
| 3 | 4 | 3 |
| 4 | 3 | 3 |

Nhân viên 2 có 5 đơn nhưng chỉ 4 khách, vì khách 1 mua hai lần (đơn 1 và 2).

### 7.6. THỨ TỰ XỬ LÝ LOGIC CỦA SELECT (phần quan trọng nhất của chương)

Anh **viết** `SELECT` đầu tiên, nhưng MySQL **thực thi** theo thứ tự:

| Thứ tự chạy | Mệnh đề | Làm gì | Còn dữ liệu gì? |
|---|---|---|---|
| 1 | `FROM` / `JOIN` | Lấy bảng, nối các bảng | Toàn bộ dòng |
| 2 | `WHERE` | **Lọc từng dòng** | Dòng thỏa điều kiện |
| 3 | `GROUP BY` | **Gom** dòng còn lại thành các nhóm | Các nhóm |
| 4 | `HAVING` | **Lọc nhóm** (dựa trên giá trị tổng hợp) | Nhóm thỏa điều kiện |
| 5 | `SELECT` | Tính cột, hàm tổng hợp, bí danh | 1 dòng / nhóm |
| 6 | `DISTINCT` | Loại dòng trùng | |
| 7 | `ORDER BY` | Sắp xếp | |
| 8 | `LIMIT` | Cắt bớt dòng | |

```
FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
```

**Hệ quả suy ra ngay:**

1. **Vì sao không dùng `SUM()` trong `WHERE`?** Vì khi `WHERE` chạy (bước 2), **chưa có nhóm nào** (nhóm tạo ở bước 3) nên chưa có gì để cộng. Muốn lọc theo kết quả tổng hợp phải dùng `HAVING` (bước 4, sau khi đã có nhóm).
2. **Vì sao không dùng bí danh cột trong `WHERE`?** `SELECT` (bước 5) chạy sau `WHERE` (bước 2), lúc ấy bí danh chưa tồn tại. Còn `ORDER BY` (bước 7) chạy sau `SELECT` nên dùng được bí danh.
3. **`WHERE` lọc dòng → nhẹ hơn.** Lọc sớm bằng `WHERE` giúp ít dữ liệu hơn phải gom nhóm. Điều kiện nào **không dính hàm tổng hợp** thì đưa vào `WHERE`.

### 7.7. WHERE khác HAVING thế nào?

| | `WHERE` | `HAVING` |
|---|---|---|
| Chạy khi nào | **Trước** GROUP BY | **Sau** GROUP BY |
| Lọc cái gì | Từng **dòng** | Từng **nhóm** |
| Dùng hàm tổng hợp (`SUM`, `COUNT`...) | ❌ Không | ✅ Có |
| Dùng cột thường | ✅ | Chỉ cột gom nhóm hoặc hàm tổng hợp (chuẩn SQL) |

**Quy tắc chọn:**
- Điều kiện nói về **một dòng đơn lẻ** ("đơn COMPLETED", "đặt sau tháng 3", "ở Hà Nội") → `WHERE`.
- Điều kiện nói về **kết quả của cả nhóm** ("tổng > 50000", "có ít nhất 3 đơn", "trung bình < 10") → `HAVING`.
- Một đề bài thường có **cả hai**: "nhân viên có **doanh thu từ đơn COMPLETED** vượt 50000" → `COMPLETED` là điều kiện dòng (`WHERE`), "vượt 50000" là điều kiện nhóm (`HAVING`).

### 7.8. Ví dụ từng bước đầy đủ: nhân viên có doanh thu COMPLETED vượt 50000

**Đề:** "Liệt kê nhân viên có tổng doanh thu từ các đơn COMPLETED vượt 50000."

```sql
SELECT EmpID, SUM(TotalAmount) AS DoanhThu
FROM SALEORDER
WHERE Status = 'COMPLETED'
GROUP BY EmpID
HAVING SUM(TotalAmount) > 50000;
```

**Bước 1 — Dữ liệu ban đầu:** 12 dòng (bảng ở mục 7.2).

**Bước 2 — Sau `WHERE Status = 'COMPLETED'`:** loại đơn 4 (CANCELLED), 6 và 10 (PENDING) → còn **9 dòng**.

| OrderID | EmpID | TotalAmount |
|---|---|---|
| 1 | 2 | 15600 |
| 2 | 2 | 9200 |
| 3 | 3 | 18800 |
| 5 | 2 | 30300 |
| 7 | 3 | 13000 |
| 8 | 4 | 4500 |
| 9 | 2 | 19000 |
| 11 | 4 | 1700 |
| 12 | 2 | 24000 |

**Bước 3 — Sau `GROUP BY EmpID`: các nhóm**

| Nhóm (EmpID) | Các đơn |
|---|---|
| 2 | 1, 2, 5, 9, 12 |
| 3 | 3, 7 |
| 4 | 8, 11 |

**Bước 4 — Tính `SUM(TotalAmount)` mỗi nhóm:**

| EmpID | SUM |
|---|---|
| 2 | 15600 + 9200 + 30300 + 19000 + 24000 = **98100** |
| 3 | 18800 + 13000 = **31800** |
| 4 | 4500 + 1700 = **6200** |

**Bước 5 — `HAVING SUM(TotalAmount) > 50000`:** chỉ nhóm 2 (98100) thỏa; nhóm 3 và 4 bị loại.

**Bước 6 — Kết quả cuối:**

| EmpID | DoanhThu |
|---|---|
| 2 | 98100.00 |

> Hãy nhớ kết quả này: đây chính là phần `SELECT ... GROUP BY ... HAVING` bên trong câu `UPDATE` ở Chương 8, và nhân viên 2 là người được tăng lương.

**Nếu nhầm `HAVING` thành `WHERE`:** `WHERE Status='COMPLETED' AND SUM(TotalAmount) > 50000` → lỗi 1111 *Invalid use of group function*, vì `WHERE` chạy trước khi có nhóm.

### 7.9. Các ví dụ được yêu cầu

**(a) Tổng doanh thu của từng khách hàng** (COMPLETED)
```sql
SELECT CustID, SUM(TotalAmount) AS DoanhThu
FROM SALEORDER
WHERE Status = 'COMPLETED'
GROUP BY CustID;
```
| CustID | DoanhThu |
|---|---|
| 1 | 26500.00 |
| 2 | 42800.00 |
| 3 | 30300.00 |
| 4 | 17500.00 |
| 5 | 19000.00 |

**(b) Số đơn hàng của mỗi nhân viên:** xem mục 7.2.

**(c) Khách hàng có tổng chi tiêu (COMPLETED) trên 30000**
```sql
SELECT CustID, SUM(TotalAmount) AS TongChiTieu
FROM SALEORDER
WHERE Status = 'COMPLETED'
GROUP BY CustID
HAVING SUM(TotalAmount) > 30000;
```
| CustID | TongChiTieu |
|---|---|
| 2 | 42800.00 |
| 3 | 30300.00 |

(Khách 1 có 26500, chưa vượt ngưỡng.) Thêm `JOIN CUSTOMER` để hiện tên: xem mục 7.11.

**(d) Khách hàng có ít nhất ba đơn hàng**
```sql
SELECT CustID, COUNT(*) AS SoDon
FROM SALEORDER
GROUP BY CustID
HAVING COUNT(*) >= 3;
```
| CustID | SoDon |
|---|---|
| 1 | 3 |
| 2 | 3 |

**(e) Sản phẩm được bán nhiều nhất** (tính theo số lượng):
```sql
SELECT p.ProdID, p.ProdName, SUM(od.Quantity) AS DaBan
FROM PRODUCT p
JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID
GROUP BY p.ProdID, p.ProdName
ORDER BY DaBan DESC
LIMIT 1;
```
Bảng đầy đủ trước khi `LIMIT`:

| ProdID | ProdName | DaBan |
|---|---|---|
| 2 | Mouse Logitech | **8** |
| 1 | Laptop Dell | 6 |
| 6 | USB 64GB | 6 |
| 7 | Smartphone | 5 |
| 4 | Monitor 24 inch | 4 |
| 5 | Headphone | 4 |
| 3 | Keyboard Mechanical | 3 |

→ `Mouse Logitech (8)`. **Lưu ý đồng hạng:** `LIMIT 1` chỉ lấy một dòng dù có nhiều sản phẩm cùng số 1. Cách lấy **tất cả** sản phẩm đồng hạng nhất: xem Chương 8 (subquery) hoặc Chương 10 (`RANK`).

**(f) Doanh thu theo nhóm hàng (GROUP BY + JOIN)**, tính từ chi tiết các đơn COMPLETED:
```sql
SELECT p.Category, SUM(od.Quantity * od.UnitPrice) AS DoanhThu
FROM ORDER_DETAIL od
JOIN SALEORDER o ON o.OrderID = od.OrderID
JOIN PRODUCT   p ON p.ProdID  = od.ProdID
WHERE o.Status = 'COMPLETED'
GROUP BY p.Category;
```
| Category | DoanhThu |
|---|---|
| Electronics | 127000.00 |
| Accessories | 9100.00 |

Kiểm tra: 127000 + 9100 = 136100 = tổng doanh thu COMPLETED (đã tính ở Chương 5).

**(g) GROUP BY kết hợp lọc theo ngày: doanh thu từng tháng**
```sql
SELECT DATE_FORMAT(OrderDate, '%Y-%m') AS Thang, SUM(TotalAmount) AS DoanhThu
FROM SALEORDER
WHERE Status = 'COMPLETED'
  AND OrderDate >= '2025-01-01' AND OrderDate < '2025-08-01'
GROUP BY DATE_FORMAT(OrderDate, '%Y-%m')
ORDER BY Thang;
```
| Thang | DoanhThu |
|---|---|
| 2025-01 | 15600.00 |
| 2025-02 | 28000.00 |
| 2025-03 | 30300.00 |
| 2025-04 | 13000.00 |
| 2025-05 | 23500.00 |
| 2025-06 | 1700.00 |
| 2025-07 | 24000.00 |

Chỉ giữ những tháng doanh thu trên 20000: thêm `HAVING SUM(TotalAmount) > 20000` → `2025-02`, `2025-03`, `2025-05`, `2025-07`.

> Cột `GROUP BY` ở đây là **biểu thức** `DATE_FORMAT(...)`, không phải cột có sẵn. Hoàn toàn hợp lệ, miễn là `SELECT` dùng cùng biểu thức đó.

### 7.10. GROUP BY kết hợp JOIN

Thêm `JOIN` để hiển thị tên thay vì ID:
```sql
SELECT c.CustName, COUNT(o.OrderID) AS SoDon, SUM(o.TotalAmount) AS Tong
FROM CUSTOMER c
JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.Status = 'COMPLETED'
GROUP BY c.CustID, c.CustName
HAVING SUM(o.TotalAmount) > 20000
ORDER BY Tong DESC;
```
| CustName | SoDon | Tong |
|---|---|---|
| Tran Thi Binh | 2 | 42800.00 |
| Le Van Cuong | 1 | 30300.00 |
| Nguyen Van An | 3 | 26500.00 |

Thứ tự chạy: `FROM+JOIN` (nối khách–đơn) → `WHERE` (lấy COMPLETED) → `GROUP BY` (mỗi khách một hộp) → `HAVING` (tổng > 20000, loại Em 19000 và Dung 17500) → `SELECT` → `ORDER BY Tong DESC`.

**Gom theo `CustID` cùng `CustName`:** gom theo khóa chính (`CustID`) chắc chắn đúng; nếu chỉ gom theo `CustName` mà hai khách trùng tên thì bị **gộp nhầm**. Thêm `CustName` vào `GROUP BY` để `SELECT` được phép hiển thị nó.

**Cảnh báo nhân dòng:** JOIN thêm `ORDER_DETAIL` rồi `SUM(o.TotalAmount)` sẽ sai (xem 6.10).

### 7.11. GROUP BY kết hợp truy vấn con

Khách chi tiêu **cao hơn mức trung bình** của các khách:
```sql
SELECT CustID, SUM(TotalAmount) AS Tong
FROM SALEORDER
GROUP BY CustID
HAVING SUM(TotalAmount) > (
    SELECT AVG(t.Tong)
    FROM (SELECT SUM(TotalAmount) AS Tong FROM SALEORDER GROUP BY CustID) t
);
```
Chạy riêng phần trong cùng: `SELECT SUM(TotalAmount) FROM SALEORDER GROUP BY CustID` cho 5 con số `26500, 57800, 31900, 17500, 28000`; trung bình = **32340**. Chỉ khách 2 (57800) vượt.

| CustID | Tong |
|---|---|
| 2 | 57800.00 |

Vì truy vấn con ở `FROM` bắt buộc có bí danh (`t`).

### 7.12. GROUP BY trong UPDATE và INSERT INTO ... SELECT

- **UPDATE:** `GROUP BY` thường nằm trong **truy vấn con** để chọn đối tượng cần sửa: `UPDATE EMPLOYEE ... WHERE EmpID IN (SELECT EmpID ... GROUP BY EmpID HAVING SUM(...) > 50000)`. Xem chi tiết **Chương 8**.
- **INSERT ... SELECT:** lưu kết quả thống kê vào bảng khác. Ví dụ:
```sql
CREATE TABLE CUSTOMER_SUMMARY (
    CustID INT PRIMARY KEY, SoDon INT, TongTien DECIMAL(12,2)
);
INSERT INTO CUSTOMER_SUMMARY (CustID, SoDon, TongTien)
SELECT CustID, COUNT(*), SUM(TotalAmount)
FROM SALEORDER
WHERE Status = 'COMPLETED'
GROUP BY CustID;
```
Xem thêm **Chương 11**.

### 7.13. Lỗi thường gặp ở GROUP BY / HAVING

| # | Sai | Lý do | Đúng |
|---|---|---|---|
| 1 | `SELECT EmpID, OrderID, COUNT(*) FROM SALEORDER GROUP BY EmpID` | `OrderID` không phải cột gom nhóm, cũng không phải hàm tổng hợp: nhóm có nhiều `OrderID`, lấy cái nào? (lỗi 1055, do `ONLY_FULL_GROUP_BY`) | Bỏ `OrderID`, hoặc thêm vào `GROUP BY`, hoặc bọc `MIN(OrderID)`/`GROUP_CONCAT(OrderID)` |
| 2 | `WHERE SUM(TotalAmount) > 50000` | `WHERE` chạy trước `GROUP BY` | `HAVING SUM(TotalAmount) > 50000` |
| 3 | `HAVING Status = 'COMPLETED'` (khi `Status` không nằm trong GROUP BY) | `Status` không còn tồn tại ở mức nhóm | Đưa vào `WHERE` |
| 4 | `HAVING Status = 'COMPLETED'` ở nơi nên là `WHERE` (dù chạy được khi gom theo `Status`) | Lọc muộn → chậm, dễ nhầm | Điều kiện dòng → `WHERE` |
| 5 | Quên `GROUP BY`, dùng `SELECT EmpID, SUM(x)` | Lỗi 1140 | Thêm `GROUP BY EmpID` |
| 6 | `GROUP BY CustName` khi có tên trùng | Gộp nhầm hai người | Gom theo `CustID` (+ `CustName`) |
| 7 | `COUNT(*)` trong `LEFT JOIN` | Ra 1 thay vì 0 | `COUNT(cột_bên_phải)` |
| 8 | `AVG` trên cột có NULL | Mẫu số nhỏ hơn bạn nghĩ | `AVG(COALESCE(x, 0))` nếu muốn xem NULL là 0 |

`GROUP BY` và NULL: tất cả giá trị NULL được xếp **vào cùng một nhóm**.

`GROUP_CONCAT` (riêng MySQL) liệt kê các giá trị trong nhóm:
```sql
SELECT EmpID, GROUP_CONCAT(OrderID ORDER BY OrderID SEPARATOR ', ') AS CacDon
FROM SALEORDER GROUP BY EmpID;
```
→ `2 | 1, 2, 5, 9, 12`; `3 | 3, 4, 7, 10`; `4 | 6, 8, 11`. Rất tiện để *nhìn các hộp* khi học.

### 7.14. Công thức viết một câu GROUP BY (học thuộc)

```
1. "Mỗi ___" / "theo ___" / "của từng ___"  → đó là cột GROUP BY
2. "tổng / số lượng / trung bình ___"       → hàm tổng hợp trong SELECT
3. Điều kiện về từng dòng (trạng thái, ngày) → WHERE
4. "vượt / ít nhất / lớn hơn ___" (về tổng)  → HAVING
5. "cao nhất / nhiều nhất / top"             → ORDER BY ... DESC LIMIT (hoặc subquery/RANK)
```

### 7.15. Bài tập tự luyện Chương 7

1. Số đơn hàng theo từng trạng thái.
2. Tổng số lượng bán ra theo từng sản phẩm (có tên), chỉ giữ sản phẩm bán từ 5 trở lên.
3. Nhân viên có từ 4 đơn trở lên (mọi trạng thái), kèm tên.
4. Với mỗi thành phố, tổng doanh thu COMPLETED của các khách ở đó; chỉ giữ thành phố trên 40000.

<details><summary>Đáp án</summary>

```sql
-- 1  → COMPLETED 9, PENDING 2, CANCELLED 1
SELECT Status, COUNT(*) AS SoDon FROM SALEORDER GROUP BY Status;

-- 2  → Mouse 8, Laptop 6, USB 6, Smartphone 5
SELECT p.ProdName, SUM(od.Quantity) AS DaBan
FROM PRODUCT p JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID
GROUP BY p.ProdID, p.ProdName
HAVING SUM(od.Quantity) >= 5;

-- 3  → Nguyen Thu Ha (5), Tran Quoc Huy (4)
SELECT e.EmpName, COUNT(*) AS SoDon
FROM EMPLOYEE e JOIN SALEORDER o ON o.EmpID = e.EmpID
GROUP BY e.EmpID, e.EmpName
HAVING COUNT(*) >= 4;

-- 4  → Ho Chi Minh: Binh 42800 + Em 19000 = 61800 ✔; Ha Noi: An 26500 + Dung 17500 = 44000 ✔;
--      Da Nang: 30300 ✘
SELECT c.City, SUM(o.TotalAmount) AS DoanhThu
FROM CUSTOMER c JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.Status = 'COMPLETED'
GROUP BY c.City
HAVING SUM(o.TotalAmount) > 40000;
```
Kết quả câu 4: `Ho Chi Minh | 61800.00` và `Ha Noi | 44000.00`.
</details>

---

### 7.16. Bài tập tự luyện bổ sung theo từng khái niệm (có đáp án)

| # | Khái niệm | Đề |
|---|---|---|
| 1 | GROUP BY một cột | Số sản phẩm của mỗi nhóm hàng. |
| 2 | GROUP BY nhiều cột | Số đơn theo từng cặp (nhân viên, trạng thái). |
| 3 | COUNT(*) vs COUNT(DISTINCT) | Mỗi trạng thái có bao nhiêu đơn và bao nhiêu khách khác nhau? |
| 4 | WHERE + HAVING | Khách có tổng đơn COMPLETED trên 20000, **không tính** đơn đặt trước 2025-02-01. |
| 5 | GROUP BY theo ngày | Số đơn mỗi tháng (mọi trạng thái). |
| 6 | GROUP BY + JOIN | Tổng số lượng bán theo nhóm hàng. |
| 7 | GROUP BY + subquery | Nhân viên có doanh thu COMPLETED **thấp nhất** (chỉ xét người có doanh thu). |

<details><summary>Đáp án</summary>

```sql
-- 1  → Electronics 3, Accessories 5
SELECT Category, COUNT(*) AS SoSP FROM PRODUCT GROUP BY Category;

-- 2  → (2,COMPLETED,5), (3,CANCELLED,1), (3,COMPLETED,2), (3,PENDING,1), (4,COMPLETED,2), (4,PENDING,1)
SELECT EmpID, Status, COUNT(*) AS SoDon FROM SALEORDER GROUP BY EmpID, Status ORDER BY EmpID, Status;

-- 3  → COMPLETED (9, 5 khách), PENDING (2, 2 khách), CANCELLED (1, 1 khách)
SELECT Status, COUNT(*) AS SoDon, COUNT(DISTINCT CustID) AS SoKhach FROM SALEORDER GROUP BY Status;

-- 4  → khách 2 (42800) và khách 3 (30300). Khách 1 chỉ còn 9200 + 1700 = 10900 nên bị loại
SELECT CustID, SUM(TotalAmount) AS Tong
FROM SALEORDER
WHERE Status = 'COMPLETED' AND OrderDate >= '2025-02-01'
GROUP BY CustID
HAVING SUM(TotalAmount) > 20000;

-- 5  → 01: 1, 02: 2, 03: 2, 04: 2, 05: 2, 06: 2, 07: 1
SELECT DATE_FORMAT(OrderDate, '%m') AS Thang, COUNT(*) AS SoDon FROM SALEORDER GROUP BY DATE_FORMAT(OrderDate, '%m');

-- 6  → Electronics 15 (6 + 4 + 5), Accessories 21 (8 + 3 + 4 + 6); tổng 36
SELECT p.Category, SUM(od.Quantity) AS SoLuong
FROM PRODUCT p JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID
GROUP BY p.Category;

-- 7  → EmpID 4 (6200)
SELECT EmpID, SUM(TotalAmount) AS Tong
FROM SALEORDER WHERE Status = 'COMPLETED'
GROUP BY EmpID
HAVING SUM(TotalAmount) = (
    SELECT MIN(t.Tong) FROM (SELECT SUM(TotalAmount) AS Tong FROM SALEORDER
                             WHERE Status = 'COMPLETED' GROUP BY EmpID) t);
```
</details>

---

## CHƯƠNG 8: TRUY VẤN CON (SUBQUERY)

### 8.1. Subquery là gì?

**Truy vấn con** là một câu `SELECT` **nằm bên trong** một câu lệnh khác, đặt trong dấu ngoặc `( ... )`. MySQL chạy câu bên trong **trước**, lấy kết quả của nó **thay vào** chỗ câu bên trong để chạy câu bên ngoài.

Phân loại theo **kết quả trả về** (quyết định bạn dùng được ở đâu):

| Loại | Trả về | Dùng với |
|---|---|---|
| **Scalar** (một giá trị) | 1 dòng × 1 cột | `=`, `>`, `<`... ; trong `SELECT` |
| **Cột** (danh sách) | nhiều dòng × 1 cột | `IN`, `NOT IN`, `ANY`, `ALL` |
| **Bảng** | nhiều dòng × nhiều cột | trong `FROM` (cần bí danh) |
| **Tương quan** (correlated) | phụ thuộc dòng của truy vấn ngoài | `EXISTS`, trong `SELECT`... |

### 8.2. Subquery trong WHERE (trả về một giá trị)

**Đề:** sản phẩm có giá cao hơn giá trung bình.

**Bước 1 — chạy riêng phần trong:**
```sql
SELECT AVG(Price) FROM PRODUCT;      -- 3906.250000
```
**Bước 2 — thay vào phần ngoài:**
```sql
SELECT ProdName, Price FROM PRODUCT WHERE Price > 3906.25;
```
**Bước 3 — ghép lại (để giá trị tự cập nhật khi dữ liệu đổi):**
```sql
SELECT ProdName, Price
FROM PRODUCT
WHERE Price > (SELECT AVG(Price) FROM PRODUCT);
```
| ProdName | Price |
|---|---|
| Laptop Dell | 15000.00 |
| Monitor 24 inch | 4000.00 |
| Smartphone | 9000.00 |

**Ví dụ:** đơn có tổng tiền lớn nhất:
```sql
SELECT OrderID, CustID, TotalAmount
FROM SALEORDER
WHERE TotalAmount = (SELECT MAX(TotalAmount) FROM SALEORDER);
```
→ `5 | 3 | 30300.00`. (Khác `ORDER BY ... LIMIT 1`: cách này lấy **tất cả** dòng đồng hạng.)

> Toán tử `=`, `>`... yêu cầu subquery trả về **đúng 1 giá trị**. Nếu trả nhiều dòng → lỗi 1242 *Subquery returns more than 1 row*. Khi đó hãy dùng `IN`.

### 8.3. IN và NOT IN với subquery

`IN (subquery)` kiểm tra giá trị có **nằm trong tập kết quả** của subquery không, giống `x in danh_sach` trong Python.

```sql
-- Khách đã từng đặt hàng
SELECT CustID, CustName FROM CUSTOMER
WHERE CustID IN (SELECT CustID FROM SALEORDER);
```
Subquery trả `1,1,2,2,3,3,4,4,5,5,1,2` (có trùng, không sao). Kết quả: khách 1–5.

```sql
-- Khách chưa đặt hàng
SELECT CustID, CustName FROM CUSTOMER
WHERE CustID NOT IN (SELECT CustID FROM SALEORDER);       -- → Vu Thi Phuong
```

```sql
-- Sản phẩm từng được bán trong đơn bị huỷ
SELECT ProdName FROM PRODUCT
WHERE ProdID IN (
    SELECT od.ProdID FROM ORDER_DETAIL od
    JOIN SALEORDER o ON o.OrderID = od.OrderID
    WHERE o.Status = 'CANCELLED'
);                                                         -- → Laptop Dell
```

> ⚠️ **Bẫy `NOT IN` + NULL:** nếu subquery trả ra **dù chỉ một NULL**, `x NOT IN (...)` trở thành "không biết" cho mọi dòng → **kết quả rỗng**. Cột `CustID` của `SALEORDER` là `NOT NULL` nên ở đây an toàn; khi cột có thể NULL hãy thêm `WHERE cột IS NOT NULL` trong subquery, hoặc dùng `NOT EXISTS`.

### 8.4. EXISTS và NOT EXISTS

`EXISTS (subquery)` trả `TRUE` nếu subquery **có ít nhất một dòng**; nội dung các cột không quan trọng (thường viết `SELECT 1`). Thường là **truy vấn tương quan**: subquery tham chiếu bảng ngoài.

```sql
-- Khách có ít nhất một đơn COMPLETED
SELECT c.CustName
FROM CUSTOMER c
WHERE EXISTS (
    SELECT 1 FROM SALEORDER o
    WHERE o.CustID = c.CustID AND o.Status = 'COMPLETED'
);
```
Với **mỗi khách `c`** (dòng ngoài), MySQL hỏi: "có dòng đơn nào của `c` và COMPLETED không?". Kết quả: An, Binh, Cuong, Dung, Em.

```sql
-- Khách chưa có đơn nào (an toàn với NULL, hơn NOT IN)
SELECT c.CustName FROM CUSTOMER c
WHERE NOT EXISTS (SELECT 1 FROM SALEORDER o WHERE o.CustID = c.CustID);   -- → Vu Thi Phuong
```

| So sánh | `IN` | `EXISTS` |
|---|---|---|
| Cách nghĩ | giá trị có trong **danh sách** | **có tồn tại** dòng liên quan |
| NULL | `NOT IN` dễ sai khi có NULL | `NOT EXISTS` không bị |
| Dùng khi | tập giá trị nhỏ, đơn giản | điều kiện tương quan phức tạp |

### 8.5. ANY và ALL

- `x > ANY (tập)`: lớn hơn **ít nhất một** phần tử (= lớn hơn **giá trị nhỏ nhất**).
- `x > ALL (tập)`: lớn hơn **mọi** phần tử (= lớn hơn **giá trị lớn nhất**).

```sql
-- Sản phẩm đắt hơn TẤT CẢ phụ kiện (Accessories). Giá phụ kiện lớn nhất là 1200
SELECT ProdName, Price FROM PRODUCT
WHERE Price > ALL (SELECT Price FROM PRODUCT WHERE Category = 'Accessories');
```
→ Laptop Dell 15000, Monitor 24 inch 4000, Smartphone 9000.

```sql
-- Sản phẩm đắt hơn ÍT NHẤT MỘT phụ kiện (tức > 250, giá phụ kiện nhỏ nhất)
SELECT ProdName, Price FROM PRODUCT
WHERE Price > ANY (SELECT Price FROM PRODUCT WHERE Category = 'Accessories');
```
→ 7 sản phẩm (mọi sản phẩm trừ USB 64GB, vì không > chính nó).

Hiểu nhầm hay gặp: `= ANY` giống `IN`; `<> ALL` giống `NOT IN`. Thông thường dùng `MAX/MIN` rõ ràng hơn: `Price > (SELECT MAX(Price) ...)`.

### 8.6. Subquery trong SELECT (mỗi dòng một giá trị)

```sql
SELECT c.CustName,
       (SELECT COUNT(*) FROM SALEORDER o WHERE o.CustID = c.CustID) AS SoDon
FROM CUSTOMER c;
```
Với mỗi khách, chạy subquery đếm đơn. Kết quả: An 3, Binh 3, Cuong 2, Dung 2, Em 2, Phuong 0.

Phải trả về **đúng 1 giá trị**. Tiện cho thống kê nhỏ; với dữ liệu lớn nên dùng `LEFT JOIN + GROUP BY` (một lần gom thay vì chạy lại nhiều lần).

### 8.7. Subquery trong FROM (bảng dẫn xuất)

```sql
SELECT t.CustID, t.Tong
FROM (
    SELECT CustID, SUM(TotalAmount) AS Tong
    FROM SALEORDER
    WHERE Status = 'COMPLETED'
    GROUP BY CustID
) AS t
WHERE t.Tong > 20000;
```
Phần trong tạo bảng tạm `t` (5 dòng); phần ngoài lọc tiếp. Kết quả: khách 1 (26500), 2 (42800), 3 (30300). Cách này cho phép **lọc/ tính tiếp trên kết quả đã tổng hợp**. (Từ MySQL 8 có thể dùng CTE cho dễ đọc, Chương 10.)

### 8.8. Subquery so với JOIN

| Tiêu chí | Subquery | JOIN |
|---|---|---|
| Cần cột của bảng thứ hai trong kết quả? | ❌ Không | ✅ Có |
| Chỉ cần kiểm tra tồn tại / lọc | ✅ Gọn, tránh nhân dòng | Có thể nhân dòng → cần `DISTINCT` |
| Tìm giá trị lớn nhất/trung bình để so sánh | ✅ Tự nhiên | Khó hơn |
| Hiệu năng | MySQL 8 thường tối ưu tương đương | Thường nhanh, dễ tối ưu |

Hai câu cho cùng kết quả:
```sql
SELECT CustName FROM CUSTOMER WHERE CustID IN (SELECT CustID FROM SALEORDER);
SELECT DISTINCT c.CustName FROM CUSTOMER c JOIN SALEORDER o ON o.CustID = c.CustID;
```
Chọn **subquery** nếu chỉ cần lọc theo bảng kia; chọn **JOIN** nếu cần hiển thị cột của cả hai bảng.

### 8.9. Subquery + GROUP BY + HAVING

**Đề:** sản phẩm bán nhiều nhất (lấy cả khi đồng hạng).
```sql
SELECT p.ProdName, SUM(od.Quantity) AS DaBan
FROM PRODUCT p JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID
GROUP BY p.ProdID, p.ProdName
HAVING SUM(od.Quantity) = (
    SELECT MAX(s.Tong)
    FROM (SELECT SUM(Quantity) AS Tong FROM ORDER_DETAIL GROUP BY ProdID) s
);
```
Phần trong cùng: `SUM(Quantity)` mỗi sản phẩm → `6, 8, 3, 4, 4, 6, 5`; `MAX = 8`. Phần ngoài giữ sản phẩm có tổng bằng 8 → `Mouse Logitech | 8`. Nếu có hai sản phẩm cùng 8, cả hai đều xuất hiện.

### 8.10. Correlated subquery (truy vấn tương quan)

**Subquery tương quan** dùng cột của bảng ngoài, nên **chạy lại cho mỗi dòng ngoài**.

**Đề:** các đơn có tổng tiền **cao hơn mức trung bình của chính khách đó**.
```sql
SELECT o.OrderID, o.CustID, o.TotalAmount
FROM SALEORDER o
WHERE o.TotalAmount > (
    SELECT AVG(o2.TotalAmount)
    FROM SALEORDER o2
    WHERE o2.CustID = o.CustID        -- ← tham chiếu dòng ngoài
)
ORDER BY o.OrderID;
```
Trung bình mỗi khách: An 8833.33; Binh 19266.67; Cuong 15950; Dung 8750; Em 14000.

| OrderID | CustID | TotalAmount | So với TB khách |
|---|---|---|---|
| 1 | 1 | 15600.00 | > 8833 |
| 2 | 1 | 9200.00 | > 8833 |
| 5 | 3 | 30300.00 | > 15950 |
| 7 | 4 | 13000.00 | > 8750 |
| 9 | 5 | 19000.00 | > 14000 |
| 12 | 2 | 24000.00 | > 19267 |

Hai bí danh `o` và `o2` cho cùng bảng giúp phân biệt "dòng đang xét" và "dòng trong subquery".

### 8.11. ⭐ Phân tích câu UPDATE kết hợp Subquery + GROUP BY + HAVING

```sql
UPDATE EMPLOYEE
SET Salary = Salary * 1.1
WHERE EmpID IN (
    SELECT EmpID
    FROM SALEORDER
    WHERE Status = 'COMPLETED'
    GROUP BY EmpID
    HAVING SUM(TotalAmount) > 50000
);
```

**Câu này muốn nói gì (bằng tiếng Việt):** "Tăng lương 10% cho những nhân viên mà tổng tiền các đơn COMPLETED của họ vượt 50000."

**Bước 1 — Chạy riêng subquery để xem nó trả về gì:**
```sql
SELECT EmpID
FROM SALEORDER
WHERE Status = 'COMPLETED'
GROUP BY EmpID
HAVING SUM(TotalAmount) > 50000;
```
Kết quả (đã phân tích từng bước ở mục 7.8):

| EmpID |
|---|
| 2 |

Để **hiểu bản chất**, hãy xem thêm các số liệu mà nó đã dùng:
```sql
SELECT EmpID, SUM(TotalAmount) AS Tong
FROM SALEORDER WHERE Status = 'COMPLETED' GROUP BY EmpID;
```
| EmpID | Tong | Qua 50000? |
|---|---|---|
| 2 | 98100 | ✅ |
| 3 | 31800 | ❌ |
| 4 | 6200 | ❌ |

**Bước 2 — Thay kết quả vào câu ngoài.** Vì subquery trả `{2}`, câu lệnh tương đương:
```sql
UPDATE EMPLOYEE SET Salary = Salary * 1.1 WHERE EmpID IN (2);
```
→ chỉ nhân viên số 2 được tăng.

**Bước 3 — Xem trước bằng SELECT (thói quen an toàn):**
```sql
SELECT EmpID, EmpName, Salary, Salary * 1.1 AS LuongMoi
FROM EMPLOYEE
WHERE EmpID IN (SELECT EmpID FROM SALEORDER WHERE Status='COMPLETED'
                GROUP BY EmpID HAVING SUM(TotalAmount) > 50000);
```
| EmpID | EmpName | Salary | LuongMoi |
|---|---|---|---|
| 2 | Nguyen Thu Ha | 15000000.00 | 16500000.000 |

**Kết quả sau UPDATE:** chỉ nhân viên 2 đổi lương từ **15,000,000 → 16,500,000**. Nhân viên 1, 3, 4, 5 giữ nguyên.

Giờ trả lời các câu hỏi anh đặt ra:

**① SELECT bên trong WHERE trả về gì?** Trả về **một cột `EmpID` với 0, 1 hoặc nhiều dòng**, ở đây là `2`. Nó đóng vai một **danh sách các mã nhân viên** thỏa điều kiện.

**② Vì sao SELECT có thể nằm bên trong WHERE?** Vì `WHERE x IN (...)` chỉ cần **một tập giá trị** ở trong ngoặc, và kết quả của một `SELECT` chính là một tập giá trị. SQL không quan tâm tập đó được viết tay `(2, 5)` hay được tính ra bởi một câu `SELECT`. Hai dạng này hoàn toàn thay thế được cho nhau.

**③ `IN` giống `in` trong Python thế nào?** Gần như là một:
```python
# Python tương đương
ds_nv_gioi = [2]                       # = kết quả của subquery
for nv in nhan_vien:
    if nv.emp_id in ds_nv_gioi:        # = WHERE EmpID IN (...)
        nv.salary = nv.salary * 1.1    # = SET Salary = Salary * 1.1
```
Cũng như Python lặp qua từng nhân viên, `UPDATE` **xét từng dòng** của bảng `EMPLOYEE`; dòng nào có `EmpID` nằm trong danh sách thì được sửa.

**④ Vì sao `TotalAmount` thuộc `SALEORDER` mà `Salary` thuộc `EMPLOYEE`, vẫn viết chung một câu được?**
Vì mỗi câu `SELECT` có **phạm vi (`FROM`) riêng**:
- Câu **trong** (`FROM SALEORDER`) chỉ nhìn thấy cột của `SALEORDER` → dùng `Status`, `TotalAmount`, `EmpID`. Nhiệm vụ: **tìm ra những ai đủ điều kiện**.
- Câu **ngoài** (`UPDATE EMPLOYEE`) chỉ nhìn thấy cột của `EMPLOYEE` → dùng `Salary`, `EmpID`. Nhiệm vụ: **sửa lương những người đó**.
Hai câu **không trộn cột** với nhau. Chúng chỉ trao đổi **một thứ duy nhất: danh sách `EmpID`**.

**⑤ SQL dùng `EmpID` để xác định nhân viên cần cập nhật thế nào?**
`EmpID` là **khóa chung**: trong `SALEORDER` nó là khóa ngoại ("nhân viên nào lập đơn này"), trong `EMPLOYEE` nó là khóa chính ("mã nhân viên"). Subquery lấy ra các `EmpID` từ `SALEORDER`; câu ngoài so khớp `EmpID` của mỗi dòng `EMPLOYEE` với danh sách đó. Cùng một mã là cùng một người.

**Sơ đồ luồng:**
```
SALEORDER (12 dòng)
   │ WHERE Status = 'COMPLETED'        → 9 dòng
   │ GROUP BY EmpID                    → 3 nhóm (2, 3, 4)
   │ HAVING SUM(TotalAmount) > 50000   → còn nhóm 2
   ▼
  danh sách EmpID = {2}
   │
   ▼
EMPLOYEE: dòng nào có EmpID IN {2} → Salary = Salary * 1.1
```

**Cách viết tương đương bằng JOIN:**
```sql
UPDATE EMPLOYEE e
JOIN (
    SELECT EmpID FROM SALEORDER
    WHERE Status = 'COMPLETED'
    GROUP BY EmpID
    HAVING SUM(TotalAmount) > 50000
) t ON t.EmpID = e.EmpID
SET e.Salary = e.Salary * 1.1;
```
Bảng dẫn xuất `t` chứa các `EmpID` đủ điều kiện, `JOIN` giữ lại đúng nhân viên đó, `SET` tăng lương.

**Lỗi thường gặp ở dạng bài này:**

| Lỗi | Hậu quả |
|---|---|
| Quên `WHERE Status = 'COMPLETED'` | Đếm cả đơn huỷ, chờ → NV 3 có 55800 > 50000 cũng bị tăng lương nhầm |
| Dùng `WHERE SUM(...) > 50000` thay vì `HAVING` | Lỗi 1111 |
| Subquery `SELECT EmpID, SUM(...)` (2 cột) với `IN` | Lỗi 1241 *Operand should contain 1 column* |
| Chạy `UPDATE` ngay, không `SELECT` trước | Không thể kiểm tra, sai là mất dữ liệu |
| Chạy lệnh **nhiều lần** | Mỗi lần nhân thêm 1.1 → lương tăng chồng |

Ví dụ lỗi thứ nhất: với dữ liệu mẫu, nếu bỏ điều kiện `Status`, tổng mọi đơn của NV 3 = 55800 > 50000 → NV 3 bị tăng lương oan.

### 8.12. Subquery với UPDATE (thêm ví dụ)

**Đề:** đặt tồn kho = 0 cho các sản phẩm chưa từng bán.
```sql
UPDATE PRODUCT
SET Stock = 0
WHERE ProdID NOT IN (SELECT ProdID FROM ORDER_DETAIL);       -- chỉ ProdID 8
```
**Đề:** đặt lại `TotalAmount` của mỗi đơn bằng tổng chi tiết (subquery tương quan trong SET):
```sql
UPDATE SALEORDER o
SET o.TotalAmount = (
    SELECT SUM(od.Quantity * od.UnitPrice)
    FROM ORDER_DETAIL od
    WHERE od.OrderID = o.OrderID
);
```
(Đơn không có chi tiết sẽ thành NULL → bọc `COALESCE(..., 0)` hoặc thêm `WHERE EXISTS (...)`.)

### 8.13. Subquery với DELETE

```sql
-- Xóa khách chưa từng có đơn hàng
DELETE FROM CUSTOMER
WHERE CustID NOT IN (SELECT CustID FROM SALEORDER);          -- xoá khách 6
```
**Lỗi 1093** (cùng bảng trong DELETE/UPDATE và subquery):
```sql
DELETE FROM EMPLOYEE
WHERE EmpID IN (SELECT EmpID FROM EMPLOYEE WHERE Salary < 11000000);   -- ❌ lỗi 1093
```
Cách sửa: bọc subquery thêm một lớp bảng dẫn xuất:
```sql
DELETE FROM EMPLOYEE
WHERE EmpID IN (SELECT EmpID FROM (SELECT EmpID FROM EMPLOYEE WHERE Salary < 11000000) AS tmp);
```
(Lưu ý ràng buộc khóa ngoại: chỉ xóa được nhân viên chưa có đơn và không là quản lý của ai.)

### 8.14. Subquery với INSERT ... SELECT

Subquery có thể nằm ở **ba chỗ** trong một câu `INSERT ... SELECT`: trong `WHERE` của phần SELECT, trong danh sách cột của SELECT (tương quan), hoặc trong `FROM` (bảng dẫn xuất). Nguyên tắc cũ vẫn đúng: cột của `SELECT` ghép với cột đích **theo vị trí**.

**a) Subquery với IN/HAVING ở WHERE: lưu tên các khách chi tiêu trên 30000**
```sql
CREATE TABLE VIP_NAMES (CustID INT PRIMARY KEY, CustName VARCHAR(100));

INSERT INTO VIP_NAMES (CustID, CustName)
SELECT CustID, CustName
FROM CUSTOMER
WHERE CustID IN (
    SELECT CustID FROM SALEORDER
    GROUP BY CustID
    HAVING SUM(TotalAmount) > 30000
);
```
*Xây từng bước:* (1) chạy riêng subquery → `2, 3` (tổng 57800 và 31900); (2) chạy câu SELECT ngoài → 2 dòng; (3) bọc `INSERT`.
**Kết quả:** `VIP_NAMES` có `(2, Tran Thi Binh)` và `(3, Le Van Cuong)`.

**b) Subquery tương quan trong danh sách cột: thống kê số đơn mỗi nhân viên**
```sql
CREATE TABLE EMP_STATS (EmpID INT PRIMARY KEY, SoDon INT);

INSERT INTO EMP_STATS (EmpID, SoDon)
SELECT e.EmpID,
       (SELECT COUNT(*) FROM SALEORDER o WHERE o.EmpID = e.EmpID)
FROM EMPLOYEE e;
```
**Kết quả:** 5 dòng: `(1, 0)`, `(2, 5)`, `(3, 4)`, `(4, 3)`, `(5, 0)`. Nhân viên chưa có đơn vẫn xuất hiện với 0 (vì `COUNT(*)` trên tập rỗng là 0).

**c) NOT EXISTS: lưu sản phẩm chưa từng bán**
```sql
CREATE TABLE DEAD_STOCK (ProdID INT PRIMARY KEY, ProdName VARCHAR(100), Stock INT);

INSERT INTO DEAD_STOCK (ProdID, ProdName, Stock)
SELECT p.ProdID, p.ProdName, p.Stock
FROM PRODUCT p
WHERE NOT EXISTS (SELECT 1 FROM ORDER_DETAIL od WHERE od.ProdID = p.ProdID);
```
**Kết quả:** `(8, Webcam, 15)`.

**d) Subquery scalar: lưu các đơn lớn hơn mức trung bình**
```sql
CREATE TABLE BIG_ORDER (OrderID INT PRIMARY KEY, TotalAmount DECIMAL(12,2));

INSERT INTO BIG_ORDER (OrderID, TotalAmount)
SELECT OrderID, TotalAmount
FROM SALEORDER
WHERE TotalAmount > (SELECT AVG(TotalAmount) FROM SALEORDER);     -- AVG = 13475
```
**Kết quả:** 6 dòng: đơn 1 (15600), 3 (18800), 4 (15000), 5 (30300), 9 (19000), 12 (24000).

**e) Subquery trong FROM: lưu thống kê mỗi khách rồi lọc**
```sql
INSERT INTO CUSTOMER_SUMMARY (CustID, SoDon, TongTien)
SELECT t.CustID, t.SoDon, t.Tong
FROM (SELECT CustID, COUNT(*) AS SoDon, SUM(TotalAmount) AS Tong
      FROM SALEORDER WHERE Status = 'COMPLETED' GROUP BY CustID) AS t
WHERE t.Tong > 20000;
```
(Giả định `CUSTOMER_SUMMARY` đã tạo ở mục 11.6 và đã `TRUNCATE`.) **Kết quả:** khách 1 (3 đơn, 26500), 2 (2, 42800), 3 (1, 30300).

**Lỗi thường gặp ở dạng này:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| `INSERT ... VALUES (SELECT ...)` | Lỗi cú pháp | Bỏ `VALUES`, đưa thẳng `SELECT` |
| Subquery trong `INSERT ... SELECT` trả 2 cột cho `IN` | Lỗi 1241 | Chỉ 1 cột |
| `NOT IN` với cột có NULL | Không chèn dòng nào | `NOT EXISTS` |
| Subquery scalar trả nhiều dòng với `>` | Lỗi 1242 | Dùng hàm tổng hợp |
| Thứ tự cột SELECT sai thứ tự cột đích | Dữ liệu sai âm thầm | Đối chiếu từng vị trí |
| Chạy lại không dọn bảng đích | Lỗi 1062 | `TRUNCATE` / `ON DUPLICATE KEY UPDATE` |

### 8.15. Lỗi thường gặp tổng hợp với Subquery

| Lỗi MySQL | Nguyên nhân | Cách sửa |
|---|---|---|
| 1242 Subquery returns more than 1 row | Dùng `=` với subquery nhiều dòng | `IN`, hoặc `MAX/MIN`, `LIMIT 1` |
| 1241 Operand should contain 1 column | `IN (SELECT a, b ...)` | Chỉ chọn 1 cột |
| 1248 Every derived table must have its own alias | Subquery trong FROM thiếu bí danh | `... ) AS t` |
| 1093 target table | UPDATE/DELETE bảng cũng nằm trong subquery | Bọc thêm lớp, hoặc JOIN |
| Kết quả rỗng với `NOT IN` | Subquery có NULL | `NOT EXISTS` hoặc `WHERE x IS NOT NULL` |

### 8.16. Bài tập tự luyện Chương 8

1. Khách có tổng chi tiêu (mọi đơn) lớn hơn 30000, **không dùng JOIN**.
2. Sản phẩm chưa bán được trong bất kỳ đơn `COMPLETED` nào (dùng `NOT EXISTS`).
3. Tăng giá 5% cho sản phẩm thuộc nhóm hàng có giá trung bình lớn hơn 3000.
4. Đơn có tổng tiền lớn hơn tổng tiền trung bình **của tất cả các đơn**.

<details><summary>Đáp án</summary>

```sql
-- 1  → CustID 2 (57800), 3 (31900)
SELECT CustID, CustName FROM CUSTOMER
WHERE CustID IN (SELECT CustID FROM SALEORDER GROUP BY CustID HAVING SUM(TotalAmount) > 30000);

-- 2  → Webcam
SELECT p.ProdName FROM PRODUCT p
WHERE NOT EXISTS (
    SELECT 1 FROM ORDER_DETAIL od JOIN SALEORDER o ON o.OrderID = od.OrderID
    WHERE od.ProdID = p.ProdID AND o.Status = 'COMPLETED'
);

-- 3  → Electronics (TB (15000+4000+9000)/3 = 9333) ✔; Accessories (TB = 650) ✘
UPDATE PRODUCT SET Price = Price * 1.05
WHERE Category IN (
    SELECT Category FROM (SELECT Category FROM PRODUCT GROUP BY Category HAVING AVG(Price) > 3000) t
);

-- 4  → TB = 13475; đơn 1 (15600), 3 (18800), 4 (15000), 5 (30300), 9 (19000), 12 (24000)
SELECT OrderID, TotalAmount FROM SALEORDER
WHERE TotalAmount > (SELECT AVG(TotalAmount) FROM SALEORDER);
```
Câu 2: kết quả là **chỉ Webcam** (USB 64GB có trong đơn 8 COMPLETED nên bị loại).
Câu 3: bọc thêm bảng dẫn xuất `t` để tránh lỗi 1093 vì subquery đọc đúng bảng `PRODUCT` đang được UPDATE.
</details>

---

### 8.17. Bài tập tự luyện theo từng loại truy vấn con (có đáp án)

| # | Loại | Đề |
|---|---|---|
| 1 | Scalar trong WHERE | Sản phẩm có giá **thấp hơn** giá trung bình. |
| 2 | IN | Khách đã mua Laptop (ProdID 1) ở bất kỳ đơn nào. |
| 3 | NOT IN | Sản phẩm không xuất hiện trong đơn PENDING nào. |
| 4 | EXISTS | Các đơn có chứa Laptop. |
| 5 | NOT EXISTS | Khách chưa có đơn CANCELLED nào. |
| 6 | ALL | Đơn có tổng **lớn hơn mọi** đơn PENDING. |
| 7 | Trong SELECT | Mỗi nhân viên kèm đơn có tổng lớn nhất (NULL nếu chưa có đơn). |
| 8 | Trong FROM | Số đơn trung bình của mỗi nhân viên (chỉ tính người có đơn). |
| 9 | Tương quan | Sản phẩm có tồn kho lớn hơn tồn kho trung bình của **nhóm hàng của nó**. |

<details><summary>Đáp án</summary>

```sql
-- 1  → Mouse, Keyboard, Headphone, USB, Webcam (TB = 3906.25)
SELECT ProdName FROM PRODUCT WHERE Price < (SELECT AVG(Price) FROM PRODUCT);

-- 2  → khách 1, 2, 3, 5
SELECT CustID, CustName FROM CUSTOMER
WHERE CustID IN (SELECT o.CustID FROM SALEORDER o JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID WHERE od.ProdID = 1);

-- 3  → ProdID 1, 3, 4, 5, 8 (sản phẩm đã vào đơn PENDING là 2, 6, 7)
SELECT ProdID, ProdName FROM PRODUCT
WHERE ProdID NOT IN (SELECT od.ProdID FROM ORDER_DETAIL od JOIN SALEORDER o ON o.OrderID = od.OrderID WHERE o.Status = 'PENDING');

-- 4  → đơn 1, 4, 5, 9, 12
SELECT OrderID FROM SALEORDER o
WHERE EXISTS (SELECT 1 FROM ORDER_DETAIL od WHERE od.OrderID = o.OrderID AND od.ProdID = 1);

-- 5  → khách 1, 3, 4, 5, 6
SELECT CustID, CustName FROM CUSTOMER c
WHERE NOT EXISTS (SELECT 1 FROM SALEORDER o WHERE o.CustID = c.CustID AND o.Status = 'CANCELLED');

-- 6  → đơn 1, 2, 3, 4, 5, 7, 9, 12 (đơn PENDING lớn nhất là 9000; đơn 2 có 9200 > 9000)
SELECT OrderID, TotalAmount FROM SALEORDER
WHERE TotalAmount > ALL (SELECT TotalAmount FROM SALEORDER WHERE Status = 'PENDING');

-- 7  → NV1 NULL, NV2 30300, NV3 18800, NV4 4500, NV5 NULL
SELECT e.EmpName, (SELECT MAX(o.TotalAmount) FROM SALEORDER o WHERE o.EmpID = e.EmpID) AS DonLonNhat
FROM EMPLOYEE e;

-- 8  → 4.0 (5, 4, 3 đơn)
SELECT AVG(t.SoDon) FROM (SELECT COUNT(*) AS SoDon FROM SALEORDER GROUP BY EmpID) t;

-- 9  → Monitor (30 > 25), Mouse (100 > 81), USB (200 > 81). Smartphone tồn 25 không lớn hơn TB 25
SELECT p.ProdName, p.Category, p.Stock FROM PRODUCT p
WHERE p.Stock > (SELECT AVG(p2.Stock) FROM PRODUCT p2 WHERE p2.Category = p.Category);
```
</details>

---

## CHƯƠNG 9: UNION VÀ CÁC TOÁN TỬ TẬP HỢP

### 9.1. UNION và UNION ALL

**Công dụng:** **xếp chồng** kết quả của hai (hoặc nhiều) câu `SELECT` thành một bảng. Nếu JOIN là nối **theo chiều ngang** (thêm cột), thì UNION là nối **theo chiều dọc** (thêm dòng).

**Cú pháp:**
```sql
SELECT ... FROM ...
UNION [ALL]
SELECT ... FROM ...
[ORDER BY ...];
```

| | `UNION` | `UNION ALL` |
|---|---|---|
| Trùng lặp | **Loại bỏ** dòng trùng | **Giữ nguyên** mọi dòng |
| Tốc độ | Chậm hơn (phải so sánh để loại trùng) | Nhanh hơn |
| Dùng khi | Muốn danh sách không trùng | Biết chắc không trùng, hoặc cần giữ trùng (đếm, cộng) |

**Ví dụ minh họa trùng lặp:**
```sql
SELECT City FROM CUSTOMER
UNION
SELECT City FROM CUSTOMER;          -- 4 dòng: Ha Noi, Ho Chi Minh, Da Nang, Hai Phong

SELECT City FROM CUSTOMER
UNION ALL
SELECT City FROM CUSTOMER;          -- 12 dòng (6 + 6, giữ hết)
```

### 9.2. Điều kiện để kết hợp hai truy vấn

1. **Cùng số cột.**
2. Cột tương ứng có **kiểu tương thích** (chữ với chữ, số với số).
3. **Tên cột kết quả** lấy từ câu `SELECT` **đầu tiên**.
4. `ORDER BY`/`LIMIT` đặt ở **cuối cùng**, áp dụng cho **toàn bộ** kết quả.

**Ví dụ: danh bạ chung gồm khách và nhân viên**
```sql
SELECT CustName AS Ten, Phone AS DienThoai, 'Khach hang' AS Loai FROM CUSTOMER
UNION ALL
SELECT EmpName, NULL, 'Nhan vien' FROM EMPLOYEE
ORDER BY Ten
LIMIT 5;
```
| Ten | DienThoai | Loai |
|---|---|---|
| Do Minh Quan | NULL | Nhan vien |
| Hoang Van Em | 0901000005 | Khach hang |
| Le Thi Lan | NULL | Nhan vien |
| Le Van Cuong | 0901000003 | Khach hang |
| Nguyen Thu Ha | NULL | Nhan vien |

Cột `Loai` là **cột hằng** để biết dòng đến từ đâu; `NULL` điền vào vị trí không có dữ liệu (EMPLOYEE không có `Phone`) để **đủ 3 cột**.

**Ví dụ: báo cáo có dòng tổng cộng**
```sql
SELECT Status, SUM(TotalAmount) AS Tong FROM SALEORDER GROUP BY Status
UNION ALL
SELECT 'TONG CONG', SUM(TotalAmount) FROM SALEORDER;
```
| Status | Tong |
|---|---|
| COMPLETED | 136100.00 |
| PENDING | 10600.00 |
| CANCELLED | 15000.00 |
| TONG CONG | 161700.00 |

(Thứ tự dòng đầu không đảm bảo nếu không có `ORDER BY`.) Dùng **`UNION ALL`**, vì nếu dùng `UNION` mà vô tình có hai dòng trùng giá trị thì sẽ bị loại mất.

### 9.3. Khi nào dùng UNION thay vì JOIN?

| Tình huống | Dùng |
|---|---|
| Ghép thêm **cột** từ bảng liên quan (khách + đơn) | `JOIN` |
| Gộp **danh sách cùng dạng** từ nhiều nguồn (khách + nhân viên; đơn năm nay + đơn lưu trữ) | `UNION [ALL]` |
| Báo cáo cần dòng "Tổng cộng" | `UNION ALL` |
| Muốn `FULL OUTER JOIN` (MySQL không có) | `LEFT JOIN` `UNION` `RIGHT JOIN` |

**Giả lập FULL OUTER JOIN:**
```sql
SELECT c.CustName, o.OrderID FROM CUSTOMER c LEFT  JOIN SALEORDER o ON o.CustID = c.CustID
UNION
SELECT c.CustName, o.OrderID FROM CUSTOMER c RIGHT JOIN SALEORDER o ON o.CustID = c.CustID;
```

### 9.4. Toán tử tập hợp khác

MySQL **8.0.31 trở lên** hỗ trợ `INTERSECT` (phần chung) và `EXCEPT` (phần chỉ có ở vế trái). Với bản cũ hơn dùng `IN`/`EXISTS`/`LEFT JOIN ... IS NULL`.
```sql
-- Khách có đơn COMPLETED nhưng KHÔNG có đơn PENDING (MySQL 8.0.31+)
SELECT CustID FROM SALEORDER WHERE Status = 'COMPLETED'
EXCEPT
SELECT CustID FROM SALEORDER WHERE Status = 'PENDING';        -- → 1, 2, 4
```

**Lỗi thường gặp:** số cột không bằng nhau (lỗi 1222); đặt `ORDER BY` sau từng `SELECT` con mà không bọc ngoặc; lẫn kiểu dữ liệu (chữ với số); nhầm `UNION` với `UNION ALL` khi cộng tổng.

### 9.5. Bài tập tự luyện Chương 9

1. Gộp danh sách thành phố của khách và tên thành phố `'Can Tho'` (cố định), không trùng.
2. Liệt kê số đơn theo trạng thái, kèm dòng `TONG` ở cuối.

<details><summary>Đáp án</summary>

```sql
-- 1  → Ha Noi, Ho Chi Minh, Da Nang, Hai Phong, Can Tho
SELECT City FROM CUSTOMER UNION SELECT 'Can Tho';

-- 2  → COMPLETED 9, PENDING 2, CANCELLED 1, TONG 12
SELECT Status, COUNT(*) AS SoDon FROM SALEORDER GROUP BY Status
UNION ALL
SELECT 'TONG', COUNT(*) FROM SALEORDER;
```
</details>

---

### 9.6. Bài tập tự luyện bổ sung Chương 9

1. Chạy riêng ba câu và cho biết số dòng: (a) `SELECT CustID FROM SALEORDER UNION SELECT CustID FROM CUSTOMER`; (b) `SELECT CustID FROM SALEORDER UNION ALL SELECT CustID FROM SALEORDER`.
2. Sửa lỗi: `SELECT CustID, CustName FROM CUSTOMER UNION SELECT EmpID FROM EMPLOYEE`.
3. Vì sao báo cáo "doanh thu từng trạng thái + dòng tổng cộng" nên dùng `UNION ALL`?

<details><summary>Đáp án</summary>

1. (a) **6** dòng (khách 1–6, trùng đã bị loại); (b) **24** dòng (12 + 12, giữ hết).
2. Lỗi 1222 (số cột khác nhau). Sửa: `SELECT CustID, CustName FROM CUSTOMER UNION SELECT EmpID, EmpName FROM EMPLOYEE;` (hai cột kiểu tương thích). Lưu ý `CustID` và `EmpID` trùng số nhưng `CustName`/`EmpName` khác nhau nên không bị gộp.
3. `UNION` loại dòng trùng toàn phần: nếu dòng tổng cộng vô tình trùng giá trị với dòng nhóm nào đó (ví dụ chỉ có một trạng thái), nó sẽ bị loại mất. `UNION ALL` giữ nguyên và nhanh hơn.
</details>

---

## CHƯƠNG 10: CTE VÀ WINDOW FUNCTIONS

> Chỉ học chương này khi đã vững Chương 4–8. Cần **MySQL 8.0 trở lên** (MySQL 5.7 không có CTE và Window Functions).

### 10.1. CTE (Common Table Expression) với WITH

**CTE** là một **bảng tạm có tên**, định nghĩa ở đầu câu lệnh bằng `WITH`, chỉ tồn tại trong câu lệnh đó. Cách dùng giống bảng dẫn xuất ở `FROM`, nhưng **đặt tên và viết trước**, giúp câu dài dễ đọc.

**Cú pháp:**
```sql
WITH ten_cte AS (
    SELECT ...
)
SELECT ... FROM ten_cte ...;
```

**Ví dụ 1:** tên khách và tổng chi tiêu COMPLETED.
```sql
WITH cust_total AS (
    SELECT CustID, SUM(TotalAmount) AS Tong
    FROM SALEORDER
    WHERE Status = 'COMPLETED'
    GROUP BY CustID
)
SELECT c.CustName, t.Tong
FROM CUSTOMER c
JOIN cust_total t ON t.CustID = c.CustID
ORDER BY t.Tong DESC;
```
| CustName | Tong |
|---|---|
| Tran Thi Binh | 42800.00 |
| Le Van Cuong | 30300.00 |
| Nguyen Van An | 26500.00 |
| Hoang Van Em | 19000.00 |
| Pham Thi Dung | 17500.00 |

Giải thích: `cust_total` là "bảng" 5 dòng (mỗi khách một dòng). Câu `SELECT` chính coi nó như bảng thật và JOIN với `CUSTOMER`.

**Ví dụ 2 — nhiều CTE, CTE sau dùng CTE trước:** khách chi tiêu trên mức trung bình.
```sql
WITH t AS (
    SELECT CustID, SUM(TotalAmount) AS Tong FROM SALEORDER GROUP BY CustID
),
a AS (
    SELECT AVG(Tong) AS TB FROM t
)
SELECT c.CustName, t.Tong
FROM t
JOIN a ON t.Tong > a.TB
JOIN CUSTOMER c ON c.CustID = t.CustID;
```
→ `Tran Thi Binh | 57800.00` (trung bình 32340). Hai CTE ngăn cách bằng dấu `,`; chỉ viết `WITH` **một lần**. So sánh với bản subquery ở mục 7.11: cùng kết quả, nhưng đọc từ trên xuống dễ hơn.

**Ví dụ 3 — CTE đệ quy (sơ đồ tổ chức):**
```sql
WITH RECURSIVE org AS (
    SELECT EmpID, EmpName, 1 AS Cap FROM EMPLOYEE WHERE ManagerID IS NULL
    UNION ALL
    SELECT e.EmpID, e.EmpName, o.Cap + 1
    FROM EMPLOYEE e JOIN org o ON e.ManagerID = o.EmpID
)
SELECT EmpName, Cap FROM org ORDER BY Cap, EmpID;
```
| EmpName | Cap |
|---|---|
| Do Minh Quan | 1 |
| Nguyen Thu Ha | 2 |
| Tran Quoc Huy | 2 |
| Le Thi Lan | 2 |
| Pham Duc Minh | 3 |

(Phần đầu là "mỏ neo": người không có quản lý. Phần sau lặp lại: tìm cấp dưới của những người đã có, đến khi hết.)

### 10.2. CTE hay subquery?

| Dùng CTE khi | Dùng subquery khi |
|---|---|
| Cần dùng **cùng một kết quả nhiều lần** | Chỉ dùng một lần, rất ngắn |
| Truy vấn nhiều tầng, cần đọc từ trên xuống | Điều kiện đơn giản `IN (...)`, `EXISTS` |
| Cần đệ quy | |
| Muốn tách "bước 1, bước 2, bước 3" cho dễ debug | |

CTE không nhanh hơn subquery; lợi ích chính là **dễ đọc, dễ sửa**.

### 10.3. Window Function là gì? Khác GROUP BY thế nào?

**Window function** tính toán trên **một "cửa sổ" các dòng liên quan**, nhưng **giữ nguyên từng dòng** trong kết quả (không nén thành một dòng như `GROUP BY`).

| | `GROUP BY` | Window function |
|---|---|---|
| Số dòng kết quả | **Ít đi** (1 dòng / nhóm) | **Giữ nguyên** |
| Hiển thị cột chi tiết cùng số tổng? | ❌ Không | ✅ Có |
| Cú pháp | `GROUP BY cột` | `hàm() OVER (...)` |
| Dùng cho | Báo cáo tổng hợp | Xếp hạng, lũy kế, so sánh với tổng nhóm |

**Cú pháp:**
```sql
ham_cua_so() OVER (
    [PARTITION BY cot_chia_nhom]
    [ORDER BY cot_sap_xep]
)
```
- `OVER (...)`: đánh dấu đây là window function.
- `PARTITION BY`: chia dòng thành các "cửa sổ" riêng (giống `GROUP BY` nhưng **không nén dòng**). Bỏ đi thì cả bảng là một cửa sổ.
- `ORDER BY` trong `OVER`: thứ tự dòng **bên trong cửa sổ** (cần cho xếp hạng và lũy kế); **khác** `ORDER BY` ở cuối câu lệnh.

### 10.4. SUM() OVER và AVG() OVER

**So sánh với tổng của khách, nhưng vẫn giữ từng đơn:**
```sql
SELECT OrderID, CustID, TotalAmount,
       SUM(TotalAmount) OVER (PARTITION BY CustID)                          AS TongKhach,
       ROUND(TotalAmount / SUM(TotalAmount) OVER (PARTITION BY CustID) * 100, 1) AS PhanTram
FROM SALEORDER
ORDER BY OrderID
LIMIT 6;
```
| OrderID | CustID | TotalAmount | TongKhach | PhanTram |
|---|---|---|---|---|
| 1 | 1 | 15600.00 | 26500.00 | 58.9 |
| 2 | 1 | 9200.00 | 26500.00 | 34.7 |
| 3 | 2 | 18800.00 | 57800.00 | 32.5 |
| 4 | 2 | 15000.00 | 57800.00 | 26.0 |
| 5 | 3 | 30300.00 | 31900.00 | 95.0 |
| 6 | 3 | 1600.00 | 31900.00 | 5.0 |

Với `GROUP BY` chỉ ra được `TongKhach`; không đồng thời giữ từng `OrderID` được.

**AVG() OVER: chênh lệch so với trung bình của khách** (khách 1):
```sql
SELECT OrderID, TotalAmount,
       ROUND(AVG(TotalAmount) OVER (PARTITION BY CustID), 2)              AS TB_Khach,
       ROUND(TotalAmount - AVG(TotalAmount) OVER (PARTITION BY CustID), 2) AS ChenhLech
FROM SALEORDER
WHERE CustID = 1
ORDER BY OrderID;
```
| OrderID | TotalAmount | TB_Khach | ChenhLech |
|---|---|---|---|
| 1 | 15600.00 | 8833.33 | 6766.67 |
| 2 | 9200.00 | 8833.33 | 366.67 |
| 11 | 1700.00 | 8833.33 | -7133.33 |

(Có thể thay cho subquery tương quan ở mục 8.10.)

**Lũy kế (running total):** thêm `ORDER BY` trong `OVER`.
```sql
SELECT OrderID, OrderDate, TotalAmount,
       SUM(TotalAmount) OVER (ORDER BY OrderDate, OrderID) AS LuyKe
FROM SALEORDER
WHERE Status = 'COMPLETED';
```
| OrderID | OrderDate | TotalAmount | LuyKe |
|---|---|---|---|
| 1 | 2025-01-05 | 15600.00 | 15600.00 |
| 2 | 2025-02-10 | 9200.00 | 24800.00 |
| 3 | 2025-02-14 | 18800.00 | 43600.00 |
| 5 | 2025-03-12 | 30300.00 | 73900.00 |
| 7 | 2025-04-15 | 13000.00 | 86900.00 |
| 8 | 2025-05-02 | 4500.00 | 91400.00 |
| 9 | 2025-05-20 | 19000.00 | 110400.00 |
| 11 | 2025-06-25 | 1700.00 | 112100.00 |
| 12 | 2025-07-07 | 24000.00 | 136100.00 |

Dòng cuối = 136100 = tổng doanh thu COMPLETED. Thứ tự xử lý: `WHERE` lọc 9 đơn → window tính lũy kế trên 9 đơn đó.

### 10.5. ROW_NUMBER, RANK, DENSE_RANK

| Hàm | Khi có đồng hạng |
|---|---|
| `ROW_NUMBER()` | Luôn đánh số 1, 2, 3, 4... **không trùng** (đồng hạng vẫn khác số) |
| `RANK()` | Đồng hạng cùng số, **bỏ số kế tiếp**: 1, 2, 2, **4** |
| `DENSE_RANK()` | Đồng hạng cùng số, **không bỏ số**: 1, 2, 2, **3** |

```sql
WITH sold AS (
    SELECT p.ProdName, SUM(od.Quantity) AS DaBan
    FROM PRODUCT p JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID
    GROUP BY p.ProdID, p.ProdName
)
SELECT ProdName, DaBan,
       ROW_NUMBER() OVER (ORDER BY DaBan DESC, ProdName) AS rn,
       RANK()       OVER (ORDER BY DaBan DESC)           AS rk,
       DENSE_RANK() OVER (ORDER BY DaBan DESC)           AS dr
FROM sold
ORDER BY DaBan DESC, ProdName;
```
| ProdName | DaBan | rn | rk | dr |
|---|---|---|---|---|
| Mouse Logitech | 8 | 1 | 1 | 1 |
| Laptop Dell | 6 | 2 | 2 | 2 |
| USB 64GB | 6 | 3 | 2 | 2 |
| Smartphone | 5 | 4 | 4 | 3 |
| Headphone | 4 | 5 | 5 | 4 |
| Monitor 24 inch | 4 | 6 | 5 | 4 |
| Keyboard Mechanical | 3 | 7 | 7 | 5 |

Laptop và USB bán bằng nhau (6) → `RANK` cho cả hai hạng 2 và nhảy tới 4; `DENSE_RANK` cho hạng 3 kế tiếp.

**Top 1 theo từng nhóm — kỹ thuật kinh điển (`PARTITION BY` + `ROW_NUMBER`):** đơn lớn nhất của mỗi khách.
```sql
WITH ranked AS (
    SELECT OrderID, CustID, TotalAmount,
           ROW_NUMBER() OVER (PARTITION BY CustID ORDER BY TotalAmount DESC) AS rn
    FROM SALEORDER
)
SELECT OrderID, CustID, TotalAmount
FROM ranked
WHERE rn = 1
ORDER BY CustID;
```
| OrderID | CustID | TotalAmount |
|---|---|---|
| 1 | 1 | 15600.00 |
| 12 | 2 | 24000.00 |
| 5 | 3 | 30300.00 |
| 7 | 4 | 13000.00 |
| 9 | 5 | 19000.00 |

**Vì sao phải dùng CTE?** Window function chạy **sau** `WHERE`, nên **không viết được** `WHERE rn = 1` trong cùng `SELECT` đã tính `rn`. Ta tính `rn` ở CTE (hoặc bảng dẫn xuất) rồi lọc ở truy vấn ngoài.

**Sản phẩm bán nhiều nhất, kể cả đồng hạng:** thay `ROW_NUMBER` bằng `RANK` và lọc `rk = 1`.

### 10.6. Lỗi thường gặp

| Lỗi | Giải thích | Sửa |
|---|---|---|
| `WHERE ROW_NUMBER() OVER (...) = 1` | Window function không dùng được trong `WHERE`/`HAVING` | Bọc CTE/subquery rồi lọc ở ngoài |
| Quên `ORDER BY` trong `OVER` khi xếp hạng | Kết quả vô nghĩa / lỗi | `OVER (ORDER BY ...)` |
| Nhầm `ROW_NUMBER` với `RANK` khi có đồng hạng | Mất dòng đồng hạng / thừa dòng | Chọn đúng hàm theo yêu cầu |
| Dùng MySQL 5.7 | Lỗi cú pháp | Cần 8.0+ |
| `ORDER BY` trong `OVER` ≠ `ORDER BY` cuối câu | Hai thứ độc lập | Viết cả hai nếu muốn kết quả có thứ tự |

### 10.7. Bài tập tự luyện Chương 10

1. Xếp hạng khách theo tổng chi tiêu COMPLETED (dùng `RANK`).
2. Với mỗi nhân viên, lấy **hai đơn gần nhất**.
3. Tính lũy kế số đơn theo ngày (mọi trạng thái).

<details><summary>Đáp án</summary>

```sql
-- 1  → Binh 1, Cuong 2, An 3, Em 4, Dung 5
SELECT c.CustName, t.Tong, RANK() OVER (ORDER BY t.Tong DESC) AS Hang
FROM CUSTOMER c
JOIN (SELECT CustID, SUM(TotalAmount) AS Tong FROM SALEORDER
      WHERE Status = 'COMPLETED' GROUP BY CustID) t ON t.CustID = c.CustID;

-- 2  → NV2: đơn 12, 9; NV3: đơn 10, 7; NV4: đơn 11, 8
WITH r AS (
    SELECT OrderID, EmpID, OrderDate,
           ROW_NUMBER() OVER (PARTITION BY EmpID ORDER BY OrderDate DESC) AS rn
    FROM SALEORDER
)
SELECT OrderID, EmpID, OrderDate FROM r WHERE rn <= 2 ORDER BY EmpID, OrderDate DESC;

-- 3
SELECT OrderID, OrderDate, COUNT(*) OVER (ORDER BY OrderDate, OrderID) AS LuyKeSoDon
FROM SALEORDER;
```
</details>

---

### 10.8. Bài tập tự luyện bổ sung theo từng khái niệm (có đáp án)

| # | Khái niệm | Đề |
|---|---|---|
| 1 | CTE | Dùng CTE tính tổng số lượng mỗi sản phẩm, rồi liệt kê sản phẩm bán nhiều hơn mức trung bình. |
| 2 | ROW_NUMBER + PARTITION | Hai sản phẩm bán chạy nhất của mỗi nhóm hàng. |
| 3 | RANK / DENSE_RANK | Xếp hạng khách theo số đơn (mọi trạng thái): cho cả `RANK` và `DENSE_RANK`. |
| 4 | SUM() OVER | Lũy kế doanh số của khách 2 theo ngày. |

<details><summary>Đáp án</summary>

```sql
-- 1  → Mouse 8, Laptop 6, USB 6 (TB = 36 / 7 ≈ 5,14; Smartphone 5 không vượt)
WITH s AS (SELECT ProdID, SUM(Quantity) AS q FROM ORDER_DETAIL GROUP BY ProdID)
SELECT p.ProdName, s.q
FROM s JOIN PRODUCT p ON p.ProdID = s.ProdID
WHERE s.q > (SELECT AVG(q) FROM s);

-- 2  → Accessories: Mouse 8, USB 6; Electronics: Laptop 6, Smartphone 5
WITH s AS (
    SELECT p.ProdName, p.Category, SUM(od.Quantity) AS q
    FROM PRODUCT p JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID
    GROUP BY p.ProdID, p.ProdName, p.Category
), r AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY Category ORDER BY q DESC) AS rn FROM s
)
SELECT Category, ProdName, q FROM r WHERE rn <= 2 ORDER BY Category, rn;

-- 3  → Khách 1 và 2 (3 đơn): RANK 1 / DENSE 1; khách 3, 4, 5 (2 đơn): RANK 3 / DENSE 2
SELECT CustID, COUNT(*) AS SoDon,
       RANK()       OVER (ORDER BY COUNT(*) DESC) AS Hang,
       DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS HangDac
FROM SALEORDER GROUP BY CustID;

-- 4  → đơn 3: 18800; đơn 4: 33800; đơn 12: 57800
SELECT OrderID, OrderDate, TotalAmount,
       SUM(TotalAmount) OVER (ORDER BY OrderDate, OrderID) AS LuyKe
FROM SALEORDER WHERE CustID = 2;
```
</details>

---

## CHƯƠNG 11: INSERT INTO ... SELECT

> Anh bảo hay nhầm phần này, nên em tách riêng và nhấn mạnh **điểm mấu chốt duy nhất:**
> **`INSERT INTO ... SELECT` ghép cột theo VỊ TRÍ, không theo TÊN.**

### 11.1. Khác gì `INSERT INTO ... VALUES`?

| | `INSERT ... VALUES` | `INSERT ... SELECT` |
|---|---|---|
| Nguồn dữ liệu | Giá trị **gõ tay** | Kết quả của một câu `SELECT` (từ bảng khác, hoặc cùng bảng) |
| Số dòng thêm | Số bộ giá trị anh viết | **Số dòng mà SELECT trả về** (0, 1, hay hàng nghìn) |
| Dùng khi | Nhập vài dòng cụ thể | Sao chép, lưu trữ (archive), lưu báo cáo thống kê |
| Có `VALUES`? | Có | **Không có** từ `VALUES`, không có ngoặc bọc SELECT |

**Cú pháp:**
```sql
INSERT INTO bang_dich (cot_dich_1, cot_dich_2, ...)
SELECT bieu_thuc_1, bieu_thuc_2, ...
FROM ...
[WHERE / JOIN / GROUP BY / HAVING ...];
```
**Quy tắc ghép cột:** cột thứ 1 của `SELECT` → `cot_dich_1`; cột thứ 2 → `cot_dich_2`... Cần **bằng số lượng** và **tương thích kiểu**. Tên cột (hay bí danh) trong SELECT **không có ý nghĩa** gì với việc ghép.

### 11.2. Chuẩn bị bảng đích

```sql
CREATE TABLE ORDER_ARCHIVE LIKE SALEORDER;   -- sao chép cấu trúc cột & chỉ mục (không có khóa ngoại, không có dữ liệu)
```

### 11.3. Sao chép toàn bộ dữ liệu

```sql
INSERT INTO ORDER_ARCHIVE
SELECT * FROM SALEORDER;
```
Kết quả: `ORDER_ARCHIVE` có **12 dòng** giống hệt `SALEORDER`. `SELECT *` chỉ dùng được khi hai bảng **cùng số cột, cùng thứ tự, cùng kiểu**. Trong công việc thật nên **liệt kê cột rõ ràng** (mục 11.7).

### 11.4. Chỉ sao chép các dòng thỏa WHERE

```sql
TRUNCATE TABLE ORDER_ARCHIVE;
INSERT INTO ORDER_ARCHIVE
SELECT * FROM SALEORDER WHERE OrderDate < '2025-04-01';
```
→ 5 dòng: đơn 1, 2, 3, 4, 5.

### 11.5. Kết hợp JOIN

```sql
CREATE TABLE ORDER_REPORT (
    OrderID     INT PRIMARY KEY,
    CustName    VARCHAR(100),
    EmpName     VARCHAR(100),
    TotalAmount DECIMAL(12,2)
);

INSERT INTO ORDER_REPORT (OrderID, CustName, EmpName, TotalAmount)
SELECT o.OrderID, c.CustName, e.EmpName, o.TotalAmount
FROM SALEORDER o
JOIN CUSTOMER c ON c.CustID = o.CustID
JOIN EMPLOYEE e ON e.EmpID  = o.EmpID
WHERE o.Status = 'COMPLETED';
```
→ 9 dòng, ví dụ:

| OrderID | CustName | EmpName | TotalAmount |
|---|---|---|---|
| 1 | Nguyen Van An | Nguyen Thu Ha | 15600.00 |
| 2 | Nguyen Van An | Nguyen Thu Ha | 9200.00 |
| 3 | Tran Thi Binh | Tran Quoc Huy | 18800.00 |
| ... | ... | ... | ... |

Bảng đích **không cần giống** bảng nguồn; chỉ cần số cột và kiểu khớp **theo vị trí**.

### 11.6. Kết hợp GROUP BY, SUM và HAVING

```sql
CREATE TABLE CUSTOMER_SUMMARY (
    CustID   INT PRIMARY KEY,
    SoDon    INT,
    TongTien DECIMAL(12,2)
);

INSERT INTO CUSTOMER_SUMMARY (CustID, SoDon, TongTien)
SELECT CustID, COUNT(*), SUM(TotalAmount)
FROM SALEORDER
WHERE Status = 'COMPLETED'
GROUP BY CustID;
```
| CustID | SoDon | TongTien |
|---|---|---|
| 1 | 3 | 26500.00 |
| 2 | 2 | 42800.00 |
| 3 | 1 | 30300.00 |
| 4 | 2 | 17500.00 |
| 5 | 1 | 19000.00 |

**Với HAVING: chỉ lưu khách chi tiêu trên 30000:**
```sql
CREATE TABLE CUSTOMER_VIP (CustID INT PRIMARY KEY, TongChiTieu DECIMAL(12,2));

INSERT INTO CUSTOMER_VIP (CustID, TongChiTieu)
SELECT CustID, SUM(TotalAmount)
FROM SALEORDER
WHERE Status = 'COMPLETED'
GROUP BY CustID
HAVING SUM(TotalAmount) > 30000;
```
| CustID | TongChiTieu |
|---|---|
| 2 | 42800.00 |
| 3 | 30300.00 |

Khi viết, **tách làm hai bước**: (1) viết và chạy riêng câu `SELECT` đến khi kết quả đúng; (2) thêm `INSERT INTO ... (cột)` ở phía trên.

### 11.7. Chỉ định rõ các cột đích

Luôn viết `INSERT INTO bang (cot1, cot2, ...)` để:
- Cột không liệt kê sẽ lấy `DEFAULT` hoặc `NULL`, hoặc `AUTO_INCREMENT` tự tăng.
- Code không vỡ khi sau này bảng đích **thêm cột**.

```sql
-- CustID tự tăng, Email để NULL, JoinDate lấy ngày hôm nay
INSERT INTO CUSTOMER (CustName, City, Phone, JoinDate)
SELECT CONCAT(EmpName, ' (KH)'), 'Ha Noi', CONCAT('09090000', EmpID), CURDATE()
FROM EMPLOYEE
WHERE Position = 'Sales' AND EmpID <= 3;
```
Thêm 2 khách mới (từ nhân viên 2 và 3); `CustID` tự cấp.

### 11.8. Khi số lượng hoặc kiểu cột không khớp

**Lỗi 1: thiếu/thừa cột**
```sql
INSERT INTO CUSTOMER_SUMMARY (CustID, SoDon, TongTien)
SELECT CustID, COUNT(*) FROM SALEORDER GROUP BY CustID;
-- ERROR 1136: Column count doesn't match value count at row 1
```
Sửa: SELECT phải trả đủ 3 cột.

**Lỗi 2: sai kiểu**
```sql
INSERT INTO CUSTOMER_SUMMARY (CustID, SoDon, TongTien)
SELECT CustName, COUNT(*), 0 FROM CUSTOMER GROUP BY CustName;
-- ERROR 1366: Incorrect integer value: 'Nguyen Van An' for column 'CustID'
```
Sửa: đặt đúng cột `CustID` ở vị trí 1.

**Lỗi 3 (nguy hiểm nhất, KHÔNG báo lỗi): đảo thứ tự cột, cùng kiểu**
```sql
INSERT INTO CUSTOMER_SUMMARY (CustID, SoDon, TongTien)
SELECT CustID, SUM(TotalAmount), COUNT(*)      -- ❌ đảo: SUM vào SoDon, COUNT vào TongTien
FROM SALEORDER WHERE Status = 'COMPLETED' GROUP BY CustID;
```
Dòng của khách 1 được lưu `SoDon = 26500, TongTien = 3`. MySQL **không phàn nàn** vì cùng là số. Nguyên nhân: ghép theo **vị trí**, bí danh không giúp được. Sửa: kiểm tra thứ tự các biểu thức `SELECT` khớp với thứ tự **cột đích** trong ngoặc.

**Lỗi 4: trùng khóa chính khi chạy lại**
```sql
-- Chạy lần 2 câu INSERT ở 11.6 → ERROR 1062: Duplicate entry '1' for key 'PRIMARY'
```
Cách xử lý:
```sql
INSERT INTO CUSTOMER_SUMMARY (CustID, SoDon, TongTien)
SELECT CustID, COUNT(*), SUM(TotalAmount) FROM SALEORDER
WHERE Status = 'COMPLETED' GROUP BY CustID
ON DUPLICATE KEY UPDATE SoDon = VALUES(SoDon), TongTien = VALUES(TongTien);   -- cập nhật nếu đã có
-- hoặc xóa sạch rồi chèn lại: TRUNCATE TABLE CUSTOMER_SUMMARY;
```

### 11.9. CREATE TABLE ... AS SELECT (tạo và điền cùng lúc)

```sql
CREATE TABLE TOP_PRODUCT AS
SELECT p.ProdID, p.ProdName, SUM(od.Quantity) AS DaBan
FROM PRODUCT p JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID
GROUP BY p.ProdID, p.ProdName;
```
Tạo bảng mới có cột lấy từ SELECT. **Không** sao chép khóa chính, khóa ngoại, `AUTO_INCREMENT`. Dùng cho bảng tạm / báo cáo; bảng chính thức nên `CREATE TABLE` rồi `INSERT ... SELECT` để kiểm soát cấu trúc.

### 11.10. Bài tập tự luyện Chương 11

1. Tạo bảng `HIGH_VALUE_ORDER(OrderID, CustID, TotalAmount)` và chèn các đơn COMPLETED có tổng từ 15000 trở lên.
2. Tạo bảng `PRODUCT_SALES(ProdID, TongSoLuong, DoanhThu)` chỉ gồm sản phẩm có doanh thu (từ chi tiết, mọi đơn) trên 10000.
3. Tìm lỗi: `INSERT INTO PRODUCT_SALES (ProdID, TongSoLuong, DoanhThu) SELECT ProdID, SUM(Quantity * UnitPrice), SUM(Quantity) FROM ORDER_DETAIL GROUP BY ProdID;`

<details><summary>Đáp án</summary>

```sql
-- 1  → đơn 1 (15600), 3 (18800), 5 (30300), 9 (19000), 12 (24000)
CREATE TABLE HIGH_VALUE_ORDER (OrderID INT PRIMARY KEY, CustID INT, TotalAmount DECIMAL(12,2));
INSERT INTO HIGH_VALUE_ORDER (OrderID, CustID, TotalAmount)
SELECT OrderID, CustID, TotalAmount FROM SALEORDER
WHERE Status = 'COMPLETED' AND TotalAmount >= 15000;

-- 2  → Laptop (6 × 15000 = 90000, SL 6), Smartphone (5 × 9000 = 45000, SL 5), Monitor (4 × 4000 = 16000, SL 4)
CREATE TABLE PRODUCT_SALES (ProdID INT PRIMARY KEY, TongSoLuong INT, DoanhThu DECIMAL(14,2));
INSERT INTO PRODUCT_SALES (ProdID, TongSoLuong, DoanhThu)
SELECT ProdID, SUM(Quantity), SUM(Quantity * UnitPrice)
FROM ORDER_DETAIL GROUP BY ProdID
HAVING SUM(Quantity * UnitPrice) > 10000;

-- 3  Lỗi: đảo thứ tự. SUM(Quantity*UnitPrice) (tiền) đang vào TongSoLuong, SUM(Quantity) (số lượng) vào DoanhThu.
--    Không báo lỗi nhưng dữ liệu sai. Sửa: đổi chỗ hai biểu thức.
```
Kiểm tra câu 2: Laptop: 1+1+2+1+1 = 6 chiếc, đơn giá 15000 → 90000. Smartphone 2+1+1+1 = 5 → 45000. Monitor 2+1+1 = 4 → 16000. Keyboard: 3 × 1200 = 3600 (loại). Mouse 8 × 300 = 2400 (loại).
</details>

---

### 11.11. Bài tập tự luyện bổ sung Chương 11 (có đáp án)

1. Chèn vào `ORDER_ARCHIVE` (tạo ở mục 11.2) các đơn đặt trước 2025-03-01 (chỉ các cột `OrderID, CustID, EmpID, OrderDate, Status, TotalAmount`, chỉ định cột rõ ràng).
2. Tạo bảng `CITY_SUMMARY(City, SoKhach, DoanhThu)` với doanh thu COMPLETED của các khách theo thành phố (thành phố nào cũng có dòng, kể cả chưa có doanh thu).
3. Tạo `ORDER_CLASS(OrderID, Loai)` gán `LON` (≥ 20000), `VUA` (≥ 10000), `NHO` cho mọi đơn.

<details><summary>Đáp án</summary>

```sql
-- 1  → 3 dòng: đơn 1, 2, 3
TRUNCATE TABLE ORDER_ARCHIVE;
INSERT INTO ORDER_ARCHIVE (OrderID, CustID, EmpID, OrderDate, Status, TotalAmount)
SELECT OrderID, CustID, EmpID, OrderDate, Status, TotalAmount
FROM SALEORDER WHERE OrderDate < '2025-03-01';

-- 2  → Ha Noi 2 / 44000; Ho Chi Minh 2 / 61800; Da Nang 1 / 30300; Hai Phong 1 / 0
CREATE TABLE CITY_SUMMARY (City VARCHAR(50) PRIMARY KEY, SoKhach INT, DoanhThu DECIMAL(14,2));
INSERT INTO CITY_SUMMARY (City, SoKhach, DoanhThu)
SELECT c.City, COUNT(DISTINCT c.CustID),
       COALESCE(SUM(CASE WHEN o.Status = 'COMPLETED' THEN o.TotalAmount END), 0)
FROM CUSTOMER c LEFT JOIN SALEORDER o ON o.CustID = c.CustID
GROUP BY c.City;

-- 3  → LON: đơn 5, 12; VUA: đơn 1, 3, 4, 7, 9; NHO: đơn 2, 6, 8, 10, 11
CREATE TABLE ORDER_CLASS (OrderID INT PRIMARY KEY, Loai VARCHAR(10));
INSERT INTO ORDER_CLASS (OrderID, Loai)
SELECT OrderID,
       CASE WHEN TotalAmount >= 20000 THEN 'LON'
            WHEN TotalAmount >= 10000 THEN 'VUA'
            ELSE 'NHO' END
FROM SALEORDER;
```
Ở câu 2, dùng `COUNT(DISTINCT c.CustID)` vì `LEFT JOIN` làm khách có nhiều đơn lặp nhiều dòng.
</details>

---

## CHƯƠNG 12: THỨ TỰ THỰC THI VÀ CÁCH SUY LUẬN KHI LÀM BÀI

### 12.1. Quy trình 10 câu hỏi

Với **mọi** đề bài, đừng viết code ngay. Hãy trả lời lần lượt:

| # | Câu hỏi | Gợi ý nhận biết trong đề |
|---|---|---|
| 1 | Đề yêu cầu **xem, thêm, sửa hay xóa** dữ liệu? | "liệt kê, tìm, cho biết" → `SELECT`; "thêm, lưu, sao chép" → `INSERT`; "tăng, đổi, cập nhật" → `UPDATE`; "xóa, loại bỏ" → `DELETE` |
| 2 | Thông tin cần nằm ở **bảng nào**? | Gạch chân các danh từ, đối chiếu với cột của từng bảng |
| 3 | Có cần **kết hợp nhiều bảng** (JOIN)? | Thông tin nằm ở ≥ 2 bảng, và cần hiển thị chúng |
| 4 | Có cần **lọc từng dòng** (`WHERE`)? | "chỉ các đơn COMPLETED", "trong tháng 5", "ở Hà Nội" |
| 5 | Có cần **tính tổng / đếm / trung bình**? | "tổng", "số lượng", "bao nhiêu", "trung bình" |
| 6 | Có cần **`GROUP BY`**? | "của **mỗi**...", "**từng**...", "theo..." |
| 7 | Có **điều kiện trên kết quả tổng hợp** (`HAVING`)? | "tổng **trên** 50000", "**ít nhất** 3 đơn" |
| 8 | Có cần **truy vấn con**? | "cao hơn **mức trung bình**", "cao nhất", "chưa từng", hoặc UPDATE/DELETE phụ thuộc kết quả thống kê |
| 9 | Có cần `INSERT INTO`, `UPDATE`, `DELETE` **bọc bên ngoài**? | Đề là "lưu/ cập nhật/ xóa" dựa trên một tập dữ liệu tìm được |
| 10 | Câu lệnh cuối cùng viết ra sao? | **Xây từng lớp** từ trong ra ngoài, chạy thử từng lớp |

### 12.2. Bản đồ từ khóa trong đề → mệnh đề SQL

| Từ khóa trong đề | Mệnh đề |
|---|---|
| "mỗi", "từng", "theo" | `GROUP BY` |
| "tổng", "tổng cộng" | `SUM` |
| "số lượng", "bao nhiêu", "đếm" | `COUNT` |
| "trung bình" | `AVG` |
| "cao nhất", "lớn nhất", "nhiều nhất" | `MAX` / `ORDER BY ... DESC LIMIT` / subquery |
| "trên / vượt / ít nhất ... (của tổng, của số đếm)" | `HAVING` |
| "đã COMPLETED", "ở Hà Nội", "trong tháng..." | `WHERE` |
| "chưa từng", "không có" | `LEFT JOIN ... IS NULL` / `NOT IN` / `NOT EXISTS` |
| "có ít nhất một", "tồn tại" | `EXISTS` / `IN` |
| "phân loại", "xếp hạng thành", "nếu... thì..." | `CASE WHEN` |
| "cao hơn mức trung bình" | Subquery với `AVG` |
| "top N", "N đầu tiên" | `ORDER BY ... LIMIT N` / `ROW_NUMBER` |
| "lưu vào bảng", "sao chép sang" | `INSERT INTO ... SELECT` |

### 12.3. Ví dụ 1 (SELECT): khách có tổng chi tiêu COMPLETED trên 30000

> **Đề:** "Liệt kê tên khách hàng và tổng chi tiêu của những khách có tổng chi tiêu từ các đơn COMPLETED vượt 30000."

**Phân tích theo 10 câu hỏi:**
1. Xem dữ liệu → `SELECT`.
2. Tên khách ở `CUSTOMER`; tiền và trạng thái ở `SALEORDER`.
3. Cần 2 bảng → `JOIN` (nối bằng `CustID`).
4. "COMPLETED" là điều kiện từng dòng → `WHERE Status = 'COMPLETED'`.
5. "tổng chi tiêu" → `SUM(TotalAmount)`.
6. "của khách" (mỗi khách một dòng) → `GROUP BY CustID, CustName`.
7. "vượt 30000" là điều kiện trên tổng → `HAVING SUM(TotalAmount) > 30000`.
8. Không cần subquery.
9. Không cần INSERT/UPDATE/DELETE.
10. Ghép:

**Xây từng bước:**
```sql
-- (1) Bắt đầu với JOIN
SELECT c.CustName, o.OrderID, o.TotalAmount
FROM CUSTOMER c JOIN SALEORDER o ON o.CustID = c.CustID;

-- (2) Thêm WHERE
... WHERE o.Status = 'COMPLETED';

-- (3) Gom nhóm và tính tổng
SELECT c.CustName, SUM(o.TotalAmount) AS Tong
FROM CUSTOMER c JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.Status = 'COMPLETED'
GROUP BY c.CustID, c.CustName;

-- (4) Thêm HAVING → câu hoàn chỉnh
SELECT c.CustName, SUM(o.TotalAmount) AS Tong
FROM CUSTOMER c JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.Status = 'COMPLETED'
GROUP BY c.CustID, c.CustName
HAVING SUM(o.TotalAmount) > 30000;
```
**Kết quả:** `Tran Thi Binh | 42800.00` và `Le Van Cuong | 30300.00`.

### 12.4. Ví dụ 2 (UPDATE + subquery): tăng lương theo doanh thu

> **Đề:** "Tăng lương 10% cho nhân viên có tổng doanh thu từ các đơn COMPLETED vượt 50000."

1. Sửa dữ liệu → `UPDATE EMPLOYEE`.
2. Lương ở `EMPLOYEE`, doanh thu ở `SALEORDER` → **hai bảng, nhưng không JOIN để hiển thị**; chỉ cần **danh sách mã nhân viên**.
3–7. "doanh thu vượt 50000 của mỗi nhân viên" → `WHERE Status='COMPLETED' GROUP BY EmpID HAVING SUM(TotalAmount) > 50000` (tính trên `SALEORDER`).
8. Cần subquery: kết quả thống kê quyết định ai bị `UPDATE`.
9. `UPDATE` bọc ngoài, điều kiện `EmpID IN (subquery)`.
10. Viết **subquery trước**, chạy ra `{2}`; rồi thêm `UPDATE ... WHERE EmpID IN (...)`. Chi tiết: **mục 8.11**.

### 12.5. Ví dụ 3 (INSERT ... SELECT): lưu doanh thu nhân viên

> **Đề:** "Tạo bảng `EMP_REVENUE(EmpID, DoanhThu)` và lưu doanh thu COMPLETED của những nhân viên đạt từ 20000 trở lên."

1. "tạo bảng và lưu" → `CREATE TABLE` rồi `INSERT`.
2. Dữ liệu ở `SALEORDER`.
3. Không cần JOIN.
4. `WHERE Status = 'COMPLETED'`.
5–6. "doanh thu của nhân viên" → `SUM`, `GROUP BY EmpID`.
7. "đạt từ 20000" → `HAVING SUM(TotalAmount) >= 20000`.
8. Không cần subquery.
9. `INSERT INTO EMP_REVENUE (EmpID, DoanhThu) SELECT ...`.
```sql
CREATE TABLE EMP_REVENUE (EmpID INT PRIMARY KEY, DoanhThu DECIMAL(12,2));

INSERT INTO EMP_REVENUE (EmpID, DoanhThu)
SELECT EmpID, SUM(TotalAmount)
FROM SALEORDER
WHERE Status = 'COMPLETED'
GROUP BY EmpID
HAVING SUM(TotalAmount) >= 20000;
```
**Kết quả:** `2 | 98100.00` và `3 | 31800.00` (NV 4 chỉ 6200 → loại).

### 12.6. Ví dụ 4 (DELETE nhiều bảng): xóa đơn PENDING

> **Đề:** "Xóa toàn bộ đơn hàng PENDING (kể cả chi tiết)."

1. Xóa → `DELETE`.
2. Đơn ở `SALEORDER`, chi tiết ở `ORDER_DETAIL` (khóa ngoại tham chiếu `SALEORDER`).
3. Cần xác định chi tiết của đơn nào → subquery/JOIN.
4. `Status = 'PENDING'`.
5–7. Không tổng hợp.
8. Subquery chọn `OrderID` của đơn PENDING.
9. **Hai lệnh DELETE theo thứ tự: con (`ORDER_DETAIL`) trước, cha (`SALEORDER`) sau.**
```sql
DELETE FROM ORDER_DETAIL
WHERE OrderID IN (SELECT OrderID FROM SALEORDER WHERE Status = 'PENDING');

DELETE FROM SALEORDER WHERE Status = 'PENDING';
```
Đảo thứ tự → lỗi 1451 vì khóa ngoại.

### 12.7. Mẹo debug: xây từ trong ra ngoài

1. Viết và **chạy riêng** phần tìm dữ liệu (SELECT lõi).
2. Kiểm tra bằng **nhẩm** hoặc đối chiếu tổng (ví dụ cộng các nhóm = tổng bảng).
3. Thêm từng lớp: `JOIN` → `WHERE` → `GROUP BY` → `HAVING` → `ORDER BY`.
4. Chỉ **sau cùng** mới bọc `INSERT`/`UPDATE`/`DELETE`, và với UPDATE/DELETE luôn thử trong transaction.

---

## CHƯƠNG 13: CÁC DẠNG BÀI SQL THƯỜNG GẶP

> Dữ liệu mẫu là `shop_db` ở đầu tài liệu (giả định đã chạy lại script gốc trước mỗi nhóm bài, đặc biệt các nhóm UPDATE/DELETE). Mỗi dạng có 3–4 bài từ dễ đến khó; mỗi bài có đáp án, kết quả, lý do suy luận. **Hãy tự làm trước khi xem.** Sau các bài của mỗi dạng có phần *Giải thích chi tiết và cách giải khác* (suy luận, từng dòng, cách khác, lỗi).

### Nhắc lại cấu trúc dữ liệu mẫu (để làm bài không phải cuộn lên)

| Bảng | Cột | Số dòng | Ghi chú dữ liệu |
|---|---|---|---|
| `CUSTOMER` | CustID, CustName, City, Phone, Email, JoinDate | 6 | Khách 3, 5 không có email; khách 6 chưa mua |
| `EMPLOYEE` | EmpID, EmpName, Position, Salary, HireDate, ManagerID | 5 | NV 1 là quản lý (không có `ManagerID`); NV 1 và 5 chưa lập đơn |
| `PRODUCT` | ProdID, ProdName, Category, Price, Stock | 8 | 3 Electronics, 5 Accessories; Webcam (8) chưa bán |
| `SALEORDER` | OrderID, CustID, EmpID, OrderDate, Status, TotalAmount | 12 | 9 COMPLETED, 2 PENDING (đơn 6, 10), 1 CANCELLED (đơn 4) |
| `ORDER_DETAIL` | OrderID, ProdID, Quantity, UnitPrice (khóa chính 2 cột) | 23 | Tổng số lượng 36; `TotalAmount` = tổng `Quantity × UnitPrice` của đơn |

Số liệu chốt cần nhớ: tổng mọi đơn 161700; tổng COMPLETED 136100 (NV 2: 98100, NV 3: 31800, NV 4: 6200); tổng theo khách (mọi đơn): 26500, 57800, 31900, 17500, 28000. Dữ liệu bị đổi bởi các bài `UPDATE`/`DELETE` thì chạy lại script ở Phụ lục D.


### DẠNG 1: LỌC DỮ LIỆU

**Bài 1.1 (dễ)** Liệt kê khách hàng ở Ha Noi hoặc Da Nang.
```sql
SELECT CustID, CustName, City FROM CUSTOMER WHERE City IN ('Ha Noi', 'Da Nang');
```
→ An (Ha Noi), Cuong (Da Nang), Dung (Ha Noi). *Suy luận:* hai giá trị cùng cột → `IN` gọn hơn `OR`.

**Bài 1.2 (dễ)** Phụ kiện (Accessories) có tồn kho từ 50 trở lên.
```sql
SELECT ProdName, Stock FROM PRODUCT WHERE Category = 'Accessories' AND Stock >= 50;
```
→ Mouse Logitech (100), Keyboard Mechanical (50), USB 64GB (200).

**Bài 1.3 (vừa)** Đơn COMPLETED đặt từ tháng 2 đến tháng 5/2025 có tổng từ 5000 đến 20000.
```sql
SELECT OrderID, OrderDate, TotalAmount
FROM SALEORDER
WHERE Status = 'COMPLETED'
  AND OrderDate >= '2025-02-01' AND OrderDate < '2025-06-01'
  AND TotalAmount BETWEEN 5000 AND 20000;
```
→ đơn 2 (9200), 3 (18800), 7 (13000), 9 (19000). Loại: đơn 5 (30300 > 20000), đơn 8 (4500 < 5000).

**Bài 1.4 (khó)** Khách có email, mà tên chứa "Thi" **hoặc** ở Ho Chi Minh.
```sql
SELECT CustName, City, Email FROM CUSTOMER
WHERE Email IS NOT NULL AND (CustName LIKE '%Thi%' OR City = 'Ho Chi Minh');
```
→ Binh, Dung, Phuong. *Lỗi hay gặp:* quên ngoặc quanh `OR` → khách Em (HCM, không email) lọt vào hoặc lọc sai.

#### Giải thích chi tiết và cách giải khác (Dạng 1): Lọc dữ liệu

**Bài 1.1**
- *Suy luận:* "Ha Noi **hoặc** Da Nang": hai giá trị của **cùng một cột** → `IN`.
- *Từng dòng:* `SELECT CustID, CustName, City` lấy cột cần; `FROM CUSTOMER` bảng khách; `WHERE City IN (...)` giữ dòng có `City` nằm trong danh sách.
- *Cách khác:* `WHERE City = 'Ha Noi' OR City = 'Da Nang'` (dài hơn khi nhiều giá trị).
- *Lỗi:* `City = 'Ha Noi' OR 'Da Nang'` ❌ (vế sau là một chuỗi, không phải phép so sánh) → viết đủ `City = ...` ở mỗi vế hoặc dùng `IN`.

**Bài 1.2**
- *Suy luận:* hai điều kiện **đồng thời** (nhóm hàng *và* tồn kho) → `AND`. "từ 50 trở lên" → `>=`, không phải `>`.
- *Từng dòng:* `Category = 'Accessories'` lọc nhóm; `Stock >= 50` lọc tồn kho.
- *Cách khác:* `WHERE Stock BETWEEN 50 AND 1000000` (không tự nhiên bằng `>=`).
- *Lỗi:* dùng `Stock > 50` làm mất Keyboard (tồn đúng 50).

**Bài 1.3**
- *Suy luận:* 3 điều kiện: trạng thái, khoảng ngày, khoảng tiền → `AND` nối ba điều kiện; ngày dùng khoảng nửa mở `>= '2025-02-01' AND < '2025-06-01'`; tiền dùng `BETWEEN` (gồm hai đầu).
- *Từng dòng:* dòng 1: trạng thái; dòng 2: tháng 2 → hết tháng 5; dòng 3: 5000 ≤ tiền ≤ 20000.
- *Cách khác:* `OrderDate BETWEEN '2025-02-01' AND '2025-05-31'` (đúng với cột `DATE`, **sai** với `DATETIME`); hoặc `MONTH(OrderDate) BETWEEN 2 AND 5` (không dùng được chỉ mục).
- *Lỗi:* quên `Status = 'COMPLETED'` → thêm đơn 4 (CANCELLED, 15000), đơn 6 (PENDING, tháng 4 nhưng 1600 nên vẫn loại bởi tiền); quên dấu bằng của biên `5000`/`20000`.

**Bài 1.4**
- *Suy luận:* "có email" luôn bắt buộc; "tên chứa Thi **hoặc** ở HCM" là một cụm → **phải đặt trong ngoặc** rồi `AND` với điều kiện email.
- *Từng dòng:* `Email IS NOT NULL` lọc NULL; `(... OR ...)` cụm điều kiện.
- *Cách khác:* hai `SELECT` có `Email IS NOT NULL` rồi `UNION`.
- *Lỗi:* không ngoặc → `A AND B OR C` chạy như `(A AND B) OR C` → khách Em (không email, ở HCM) lọt vào.

### DẠNG 2: SẮP XẾP VÀ LOẠI BỎ TRÙNG LẶP

**Bài 2.1 (dễ)** Các trạng thái đơn hàng khác nhau, sắp A–Z.
```sql
SELECT DISTINCT Status FROM SALEORDER ORDER BY Status;
```
→ CANCELLED, COMPLETED, PENDING.

**Bài 2.2 (vừa)** 5 sản phẩm đắt nhất; cùng giá thì xếp theo tên.
```sql
SELECT ProdName, Price FROM PRODUCT ORDER BY Price DESC, ProdName LIMIT 5;
```
→ Laptop 15000, Smartphone 9000, Monitor 4000, Keyboard 1200, Headphone 800.

**Bài 2.3 (vừa)** Các cặp (khách, nhân viên) khác nhau từng giao dịch.
```sql
SELECT DISTINCT CustID, EmpID FROM SALEORDER ORDER BY CustID, EmpID;
```
→ 10 cặp trên 12 đơn: (1,2), (1,4), (2,2), (2,3), (3,2), (3,4), (4,3), (4,4), (5,2), (5,3). *Suy luận:* `DISTINCT` áp dụng cho **tổ hợp** cột.

#### Giải thích chi tiết và cách giải khác (Dạng 2): Sắp xếp và loại trùng

**Bài 2.1**
- *Suy luận:* "khác nhau" → `DISTINCT`; "sắp A–Z" → `ORDER BY` (mặc định tăng dần).
- *Từng dòng:* `SELECT DISTINCT Status` loại trùng; `ORDER BY Status` sắp theo bảng chữ cái.
- *Cách khác:* `SELECT Status FROM SALEORDER GROUP BY Status ORDER BY Status;`.
- *Lỗi:* `SELECT Status DISTINCT` (sai vị trí); `DISTINCT` không đi sau tên cột.

**Bài 2.2**
- *Suy luận:* "5 đắt nhất" → sắp giảm theo giá rồi cắt 5; "cùng giá thì theo tên" → cột sắp xếp thứ hai.
- *Từng dòng:* `ORDER BY Price DESC, ProdName` (cột thứ hai chỉ phát huy khi trùng giá); `LIMIT 5`.
- *Cách khác:* `ROW_NUMBER() OVER (ORDER BY Price DESC, ProdName)` trong CTE rồi `WHERE rn <= 5`.
- *Lỗi:* `LIMIT` không có `ORDER BY` → 5 dòng bất kỳ; quên `DESC` → 5 sản phẩm **rẻ** nhất.

**Bài 2.3**
- *Suy luận:* "cặp khác nhau" → `DISTINCT` áp dụng cho **cả hai cột cùng lúc**.
- *Từng dòng:* `SELECT DISTINCT CustID, EmpID`; `ORDER BY CustID, EmpID` cho dễ đọc.
- *Cách khác:* `SELECT CustID, EmpID FROM SALEORDER GROUP BY CustID, EmpID;`.
- *Lỗi:* `SELECT DISTINCT CustID, DISTINCT EmpID` ❌; `DISTINCT CustID` chỉ loại trùng theo `CustID` (5 dòng).

### DẠNG 3: JOIN HAI BẢNG

**Bài 3.1 (dễ)** Các đơn COMPLETED của khách ở Ha Noi, kèm tên khách.
```sql
SELECT o.OrderID, c.CustName, o.TotalAmount
FROM SALEORDER o JOIN CUSTOMER c ON c.CustID = o.CustID
WHERE c.City = 'Ha Noi' AND o.Status = 'COMPLETED'
ORDER BY o.OrderID;
```
→ đơn 1, 2, 11 (An); 7, 8 (Dung).

**Bài 3.2 (vừa)** Mọi nhân viên và số đơn họ lập (0 nếu chưa có).
```sql
SELECT e.EmpName, COUNT(o.OrderID) AS SoDon
FROM EMPLOYEE e LEFT JOIN SALEORDER o ON o.EmpID = e.EmpID
GROUP BY e.EmpID, e.EmpName;
```
→ Quan 0, Ha 5, Huy 4, Lan 3, Minh 0. *Cách khác:* subquery trong SELECT (mục 8.6).

**Bài 3.3 (vừa)** Chi tiết đơn 8 kèm tên sản phẩm.
```sql
SELECT p.ProdName, od.Quantity, od.UnitPrice
FROM ORDER_DETAIL od JOIN PRODUCT p ON p.ProdID = od.ProdID
WHERE od.OrderID = 8;
```
→ Keyboard Mechanical (2, 1200), Headphone (2, 800), USB 64GB (2, 250).

#### Giải thích chi tiết và cách giải khác (Dạng 3): JOIN hai bảng

**Bài 3.1**
- *Suy luận:* thành phố ở `CUSTOMER`, trạng thái ở `SALEORDER` → JOIN; mỗi bảng một điều kiện lọc.
- *Từng dòng:* `JOIN ... ON c.CustID = o.CustID` nối bằng khóa; `WHERE c.City = 'Ha Noi' AND o.Status = 'COMPLETED'`.
- *Cách khác:* không JOIN nếu chỉ cần ID đơn: `WHERE CustID IN (SELECT CustID FROM CUSTOMER WHERE City='Ha Noi') AND Status='COMPLETED'` (nhưng đề cần tên khách nên giữ JOIN).
- *Lỗi:* quên tiền tố bí danh ở cột trùng tên (1052).

**Bài 3.2**
- *Suy luận:* "mọi nhân viên, 0 nếu chưa có" → `LEFT JOIN` từ `EMPLOYEE`; đếm đơn → `COUNT(o.OrderID)`.
- *Từng dòng:* `LEFT JOIN` giữ nhân viên không có đơn; `COUNT(o.OrderID)` bỏ NULL → 0; `GROUP BY e.EmpID, e.EmpName`.
- *Cách khác:* `SELECT e.EmpName, (SELECT COUNT(*) FROM SALEORDER o WHERE o.EmpID = e.EmpID) FROM EMPLOYEE e;`.
- *Lỗi:* `COUNT(*)` → ra 1 cho người chưa có đơn; `INNER JOIN` → mất hẳn Quan và Minh.

**Bài 3.3**
- *Suy luận:* chi tiết đơn nằm ở `ORDER_DETAIL`, tên sản phẩm ở `PRODUCT` → nối bằng `ProdID`; lọc `OrderID = 8`.
- *Từng dòng:* `JOIN PRODUCT p ON p.ProdID = od.ProdID`; `WHERE od.OrderID = 8`.
- *Cách khác:* `SELECT (SELECT ProdName FROM PRODUCT p WHERE p.ProdID = od.ProdID) ...` (kém gọn).
- *Lỗi:* nối `p.ProdID = od.OrderID` (nhầm cột).

### DẠNG 4: JOIN BA BẢNG TRỞ LÊN

**Bài 4.1 (vừa)** Tên khách, sản phẩm và số lượng của đơn 9.
```sql
SELECT c.CustName, p.ProdName, od.Quantity
FROM SALEORDER o
JOIN CUSTOMER c      ON c.CustID = o.CustID
JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
JOIN PRODUCT p       ON p.ProdID = od.ProdID
WHERE o.OrderID = 9;
```
→ Hoang Van Em: Laptop Dell (1), Monitor 24 inch (1).

**Bài 4.2 (vừa)** Những nhân viên từng bán Laptop Dell trong đơn COMPLETED.
```sql
SELECT DISTINCT e.EmpName
FROM EMPLOYEE e
JOIN SALEORDER o     ON o.EmpID = e.EmpID
JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
JOIN PRODUCT p       ON p.ProdID = od.ProdID
WHERE p.ProdName = 'Laptop Dell' AND o.Status = 'COMPLETED';
```
→ Nguyen Thu Ha (đơn 1, 5, 9, 12). Đơn 4 (NV 3) bán Laptop nhưng đã CANCELLED → loại.

**Bài 4.3 (khó)** Doanh thu của mỗi nhân viên theo nhóm hàng (đơn COMPLETED).
```sql
SELECT e.EmpName, p.Category, SUM(od.Quantity * od.UnitPrice) AS DoanhThu
FROM EMPLOYEE e
JOIN SALEORDER o     ON o.EmpID = e.EmpID
JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
JOIN PRODUCT p       ON p.ProdID = od.ProdID
WHERE o.Status = 'COMPLETED'
GROUP BY e.EmpID, e.EmpName, p.Category
ORDER BY e.EmpID, p.Category;
```
| EmpName | Category | DoanhThu |
|---|---|---|
| Nguyen Thu Ha | Accessories | 2100.00 |
| Nguyen Thu Ha | Electronics | 96000.00 |
| Tran Quoc Huy | Accessories | 800.00 |
| Tran Quoc Huy | Electronics | 31000.00 |
| Le Thi Lan | Accessories | 6200.00 |

*Kiểm tra:* 2100 + 96000 = 98100 (NV 2); 800 + 31000 = 31800 (NV 3); 6200 (NV 4). *Suy luận:* `SUM` lấy từ bảng chi tiết (`Quantity × UnitPrice`) để tránh nhân dòng (xem 6.10).

#### Giải thích chi tiết và cách giải khác (Dạng 4): JOIN ba bảng trở lên

**Bài 4.1**
- *Suy luận:* khách ↔ đơn ↔ chi tiết ↔ sản phẩm: **không** nối trực tiếp khách với sản phẩm được, phải đi qua `SALEORDER` và `ORDER_DETAIL`.
- *Từng dòng:* mỗi `JOIN` thêm một bảng có khóa chung với bảng đã có; `WHERE o.OrderID = 9` ở cuối.
- *Cách khác:* xuất phát từ `ORDER_DETAIL` làm bảng trung tâm.
- *Lỗi:* bỏ `ORDER_DETAIL` → không có đường nối tới `PRODUCT`.

**Bài 4.2**
- *Suy luận:* "nhân viên đã bán Laptop" → đường: `EMPLOYEE – SALEORDER – ORDER_DETAIL – PRODUCT`; một nhân viên bán nhiều lần → trùng → `DISTINCT`.
- *Từng dòng:* `WHERE p.ProdName = 'Laptop Dell' AND o.Status = 'COMPLETED'`.
- *Cách khác:* `EXISTS`: `SELECT e.EmpName FROM EMPLOYEE e WHERE EXISTS (SELECT 1 FROM SALEORDER o JOIN ORDER_DETAIL od ON od.OrderID=o.OrderID WHERE o.EmpID=e.EmpID AND od.ProdID=1 AND o.Status='COMPLETED');` (không cần `DISTINCT`).
- *Lỗi:* bỏ `Status` → thêm Tran Quoc Huy (đơn 4 bị huỷ).

**Bài 4.3**
- *Suy luận:* "mỗi nhân viên **theo nhóm hàng**" → `GROUP BY` hai tiêu chí; doanh thu từ chi tiết.
- *Từng dòng:* `SUM(od.Quantity * od.UnitPrice)` tính thành tiền ở mức chi tiết; `GROUP BY e.EmpID, e.EmpName, p.Category`.
- *Cách khác:* CTE tính từng dòng chi tiết trước rồi gom.
- *Lỗi:* dùng `SUM(o.TotalAmount)` → bị nhân theo số dòng chi tiết; thiếu `p.Category` trong `GROUP BY` → lỗi 1055.

### DẠNG 5: ĐẾM VÀ TÍNH TỔNG

**Bài 5.1 (dễ)** Số khách theo từng thành phố.
```sql
SELECT City, COUNT(*) AS SoKhach FROM CUSTOMER GROUP BY City;
```
→ Ha Noi 2, Ho Chi Minh 2, Da Nang 1, Hai Phong 1.

**Bài 5.2 (vừa)** Giá trị tồn kho (`Stock × Price`) theo nhóm hàng.
```sql
SELECT Category, SUM(Stock * Price) AS GiaTriTon FROM PRODUCT GROUP BY Category;
```
→ Electronics 645000.00 (300000 + 120000 + 225000); Accessories 182500.00 (30000 + 60000 + 32000 + 50000 + 10500).

**Bài 5.3 (vừa)** Số dòng chi tiết, tổng số lượng bán ra và số đơn có chi tiết.
```sql
SELECT COUNT(*) AS SoDong, SUM(Quantity) AS TongSL, COUNT(DISTINCT OrderID) AS SoDon
FROM ORDER_DETAIL;
```
→ 23 | 36 | 12.

#### Giải thích chi tiết và cách giải khác (Dạng 5): Đếm và tính tổng

**Bài 5.1:** *Suy luận:* "theo từng thành phố" → `GROUP BY City`; "số khách" → `COUNT(*)`. *Từng dòng:* một dòng kết quả mỗi thành phố. *Cách khác:* `COUNT(CustID)`. *Lỗi:* thiếu `GROUP BY City`.

**Bài 5.2:** *Suy luận:* tồn kho × giá = giá trị từng dòng; `SUM` theo nhóm hàng. *Từng dòng:* `SUM(Stock * Price)` cộng giá trị từng sản phẩm. *Cách khác:* window `SUM(Stock*Price) OVER (PARTITION BY Category)` (giữ từng dòng). *Lỗi:* `SUM(Stock) * SUM(Price)` ❌ (tổng nhân tổng ≠ tổng của tích).

**Bài 5.3:** *Suy luận:* ba chỉ số trên cùng một bảng; không `GROUP BY` → cả bảng là một nhóm. *Từng dòng:* `COUNT(*)` số dòng chi tiết; `SUM(Quantity)` số lượng; `COUNT(DISTINCT OrderID)` số đơn. *Cách khác:* tính từng giá trị bằng 3 câu riêng. *Lỗi:* `COUNT(OrderID)` thay `COUNT(DISTINCT OrderID)` → 23 thay vì 12.

### DẠNG 6: GROUP BY VÀ HAVING

**Bài 6.1 (dễ)** Khách có tổng chi tiêu (mọi đơn) trên 25000.
```sql
SELECT CustID, SUM(TotalAmount) AS Tong
FROM SALEORDER GROUP BY CustID HAVING SUM(TotalAmount) > 25000;
```
→ 1 (26500), 2 (57800), 3 (31900), 5 (28000). Khách 4 (17500) bị loại.

**Bài 6.2 (vừa)** Sản phẩm xuất hiện trong ít nhất 3 đơn khác nhau.
```sql
SELECT p.ProdName, COUNT(DISTINCT od.OrderID) AS SoDon
FROM PRODUCT p JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID
GROUP BY p.ProdID, p.ProdName
HAVING COUNT(DISTINCT od.OrderID) >= 3;
```
→ Laptop 5, Mouse 4, Monitor 3, Smartphone 4, Headphone 3.

**Bài 6.3 (khó)** Các tháng có ít nhất 2 đơn COMPLETED.
```sql
SELECT DATE_FORMAT(OrderDate, '%Y-%m') AS Thang, COUNT(*) AS SoDon
FROM SALEORDER
WHERE Status = 'COMPLETED'
GROUP BY DATE_FORMAT(OrderDate, '%Y-%m')
HAVING COUNT(*) >= 2;
```
→ 2025-02 (2: đơn 2, 3), 2025-05 (2: đơn 8, 9).

#### Giải thích chi tiết và cách giải khác (Dạng 6): GROUP BY và HAVING

**Bài 6.1:** *Suy luận:* "tổng chi tiêu **trên** 25000" là điều kiện trên tổng → `HAVING`. *Từng dòng:* `GROUP BY CustID` rồi `HAVING SUM(TotalAmount) > 25000`. *Cách khác:* bảng dẫn xuất rồi `WHERE Tong > 25000`. *Lỗi:* `WHERE SUM(...) > 25000` (lỗi 1111).

**Bài 6.2:** *Suy luận:* "xuất hiện trong ≥ 3 đơn khác nhau" → đếm đơn khác nhau của mỗi sản phẩm. *Từng dòng:* `COUNT(DISTINCT od.OrderID)` (vì khóa chính `(OrderID, ProdID)` nên mỗi sản phẩm xuất hiện tối đa một dòng/đơn, `COUNT(*)` cho cùng số, nhưng `DISTINCT` thể hiện ý đồ rõ ràng). *Cách khác:* `COUNT(*)` ở đây tương đương. *Lỗi:* nhầm với `SUM(Quantity)` (số lượng, không phải số đơn).

**Bài 6.3:** *Suy luận:* gom theo tháng, chỉ COMPLETED, giữ tháng có ≥ 2 đơn. *Từng dòng:* `WHERE` lọc COMPLETED trước; `GROUP BY DATE_FORMAT(OrderDate,'%Y-%m')`; `HAVING COUNT(*) >= 2`. *Cách khác:* `GROUP BY YEAR(OrderDate), MONTH(OrderDate)`. *Lỗi:* gom theo `MONTH` đơn thuần khi dữ liệu có nhiều năm.

### DẠNG 7: CASE WHEN

**Bài 7.1 (dễ)** Gắn nhãn cho từng đơn: COMPLETED → "Xong", còn lại → "Chua xong".
```sql
SELECT OrderID, Status,
       CASE WHEN Status = 'COMPLETED' THEN 'Xong' ELSE 'Chua xong' END AS TinhTrang
FROM SALEORDER;
```

**Bài 7.2 (vừa)** Bảng chéo (pivot): doanh thu mỗi khách theo từng trạng thái.
```sql
SELECT CustID,
       SUM(CASE WHEN Status = 'COMPLETED' THEN TotalAmount ELSE 0 END) AS Xong,
       SUM(CASE WHEN Status = 'PENDING'   THEN TotalAmount ELSE 0 END) AS DangCho,
       SUM(CASE WHEN Status = 'CANCELLED' THEN TotalAmount ELSE 0 END) AS Huy
FROM SALEORDER
GROUP BY CustID;
```
| CustID | Xong | DangCho | Huy |
|---|---|---|---|
| 1 | 26500 | 0 | 0 |
| 2 | 42800 | 0 | 15000 |
| 3 | 30300 | 1600 | 0 |
| 4 | 17500 | 0 | 0 |
| 5 | 19000 | 9000 | 0 |

**Bài 7.3 (vừa)** Mỗi nhân viên có bao nhiêu đơn lớn (≥ 20000) và bao nhiêu đơn nhỏ (< 20000)?
```sql
SELECT EmpID,
       SUM(CASE WHEN TotalAmount >= 20000 THEN 1 ELSE 0 END) AS DonLon,
       SUM(CASE WHEN TotalAmount <  20000 THEN 1 ELSE 0 END) AS DonNho
FROM SALEORDER GROUP BY EmpID;
```
→ NV 2: 2 lớn (30300, 24000), 3 nhỏ; NV 3: 0 lớn, 4 nhỏ; NV 4: 0 lớn, 3 nhỏ.

#### Giải thích chi tiết và cách giải khác (Dạng 7): CASE WHEN

**Bài 7.1:** *Suy luận:* "nếu... thì ... còn lại ..." → `CASE`. *Từng dòng:* `CASE WHEN Status='COMPLETED' THEN 'Xong' ELSE 'Chua xong' END`. *Cách khác:* `IF(Status='COMPLETED','Xong','Chua xong')`. *Lỗi:* thiếu `END`.

**Bài 7.2:** *Suy luận:* "doanh thu theo từng trạng thái, mỗi trạng thái một cột" → pivot bằng `SUM(CASE ...)`. *Từng dòng:* mỗi `SUM(CASE WHEN Status=... THEN TotalAmount ELSE 0 END)` cộng đúng trạng thái; `GROUP BY CustID`. *Cách khác:* `GROUP BY CustID, Status` (kết quả dạng dọc, mỗi trạng thái một dòng). *Lỗi:* quên `ELSE 0` (ra NULL cho khách không có đơn loại đó).

**Bài 7.3:** *Suy luận:* đếm theo ngưỡng → `CASE` trả 1/0 rồi `SUM`. *Từng dòng:* hai `SUM(CASE ... THEN 1 ELSE 0 END)`. *Cách khác:* `COUNT(CASE WHEN TotalAmount >= 20000 THEN 1 END)` hoặc riêng MySQL `SUM(TotalAmount >= 20000)`. *Lỗi:* dùng `COUNT(CASE ... ELSE 0 END)` → `COUNT` đếm cả số 0 (không NULL) nên ra tổng số dòng.

### DẠNG 8: CẬP NHẬT DỮ LIỆU

> Chạy trong `START TRANSACTION; ... ROLLBACK;` để thử.

**Bài 8.1 (dễ)** Giảm 10% giá sản phẩm có tồn kho từ 100 trở lên.
```sql
UPDATE PRODUCT SET Price = Price * 0.9 WHERE Stock >= 100;
```
→ Mouse 300 → 270; USB 250 → 225 (2 dòng).

**Bài 8.2 (vừa)** Đổi chức vụ thành `Senior Sales` cho nhân viên Sales vào làm trước 2022 và lương từ 15,000,000.
```sql
UPDATE EMPLOYEE SET Position = 'Senior Sales'
WHERE Position = 'Sales' AND HireDate < '2022-01-01' AND Salary >= 15000000;
```
→ chỉ NV 2 (Nguyen Thu Ha: vào làm 2021-03-01, lương 15,000,000).

**Bài 8.3 (vừa)** Với sản phẩm tồn kho dưới 20, nhập thêm 50; các sản phẩm khác giữ nguyên (CASE WHEN).
```sql
UPDATE PRODUCT
SET Stock = CASE WHEN Stock < 20 THEN Stock + 50 ELSE Stock END;
```
→ chỉ Webcam: 15 → 65. (Laptop tồn đúng 20, không thỏa `< 20`.) *Cách khác:* `UPDATE PRODUCT SET Stock = Stock + 50 WHERE Stock < 20;` gọn hơn khi chỉ có một trường hợp.

---

#### Giải thích chi tiết và cách giải khác (Dạng 8): Cập nhật dữ liệu

**Bài 8.1:** *Suy luận:* sửa có điều kiện, giá mới dựa trên giá cũ. *Từng dòng:* `SET Price = Price * 0.9` (giá cũ × 0.9); `WHERE Stock >= 100`. *Cách khác:* `Price = Price - Price * 0.1`. *Lỗi:* quên `WHERE` → giảm giá **mọi** sản phẩm.

**Bài 8.2:** *Suy luận:* ba điều kiện lọc (chức vụ, ngày vào, lương) → `AND`. *Từng dòng:* `SET Position = 'Senior Sales'`. *Cách khác:* xem trước bằng `SELECT` cùng điều kiện. *Lỗi:* `HireDate < 2022` (thiếu nháy và là ngày đầy đủ).

**Bài 8.3:** *Suy luận:* chỉ một trường hợp đặc biệt → có thể `CASE` hoặc `WHERE`. *Từng dòng:* `CASE WHEN Stock < 20 THEN Stock + 50 ELSE Stock END`. *Cách khác:* `UPDATE ... SET Stock = Stock + 50 WHERE Stock < 20` (gọn và nhanh hơn vì chỉ chạm dòng cần sửa). *Lỗi:* quên `ELSE Stock` → các dòng còn lại thành NULL.

### DẠNG 9: CẬP NHẬT DỮ LIỆU DỰA TRÊN BẢNG KHÁC

**Bài 9.1 (vừa)** Hủy các đơn PENDING của khách ở Da Nang (dùng JOIN).
```sql
UPDATE SALEORDER o
JOIN CUSTOMER c ON c.CustID = o.CustID
SET o.Status = 'CANCELLED'
WHERE c.City = 'Da Nang' AND o.Status = 'PENDING';
```
→ chỉ đơn 6 (khách 3, Da Nang) đổi sang CANCELLED. *Cách khác:* `WHERE Status='PENDING' AND CustID IN (SELECT CustID FROM CUSTOMER WHERE City='Da Nang')`.

**Bài 9.2 (vừa)** Tăng lương 5% cho nhân viên có ít nhất một đơn COMPLETED (dùng EXISTS).
```sql
UPDATE EMPLOYEE e
SET e.Salary = e.Salary * 1.05
WHERE EXISTS (SELECT 1 FROM SALEORDER o WHERE o.EmpID = e.EmpID AND o.Status = 'COMPLETED');
```
→ NV 2: 15,750,000; NV 3: 14,700,000; NV 4: 13,650,000. NV 1 và 5 không đổi.

**Bài 9.3 (khó)** Thưởng 100,000 cho mỗi đơn COMPLETED mà nhân viên đã lập, cộng vào lương (subquery tương quan trong `SET`).
```sql
UPDATE EMPLOYEE e
SET e.Salary = e.Salary + 100000 * (
    SELECT COUNT(*) FROM SALEORDER o WHERE o.EmpID = e.EmpID AND o.Status = 'COMPLETED'
);
```
→ NV 2 (5 đơn): +500,000 = 15,500,000; NV 3 (2 đơn): 14,200,000; NV 4 (2 đơn): 13,200,000; NV 1 và NV 5: `COUNT(*) = 0` nên giữ nguyên (không phải NULL, vì `COUNT` trả 0 khi không có dòng).

#### Giải thích chi tiết và cách giải khác (Dạng 9): Cập nhật dựa trên bảng khác

**Bài 9.1:** *Suy luận:* điều kiện (thành phố) ở bảng khác → JOIN trong `UPDATE`. *Từng dòng:* `UPDATE SALEORDER o JOIN CUSTOMER c ON ... SET o.Status = ...` rồi `WHERE`. *Cách khác:* subquery `IN`. *Lỗi:* đặt `SET` trước `JOIN` (MySQL yêu cầu `JOIN` trước `SET`).

**Bài 9.2:** *Suy luận:* "có ít nhất một đơn" → `EXISTS`. *Từng dòng:* subquery tương quan với `e.EmpID`. *Cách khác:* `WHERE EmpID IN (SELECT EmpID FROM SALEORDER WHERE Status='COMPLETED')`. *Lỗi:* quên `o.EmpID = e.EmpID` → tăng lương **tất cả** nhân viên.

**Bài 9.3:** *Suy luận:* thưởng theo **số đơn** → đếm bằng subquery tương quan trong `SET`. *Từng dòng:* `100000 * (SELECT COUNT(*) ...)`. *Cách khác:* `UPDATE ... JOIN (SELECT EmpID, COUNT(*) ...GROUP BY EmpID) t` (nhân viên không có đơn không bị đổi). *Lỗi:* dùng `COUNT(o.OrderID)` với `LEFT JOIN` rồi quên `COALESCE`.

### DẠNG 10: INSERT INTO ... SELECT

**Bài 10.1 (dễ)** Sao chép phụ kiện sang bảng `PRODUCT_ACC(ProdID, ProdName, Price)`.
```sql
CREATE TABLE PRODUCT_ACC (ProdID INT PRIMARY KEY, ProdName VARCHAR(100), Price DECIMAL(12,2));
INSERT INTO PRODUCT_ACC (ProdID, ProdName, Price)
SELECT ProdID, ProdName, Price FROM PRODUCT WHERE Category = 'Accessories';
```
→ 5 dòng (ProdID 2, 3, 5, 6, 8).

**Bài 10.2 (vừa)** Lưu doanh thu COMPLETED theo tháng vào `MONTHLY_REVENUE(Thang, DoanhThu)`.
```sql
CREATE TABLE MONTHLY_REVENUE (Thang CHAR(7) PRIMARY KEY, DoanhThu DECIMAL(14,2));
INSERT INTO MONTHLY_REVENUE (Thang, DoanhThu)
SELECT DATE_FORMAT(OrderDate, '%Y-%m'), SUM(TotalAmount)
FROM SALEORDER WHERE Status = 'COMPLETED'
GROUP BY DATE_FORMAT(OrderDate, '%Y-%m');
```
→ 7 dòng (2025-01 → 2025-07), cộng lại 136100.

**Bài 10.3 (vừa)** Lưu khách chưa từng mua vào `PROSPECT(CustID, CustName)`.
```sql
CREATE TABLE PROSPECT (CustID INT PRIMARY KEY, CustName VARCHAR(100));
INSERT INTO PROSPECT (CustID, CustName)
SELECT c.CustID, c.CustName
FROM CUSTOMER c LEFT JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.OrderID IS NULL;
```
→ 1 dòng: `6 | Vu Thi Phuong`.

#### Giải thích chi tiết và cách giải khác (Dạng 10): INSERT INTO ... SELECT

**Bài 10.1:** *Suy luận:* sao chép có điều kiện. *Từng dòng:* ba cột trong ngoặc ↔ ba biểu thức `SELECT` theo vị trí. *Cách khác:* `CREATE TABLE PRODUCT_ACC AS SELECT ...` (không giữ khóa chính). *Lỗi:* lệch thứ tự cột.

**Bài 10.2:** *Suy luận:* lưu báo cáo thống kê → `INSERT` bọc `SELECT ... GROUP BY`. *Từng dòng:* cột `Thang` ↔ `DATE_FORMAT(...)`, `DoanhThu` ↔ `SUM`. *Cách khác:* tạo bảng bằng `CREATE TABLE ... AS`. *Lỗi:* kiểu `CHAR(7)` phải đủ chỗ cho `'2025-01'` (7 ký tự).

**Bài 10.3:** *Suy luận:* "chưa từng mua" → `LEFT JOIN ... IS NULL`. *Từng dòng:* chỉ chèn `CustID`, `CustName`. *Cách khác:* `WHERE CustID NOT IN (SELECT CustID FROM SALEORDER)`. *Lỗi:* `INSERT` lại lần hai → trùng khóa.

### DẠNG 11: DELETE CÓ ĐIỀU KIỆN

**Bài 11.1 (dễ)** Xóa khách chưa từng có đơn hàng.
```sql
DELETE FROM CUSTOMER WHERE CustID NOT IN (SELECT CustID FROM SALEORDER);
```
→ xóa khách 6.

**Bài 11.2 (vừa)** Xóa đơn CANCELLED cùng chi tiết của chúng.
```sql
DELETE FROM ORDER_DETAIL WHERE OrderID IN (SELECT OrderID FROM SALEORDER WHERE Status = 'CANCELLED');
DELETE FROM SALEORDER WHERE Status = 'CANCELLED';
```
→ xóa dòng chi tiết (4, 1) và đơn 4. Thứ tự: **con trước, cha sau**.

**Bài 11.3 (vừa)** Xóa sản phẩm phụ kiện chưa từng bán (dùng JOIN).
```sql
DELETE p
FROM PRODUCT p
LEFT JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID
WHERE p.Category = 'Accessories' AND od.OrderID IS NULL;
```
→ xóa Webcam (ProdID 8). `DELETE p` chỉ rõ xóa từ bảng `PRODUCT`.

#### Giải thích chi tiết và cách giải khác (Dạng 11): DELETE có điều kiện

**Bài 11.1:** *Suy luận:* xóa theo điều kiện "không tồn tại ở bảng khác". *Từng dòng:* `NOT IN (SELECT CustID FROM SALEORDER)`. *Cách khác:* `NOT EXISTS` hoặc `LEFT JOIN ... IS NULL`. *Lỗi:* xóa khách còn đơn → lỗi 1451.

**Bài 11.2:** *Suy luận:* khóa ngoại → **con trước, cha sau**. *Từng dòng:* lệnh 1 xóa chi tiết, lệnh 2 xóa đơn. *Cách khác:* tạo khóa ngoại `ON DELETE CASCADE` (cân nhắc rủi ro). *Lỗi:* đảo thứ tự.

**Bài 11.3:** *Suy luận:* "chưa từng bán" → `LEFT JOIN ... IS NULL`; xóa từ `PRODUCT`. *Từng dòng:* `DELETE p FROM PRODUCT p LEFT JOIN ...`. *Cách khác:* `NOT EXISTS` / `NOT IN`. *Lỗi:* viết `DELETE FROM PRODUCT p LEFT JOIN ...` (thiếu chỉ định bảng đích).

### DẠNG 12: SUBQUERY

**Bài 12.1 (vừa)** Sản phẩm có giá cao hơn giá trung bình **cùng nhóm hàng**.
```sql
SELECT p.ProdName, p.Category, p.Price
FROM PRODUCT p
WHERE p.Price > (SELECT AVG(p2.Price) FROM PRODUCT p2 WHERE p2.Category = p.Category);
```
→ Laptop Dell (> 9333.33 của Electronics); Keyboard Mechanical, Headphone, Webcam (> 650 của Accessories). *Suy luận:* "cùng nhóm" → subquery **tương quan**.

**Bài 12.2 (vừa)** Khách có ít nhất một đơn lớn hơn 25000.
```sql
SELECT CustName FROM CUSTOMER c
WHERE EXISTS (SELECT 1 FROM SALEORDER o WHERE o.CustID = c.CustID AND o.TotalAmount > 25000);
```
→ Le Van Cuong (đơn 5: 30300).

**Bài 12.3 (khó)** Nhân viên có doanh thu COMPLETED cao nhất.
```sql
SELECT EmpID, SUM(TotalAmount) AS Tong
FROM SALEORDER WHERE Status = 'COMPLETED'
GROUP BY EmpID
HAVING SUM(TotalAmount) = (
    SELECT MAX(t.Tong)
    FROM (SELECT SUM(TotalAmount) AS Tong FROM SALEORDER WHERE Status = 'COMPLETED' GROUP BY EmpID) t
);
```
→ `2 | 98100.00`.

#### Giải thích chi tiết và cách giải khác (Dạng 12): Subquery

**Bài 12.1:** *Suy luận:* "cùng nhóm hàng" → subquery **tương quan**. *Từng dòng:* `p2.Category = p.Category` buộc trung bình tính trong đúng nhóm của dòng đang xét. *Cách khác:* `JOIN` với bảng dẫn xuất `(SELECT Category, AVG(Price) ... GROUP BY Category)` hoặc `AVG() OVER (PARTITION BY Category)`. *Lỗi:* quên điều kiện tương quan → so với trung bình toàn bảng.

**Bài 12.2:** *Suy luận:* "có ít nhất một đơn lớn hơn 25000" → `EXISTS`. *Từng dòng:* subquery tìm đơn của khách `c` có tiền > 25000. *Cách khác:* `IN (SELECT CustID FROM SALEORDER WHERE TotalAmount > 25000)` hoặc JOIN + `DISTINCT`. *Lỗi:* quên điều kiện nối `o.CustID = c.CustID`.

**Bài 12.3:** *Suy luận:* "cao nhất" kèm cả đồng hạng → so với `MAX` của tổng. *Từng dòng:* trong cùng: tổng mỗi nhân viên; ngoài: `MAX`; `HAVING SUM(...) = (...)`. *Cách khác:* `ORDER BY ... DESC LIMIT 1` (không lấy đồng hạng) hoặc `RANK()`. *Lỗi:* `MAX(SUM(...))` lồng trực tiếp ❌.

### DẠNG 13: TRUY VẤN NGÀY THÁNG

**Bài 13.1 (dễ)** Các đơn trong 30 ngày kể từ ngày 2025-07-31 trở về trước.
```sql
SELECT OrderID, OrderDate FROM SALEORDER
WHERE OrderDate >= DATE_SUB('2025-07-31', INTERVAL 30 DAY) AND OrderDate <= '2025-07-31';
```
→ `DATE_SUB(...) = 2025-07-01`; chỉ đơn 12 (2025-07-07).

**Bài 13.2 (vừa)** Số ngày giữa đơn đầu tiên và đơn gần nhất của mỗi khách.
```sql
SELECT CustID, MIN(OrderDate) AS DauTien, MAX(OrderDate) AS GanNhat,
       DATEDIFF(MAX(OrderDate), MIN(OrderDate)) AS SoNgay
FROM SALEORDER GROUP BY CustID;
```
→ KH1: 171; KH2: 143; KH3: 20; KH4: 17; KH5: 19.

**Bài 13.3 (vừa)** Khách đăng ký trong nửa đầu 2024 (trước 2024-07-01), tính số tháng làm thành viên đến 2025-01-01.
```sql
SELECT CustName, JoinDate, TIMESTAMPDIFF(MONTH, JoinDate, '2025-01-01') AS SoThang
FROM CUSTOMER
WHERE JoinDate >= '2024-01-01' AND JoinDate < '2024-07-01';
```
→ An 11, Binh 10, Cuong 9, Dung 7, Em 6. (Phuong tham gia 2024-07-01 → ngoài khoảng.)

#### Giải thích chi tiết và cách giải khác (Dạng 13): Ngày tháng

**Bài 13.1:** *Suy luận:* "30 ngày trước 31/7" = từ `DATE_SUB(...)` đến 31/7. *Từng dòng:* cận dưới dùng `DATE_SUB`, cận trên là chính ngày. *Cách khác:* `OrderDate BETWEEN '2025-07-01' AND '2025-07-31'` (nếu biết trước ngày). *Lỗi:* `INTERVAL 30 DAYS` (đúng là `DAY`).

**Bài 13.2:** *Suy luận:* khoảng cách giữa đơn đầu và đơn cuối → `MAX` và `MIN` ngày, trừ nhau. *Từng dòng:* `DATEDIFF(MAX(...), MIN(...))` mỗi khách. *Cách khác:* `TIMESTAMPDIFF(DAY, MIN(...), MAX(...))`. *Lỗi:* đảo thứ tự tham số `DATEDIFF` → số âm.

**Bài 13.3:** *Suy luận:* tuổi thành viên theo tháng trọn → `TIMESTAMPDIFF(MONTH, ...)`; khoảng "nửa đầu 2024" bằng khoảng nửa mở. *Từng dòng:* điều kiện `JoinDate >= ... AND < ...`. *Cách khác:* `YEAR(JoinDate) = 2024 AND MONTH(JoinDate) <= 6`. *Lỗi:* `DATEDIFF(...)/30` (xấp xỉ, không trọn tháng).

### DẠNG 14: TÌM BẢN GHI LỚN NHẤT HOẶC NHỎ NHẤT

**Bài 14.1 (vừa)** Đơn có tổng lớn nhất của **mỗi khách** (JOIN với bảng gom nhóm).
```sql
SELECT o.CustID, o.OrderID, o.TotalAmount
FROM SALEORDER o
JOIN (SELECT CustID, MAX(TotalAmount) AS Mx FROM SALEORDER GROUP BY CustID) m
  ON m.CustID = o.CustID AND m.Mx = o.TotalAmount
ORDER BY o.CustID;
```
→ (1, đơn 1, 15600), (2, đơn 12, 24000), (3, đơn 5, 30300), (4, đơn 7, 13000), (5, đơn 9, 19000). *Cách khác:* `ROW_NUMBER() OVER (PARTITION BY ...)` (mục 10.5). *Lỗi hay gặp:* `SELECT CustID, OrderID, MAX(TotalAmount) ... GROUP BY CustID` → `OrderID` **không** đi cùng dòng có `MAX`.

**Bài 14.2 (dễ)** Sản phẩm rẻ nhất mỗi nhóm hàng.
```sql
SELECT p.Category, p.ProdName, p.Price
FROM PRODUCT p
WHERE p.Price = (SELECT MIN(p2.Price) FROM PRODUCT p2 WHERE p2.Category = p.Category);
```
→ Electronics: Monitor 24 inch (4000); Accessories: USB 64GB (250).

**Bài 14.3 (dễ)** Khách đăng ký sớm nhất và muộn nhất.
```sql
(SELECT 'Som nhat' AS Loai, CustName, JoinDate FROM CUSTOMER ORDER BY JoinDate ASC  LIMIT 1)
UNION ALL
(SELECT 'Muon nhat',        CustName, JoinDate FROM CUSTOMER ORDER BY JoinDate DESC LIMIT 1);
```
→ Som nhat: Nguyen Van An (2024-01-10); Muon nhat: Vu Thi Phuong (2024-07-01). *Suy luận:* mỗi vế có `ORDER BY ... LIMIT` riêng nên phải bọc trong ngoặc.

#### Giải thích chi tiết và cách giải khác (Dạng 14): Lớn nhất / nhỏ nhất

**Bài 14.1:** *Suy luận:* "lớn nhất **của mỗi**" cần giữ cả `OrderID` → không dùng `MAX` đơn thuần. *Từng dòng:* bảng dẫn xuất `m` có `MAX` mỗi khách; `JOIN` khớp `CustID` và `TotalAmount = Mx`. *Cách khác:* `ROW_NUMBER()` (một dòng/khách), hoặc `WHERE TotalAmount = (SELECT MAX(...) ... WHERE CustID = o.CustID)`. *Lỗi:* `SELECT CustID, OrderID, MAX(TotalAmount) GROUP BY CustID` (không bảo đảm `OrderID` đúng).

**Bài 14.2:** *Suy luận:* "rẻ nhất mỗi nhóm" → subquery tương quan với `MIN`. *Từng dòng:* so `p.Price` với `MIN(p2.Price)` cùng nhóm. *Cách khác:* window `MIN(Price) OVER (PARTITION BY Category)` hoặc JOIN bảng dẫn xuất. *Lỗi:* quên tương quan → chỉ ra một sản phẩm rẻ nhất toàn bảng.

**Bài 14.3:** *Suy luận:* hai truy vấn "đầu" và "cuối" → `UNION ALL`. *Từng dòng:* mỗi vế `ORDER BY ... LIMIT 1` trong ngoặc. *Cách khác:* `WHERE JoinDate = (SELECT MIN(JoinDate) ...) OR JoinDate = (SELECT MAX(JoinDate) ...)`. *Lỗi:* thiếu ngoặc quanh mỗi vế.

### DẠNG 15: TÌM ĐỐI TƯỢNG THỎA NHIỀU ĐIỀU KIỆN

**Bài 15.1 (vừa)** Khách có **cả** đơn COMPLETED **và** đơn PENDING.
```sql
SELECT CustID FROM SALEORDER
GROUP BY CustID
HAVING SUM(Status = 'COMPLETED') > 0 AND SUM(Status = 'PENDING') > 0;
```
→ 3, 5. (Trong MySQL, biểu thức `Status = 'X'` cho 1 hoặc 0, nên `SUM(...)` đếm số dòng thỏa; chuẩn SQL dùng `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`.)
*Cách khác:* `WHERE CustID IN (SELECT ... 'COMPLETED') AND CustID IN (SELECT ... 'PENDING')`.

**Bài 15.2 (khó)** Khách đã mua **cả** Laptop Dell (ProdID 1) **và** Smartphone (ProdID 7) (mọi trạng thái đơn).
```sql
SELECT c.CustName
FROM CUSTOMER c
JOIN SALEORDER o     ON o.CustID = c.CustID
JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
WHERE od.ProdID IN (1, 7)
GROUP BY c.CustID, c.CustName
HAVING COUNT(DISTINCT od.ProdID) = 2;
```
→ Tran Thi Binh, Hoang Van Em. *Suy luận:* lọc 2 sản phẩm bằng `IN`, rồi đòi hỏi khách có **đủ 2 sản phẩm khác nhau** (`COUNT(DISTINCT) = 2`). Không dùng `AND ProdID=1 AND ProdID=7` vì một dòng không thể có hai giá trị.

**Bài 15.3 (khó)** Khách ở Ha Noi hoặc Ho Chi Minh, có ≥ 2 đơn COMPLETED **và chưa có đơn CANCELLED nào**.
```sql
SELECT c.CustName
FROM CUSTOMER c
JOIN SALEORDER o ON o.CustID = c.CustID
WHERE c.City IN ('Ha Noi', 'Ho Chi Minh')
GROUP BY c.CustID, c.CustName
HAVING SUM(o.Status = 'COMPLETED') >= 2
   AND SUM(o.Status = 'CANCELLED') = 0;
```
→ Nguyen Van An, Pham Thi Dung. (Binh có 2 đơn COMPLETED nhưng có 1 đơn CANCELLED; Em chỉ có 1 đơn COMPLETED.)

#### Giải thích chi tiết và cách giải khác (Dạng 15): Thỏa nhiều điều kiện

**Bài 15.1:** *Suy luận:* "có cả A và B" của **cùng một khách** nằm ở **các dòng khác nhau** → gom theo khách rồi kiểm tra từng loại. *Từng dòng:* `SUM(Status='COMPLETED') > 0 AND SUM(Status='PENDING') > 0` (đúng/sai = 1/0). *Cách khác:* hai `IN`; hoặc `COUNT(DISTINCT CASE WHEN Status IN ('COMPLETED','PENDING') THEN Status END) = 2`. *Lỗi:* `WHERE Status='COMPLETED' AND Status='PENDING'` (không dòng nào thỏa).

**Bài 15.2:** *Suy luận:* "đã mua cả hai sản phẩm" → lọc `IN (1, 7)` rồi đòi **đủ 2 sản phẩm khác nhau**. *Từng dòng:* `HAVING COUNT(DISTINCT od.ProdID) = 2`. *Cách khác:* hai `EXISTS` (một cho mỗi sản phẩm). *Lỗi:* `AND ProdID = 1 AND ProdID = 7` trên cùng dòng.

**Bài 15.3:** *Suy luận:* "≥ 2 COMPLETED **và** 0 CANCELLED" → hai điều kiện trên số đếm theo trạng thái. *Từng dòng:* `SUM(Status = ...)` đếm trong nhóm; `WHERE` giới hạn thành phố. *Cách khác:* subquery `NOT EXISTS` cho "chưa có CANCELLED". *Lỗi:* đặt `Status = 'COMPLETED'` vào `WHERE` làm mất khả năng đếm CANCELLED.

### DẠNG 16: DOANH THU VÀ THỐNG KÊ BÁN HÀNG

**Bài 16.1 (vừa)** Top 3 sản phẩm theo doanh thu (đơn COMPLETED).
```sql
SELECT p.ProdName, SUM(od.Quantity * od.UnitPrice) AS DoanhThu
FROM ORDER_DETAIL od
JOIN SALEORDER o ON o.OrderID = od.OrderID
JOIN PRODUCT p   ON p.ProdID  = od.ProdID
WHERE o.Status = 'COMPLETED'
GROUP BY p.ProdID, p.ProdName
ORDER BY DoanhThu DESC
LIMIT 3;
```
→ Laptop Dell 75000, Smartphone 36000, Monitor 24 inch 16000.

**Bài 16.2 (vừa)** Giá trị trung bình mỗi đơn COMPLETED theo thành phố của khách.
```sql
SELECT c.City, COUNT(*) AS SoDon, AVG(o.TotalAmount) AS TrungBinh
FROM SALEORDER o JOIN CUSTOMER c ON c.CustID = o.CustID
WHERE o.Status = 'COMPLETED'
GROUP BY c.City;
```
→ Ha Noi: 5 đơn, TB 8800; Ho Chi Minh: 3 đơn, TB 20600; Da Nang: 1 đơn, TB 30300. (Hai Phong không có đơn.)

**Bài 16.3 (khó)** Tỷ trọng doanh thu COMPLETED của từng nhân viên trên tổng.
```sql
SELECT e.EmpName,
       SUM(o.TotalAmount) AS DoanhThu,
       ROUND(SUM(o.TotalAmount) * 100 / SUM(SUM(o.TotalAmount)) OVER (), 1) AS TyTrong
FROM SALEORDER o JOIN EMPLOYEE e ON e.EmpID = o.EmpID
WHERE o.Status = 'COMPLETED'
GROUP BY e.EmpID, e.EmpName;
```
| EmpName | DoanhThu | TyTrong |
|---|---|---|
| Nguyen Thu Ha | 98100.00 | 72.1 |
| Tran Quoc Huy | 31800.00 | 23.4 |
| Le Thi Lan | 6200.00 | 4.6 |

*Suy luận:* `SUM(SUM(x)) OVER ()` = tổng của các tổng nhóm = tổng toàn bảng (window chạy **sau** `GROUP BY`). Cách khác: subquery `(SELECT SUM(TotalAmount) FROM SALEORDER WHERE Status='COMPLETED')` làm mẫu số.

---

#### Giải thích chi tiết và cách giải khác (Dạng 16): Doanh thu và thống kê

**Bài 16.1:** *Suy luận:* doanh thu sản phẩm tính ở chi tiết; "top 3" → sắp giảm rồi `LIMIT 3`. *Từng dòng:* JOIN 3 bảng, `WHERE` COMPLETED, `GROUP BY` sản phẩm. *Cách khác:* `RANK() OVER (ORDER BY ... DESC)` rồi `rk <= 3` (lấy cả đồng hạng). *Lỗi:* dùng `TotalAmount` của đơn.

**Bài 16.2:** *Suy luận:* trung bình mỗi đơn theo thành phố khách → JOIN khách, gom theo `City`. *Từng dòng:* `AVG(o.TotalAmount)` (mỗi đơn là một dòng ở đây, không nhân dòng vì không JOIN chi tiết). *Cách khác:* `SUM(...)/COUNT(*)`. *Lỗi:* `AVG` sau khi JOIN thêm `ORDER_DETAIL` (nhân dòng làm lệch).

**Bài 16.3:** *Suy luận:* "tỷ trọng" = phần / tổng → cần tổng chung bên cạnh từng nhóm. *Từng dòng:* `SUM(SUM(x)) OVER ()` = tổng các tổng nhóm (window chạy sau `GROUP BY`). *Cách khác:* subquery làm mẫu số, hoặc CTE (VD25). *Lỗi:* chia hai số nguyên không nhân 100; quên `ROUND`.

---

## CHƯƠNG 14: 30 VÍ DỤ TỔNG HỢP XÂY TỪNG BƯỚC

> **Mẫu mỗi ví dụ:** Đề → Phân tích (dùng gì, vì sao) → Xây từng bước (kèm kết quả trung gian) → SQL hoàn chỉnh → Giải thích từng dòng → Kết quả → Lỗi phổ biến (sai → đúng).
> Với ví dụ UPDATE/DELETE/INSERT, hãy bọc trong `START TRANSACTION; ... ROLLBACK;` hoặc chạy lại script gốc để phục hồi dữ liệu.
> **Phương pháp xuyên suốt:** luôn bắt đầu từ `SELECT` đơn giản nhất, thêm **một lớp mỗi lần**, và chạy thử sau mỗi lớp.

### NHÓM A: SELECT CƠ BẢN VÀ JOIN (VD1–VD6)

---

#### VD1: SELECT + WHERE + ORDER BY

**Đề:** Liệt kê tên và giá các sản phẩm thuộc nhóm Electronics, giá từ cao xuống thấp.

**Phân tích:**
| Câu hỏi | Trả lời |
|---|---|
| Lấy, thêm, sửa hay xóa? | Lấy → `SELECT` |
| Bảng nào? | `PRODUCT` (đủ cả tên, giá, nhóm hàng) |
| Cần JOIN? | Không, mọi thứ nằm trong một bảng |
| Lọc từng dòng? | Có: `Category = 'Electronics'` → `WHERE` |
| Sắp xếp? | "cao xuống thấp" → `ORDER BY Price DESC` |
| Tổng hợp? | Không |

**Xây từng bước:**

*Bước 1: lấy các cột cần hiển thị.*
```sql
SELECT ProdName, Price FROM PRODUCT;
```
→ 8 dòng (cả Accessories).

*Bước 2: thêm WHERE để chỉ giữ Electronics.*
```sql
SELECT ProdName, Price FROM PRODUCT WHERE Category = 'Electronics';
```
| ProdName | Price |
|---|---|
| Laptop Dell | 15000.00 |
| Monitor 24 inch | 4000.00 |
| Smartphone | 9000.00 |

(Còn 3 dòng, theo thứ tự `ProdID`, chưa sắp theo giá.)

*Bước 3: thêm ORDER BY.*

**SQL hoàn chỉnh:**
```sql
SELECT ProdName, Price
FROM PRODUCT
WHERE Category = 'Electronics'
ORDER BY Price DESC;
```
**Giải thích từng dòng:**
- `SELECT ProdName, Price`: chỉ lấy hai cột cần hiển thị.
- `FROM PRODUCT`: nguồn dữ liệu.
- `WHERE Category = 'Electronics'`: lọc **từng dòng** trước khi sắp xếp.
- `ORDER BY Price DESC`: bước cuối, sắp theo giá giảm dần.

**Kết quả:**
| ProdName | Price |
|---|---|
| Laptop Dell | 15000.00 |
| Smartphone | 9000.00 |
| Monitor 24 inch | 4000.00 |

**Lỗi phổ biến:**
| Sai | Vì sao | Đúng |
|---|---|---|
| `ORDER BY Price DESC WHERE Category = 'Electronics'` | Sai thứ tự mệnh đề | `WHERE` trước `ORDER BY` |
| `WHERE Category = Electronics` | Thiếu nháy, MySQL hiểu là tên cột | `'Electronics'` |
| `WHERE Category == 'Electronics'` | `==` là cú pháp Python | Dùng `=` |

---

#### VD2: SELECT + JOIN + WHERE

**Đề:** Liệt kê các đơn hàng COMPLETED đặt từ ngày 2025-05-01 trở đi, kèm tên nhân viên lập đơn.

**Phân tích:**
| Câu hỏi | Trả lời |
|---|---|
| Bảng nào? | `SALEORDER` (đơn, ngày, trạng thái) và `EMPLOYEE` (tên nhân viên) |
| JOIN? | Có, nối bằng `EmpID` (khóa ngoại ↔ khóa chính) |
| WHERE? | `Status = 'COMPLETED'` và `OrderDate >= '2025-05-01'` |

**Xây từng bước:**

*Bước 1: lấy đơn kèm `EmpID`.*
```sql
SELECT OrderID, OrderDate, Status, EmpID FROM SALEORDER;     -- 12 dòng
```
*Bước 2: JOIN để đổi `EmpID` thành tên.*
```sql
SELECT o.OrderID, o.OrderDate, o.Status, e.EmpName
FROM SALEORDER o
JOIN EMPLOYEE e ON e.EmpID = o.EmpID;                         -- vẫn 12 dòng (mọi đơn đều có nhân viên)
```
*Bước 3: lọc `Status`* → còn **9** dòng (bỏ đơn 4, 6, 10).
*Bước 4: lọc ngày* → còn **4** dòng.

**SQL hoàn chỉnh:**
```sql
SELECT o.OrderID, o.OrderDate, e.EmpName
FROM SALEORDER o
JOIN EMPLOYEE e ON e.EmpID = o.EmpID
WHERE o.Status = 'COMPLETED'
  AND o.OrderDate >= '2025-05-01'
ORDER BY o.OrderID;
```
**Giải thích:**
- `SALEORDER o` / `EMPLOYEE e`: bí danh ngắn gọn.
- `ON e.EmpID = o.EmpID`: ghép mỗi đơn với đúng nhân viên lập đơn.
- `WHERE ... AND ...`: cả hai điều kiện phải đúng.
- Ngày viết dạng `'YYYY-MM-DD'` trong nháy đơn.

**Kết quả:**
| OrderID | OrderDate | EmpName |
|---|---|---|
| 8 | 2025-05-02 | Le Thi Lan |
| 9 | 2025-05-20 | Nguyen Thu Ha |
| 11 | 2025-06-25 | Le Thi Lan |
| 12 | 2025-07-07 | Nguyen Thu Ha |

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| `ON o.EmpID = e.OrderID` | Nối nhầm cột, ra kết quả vô nghĩa mà không báo lỗi | `o.EmpID = e.EmpID` |
| `SELECT OrderID, EmpID ...` (cột có ở cả hai bảng, không tiền tố) | Lỗi 1052 mơ hồ | `o.EmpID` |
| `OrderDate >= 2025-05-01` (thiếu nháy) | MySQL tính `2025 - 05 - 01 = 2019` | `'2025-05-01'` |

---

#### VD3: JOIN + GROUP BY + SUM

**Đề:** Tính tổng doanh thu từ các đơn COMPLETED của mỗi nhân viên (hiển thị tên).

**Phân tích:** "của **mỗi** nhân viên" → `GROUP BY` nhân viên; "tổng doanh thu" → `SUM(TotalAmount)`; "COMPLETED" → điều kiện từng dòng → `WHERE`; tên nằm ở `EMPLOYEE` → `JOIN`.

**Xây từng bước:**

*Bước 1: JOIN + WHERE (chưa gom nhóm), nhìn từng dòng.*
```sql
SELECT e.EmpName, o.TotalAmount
FROM EMPLOYEE e JOIN SALEORDER o ON o.EmpID = e.EmpID
WHERE o.Status = 'COMPLETED';
```
| EmpName | TotalAmount |
|---|---|
| Nguyen Thu Ha | 15600 |
| Nguyen Thu Ha | 9200 |
| Tran Quoc Huy | 18800 |
| Nguyen Thu Ha | 30300 |
| Tran Quoc Huy | 13000 |
| Le Thi Lan | 4500 |
| Nguyen Thu Ha | 19000 |
| Le Thi Lan | 1700 |
| Nguyen Thu Ha | 24000 |

*Bước 2: nhóm theo nhân viên (3 hộp):* Ha {15600, 9200, 30300, 19000, 24000}; Huy {18800, 13000}; Lan {4500, 1700}.

*Bước 3: `SUM` từng hộp:* Ha = 98100; Huy = 31800; Lan = 6200.

**SQL hoàn chỉnh:**
```sql
SELECT e.EmpName, SUM(o.TotalAmount) AS DoanhThu
FROM EMPLOYEE e
JOIN SALEORDER o ON o.EmpID = e.EmpID
WHERE o.Status = 'COMPLETED'
GROUP BY e.EmpID, e.EmpName;
```
**Giải thích:**
- `GROUP BY e.EmpID, e.EmpName`: gom theo khóa chính; thêm `EmpName` để `SELECT` được phép hiện tên.
- `SUM(o.TotalAmount)`: cộng trong từng hộp.
- `WHERE` chạy **trước** gom nhóm nên chỉ các đơn COMPLETED được cộng.

**Kết quả:**
| EmpName | DoanhThu |
|---|---|
| Nguyen Thu Ha | 98100.00 |
| Tran Quoc Huy | 31800.00 |
| Le Thi Lan | 6200.00 |

Kiểm tra: 98100 + 31800 + 6200 = 136100 = tổng doanh thu COMPLETED.

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| Thiếu `GROUP BY` | Lỗi 1140 (trộn cột với hàm tổng hợp) | Thêm `GROUP BY` |
| `GROUP BY e.EmpName` (hai nhân viên trùng tên) | Gộp nhầm | Gom theo `EmpID` |
| Bỏ `WHERE Status` | Cộng cả đơn huỷ/chờ (161700) | Giữ điều kiện |

---

#### VD4: JOIN + GROUP BY + HAVING

**Đề:** Liệt kê tên khách có ít nhất 2 đơn COMPLETED, kèm số đơn.

**Phân tích:** "mỗi khách" → `GROUP BY`; "số đơn" → `COUNT`; "COMPLETED" → `WHERE`; "ít nhất 2" là điều kiện trên **kết quả đếm** → `HAVING`.

**Xây từng bước:**

*Bước 1: đếm đơn COMPLETED mỗi khách (chưa HAVING).*
```sql
SELECT c.CustName, COUNT(*) AS SoDon
FROM CUSTOMER c JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.Status = 'COMPLETED'
GROUP BY c.CustID, c.CustName;
```
| CustName | SoDon |
|---|---|
| Nguyen Van An | 3 |
| Tran Thi Binh | 2 |
| Le Van Cuong | 1 |
| Pham Thi Dung | 2 |
| Hoang Van Em | 1 |

*Bước 2: thêm `HAVING COUNT(*) >= 2`:* loại Cuong và Em.

**SQL hoàn chỉnh:**
```sql
SELECT c.CustName, COUNT(*) AS SoDon
FROM CUSTOMER c
JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.Status = 'COMPLETED'
GROUP BY c.CustID, c.CustName
HAVING COUNT(*) >= 2;
```
**Giải thích:** `WHERE` lọc dòng → `GROUP BY` gom → `HAVING` lọc nhóm. Khách 6 (không có đơn) không có hộp nào nên không xuất hiện.

**Kết quả:**
| CustName | SoDon |
|---|---|
| Nguyen Van An | 3 |
| Tran Thi Binh | 2 |
| Pham Thi Dung | 2 |

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| `WHERE COUNT(*) >= 2` | Lỗi 1111 | `HAVING COUNT(*) >= 2` |
| `HAVING Status = 'COMPLETED'` | `Status` không còn ở mức nhóm | Đưa vào `WHERE` |
| `COUNT(o.TotalAmount)` thay `COUNT(*)` | Vẫn đúng ở đây nhưng bỏ sót nếu cột NULL | Dùng `COUNT(*)` hoặc `COUNT(o.OrderID)` |

---

#### VD5: JOIN + GROUP BY + HAVING + ORDER BY

**Đề:** Liệt kê sản phẩm có tổng doanh thu trên 3000 từ các đơn COMPLETED, sắp từ cao đến thấp.

**Phân tích:** Doanh thu theo sản phẩm tính ở mức **chi tiết đơn** (`Quantity × UnitPrice`) nên phải JOIN `ORDER_DETAIL`; cần tên sản phẩm (`PRODUCT`) và trạng thái (`SALEORDER`) → JOIN 3 bảng. `COMPLETED` → `WHERE`; "trên 3000" → `HAVING`; "sắp" → `ORDER BY`.

**Xây từng bước:**

*Bước 1: JOIN 3 bảng, lọc COMPLETED, nhìn từng dòng chi tiết:* có **19** dòng (9 đơn COMPLETED, tổng 19 dòng chi tiết).

*Bước 2: tính thành tiền mỗi dòng và gom theo sản phẩm (7 hộp):*
```sql
SELECT p.ProdName, SUM(od.Quantity * od.UnitPrice) AS DoanhThu
FROM ORDER_DETAIL od
JOIN SALEORDER o ON o.OrderID = od.OrderID
JOIN PRODUCT   p ON p.ProdID  = od.ProdID
WHERE o.Status = 'COMPLETED'
GROUP BY p.ProdID, p.ProdName;
```
| ProdName | DoanhThu |
|---|---|
| Laptop Dell | 75000.00 |
| Mouse Logitech | 1800.00 |
| Keyboard Mechanical | 3600.00 |
| Monitor 24 inch | 16000.00 |
| Headphone | 3200.00 |
| USB 64GB | 500.00 |
| Smartphone | 36000.00 |

*Bước 3: `HAVING ... > 3000`:* loại Mouse (1800) và USB (500).
*Bước 4: `ORDER BY DoanhThu DESC`.*

**SQL hoàn chỉnh:**
```sql
SELECT p.ProdName, SUM(od.Quantity * od.UnitPrice) AS DoanhThu
FROM ORDER_DETAIL od
JOIN SALEORDER o ON o.OrderID = od.OrderID
JOIN PRODUCT   p ON p.ProdID  = od.ProdID
WHERE o.Status = 'COMPLETED'
GROUP BY p.ProdID, p.ProdName
HAVING SUM(od.Quantity * od.UnitPrice) > 3000
ORDER BY DoanhThu DESC;
```
**Giải thích:**
- `FROM ORDER_DETAIL od`: bảng chi tiết là "trung tâm" vì mỗi dòng là một sản phẩm trong một đơn.
- Hai `JOIN` bổ sung trạng thái đơn và tên sản phẩm.
- `HAVING` phải lặp lại biểu thức `SUM(...)` (MySQL cho dùng bí danh trong `HAVING` nhưng lặp biểu thức an toàn hơn khi chuyển sang hệ khác).
- `ORDER BY DoanhThu`: dùng bí danh được vì `ORDER BY` chạy sau `SELECT`.

**Kết quả:**
| ProdName | DoanhThu |
|---|---|
| Laptop Dell | 75000.00 |
| Smartphone | 36000.00 |
| Monitor 24 inch | 16000.00 |
| Keyboard Mechanical | 3600.00 |
| Headphone | 3200.00 |

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| `WHERE DoanhThu > 3000` | Lỗi 1054: bí danh chưa tồn tại lúc `WHERE` chạy | `HAVING` |
| `SUM(o.TotalAmount)` thay vì `SUM(od.Quantity * od.UnitPrice)` | Nhân dòng, ra tổng cả đơn lặp lại nhiều lần | Tính ở mức chi tiết |
| `GROUP BY p.ProdName` khi hai sản phẩm trùng tên | Gộp nhầm | Thêm `p.ProdID` |

---

#### VD6: Self JOIN

**Đề:** Liệt kê các cặp nhân viên có cùng người quản lý.

**Phân tích:** Thông tin nằm trong **cùng một bảng** (`EMPLOYEE`): hai nhân viên cùng `ManagerID`. Cần đọc bảng hai lần → Self JOIN với hai bí danh `a`, `b`.

**Xây từng bước:**

*Bước 1: nối mọi cặp có cùng `ManagerID` (chưa chặn ghép với chính mình).*
```sql
SELECT a.EmpName AS NV1, b.EmpName AS NV2
FROM EMPLOYEE a JOIN EMPLOYEE b ON a.ManagerID = b.ManagerID;
```
→ **10 dòng**: 9 cặp (3 × 3) của nhóm quản lý số 1 (gồm cả cặp ghép với chính mình như Ha-Ha) và 1 dòng Minh-Minh (nhóm quản lý số 2). Quan có `ManagerID = NULL` nên không ghép được (`NULL = NULL` không đúng).

*Bước 2: thêm `a.EmpID < b.EmpID`* để bỏ cặp với chính mình và bỏ cặp lặp ngược (Ha-Huy và Huy-Ha chỉ giữ một).

**SQL hoàn chỉnh:**
```sql
SELECT a.EmpName AS NV1, b.EmpName AS NV2, a.ManagerID
FROM EMPLOYEE a
JOIN EMPLOYEE b
  ON a.ManagerID = b.ManagerID
 AND a.EmpID < b.EmpID;
```
**Giải thích:** `a` và `b` là hai "bản sao" của cùng một bảng; điều kiện `a.EmpID < b.EmpID` chọn đúng một chiều của mỗi cặp.

**Kết quả:**
| NV1 | NV2 | ManagerID |
|---|---|---|
| Nguyen Thu Ha | Tran Quoc Huy | 1 |
| Nguyen Thu Ha | Le Thi Lan | 1 |
| Tran Quoc Huy | Le Thi Lan | 1 |

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| Quên bí danh (`FROM EMPLOYEE JOIN EMPLOYEE`) | Lỗi 1066 not unique table | Dùng `a`, `b` |
| `a.EmpID <> b.EmpID` | Mỗi cặp xuất hiện 2 lần (đảo chiều) | `<` |
| Mong Minh được ghép | Minh là người duy nhất dưới quản lý số 2 | Không có cặp |

---

### NHÓM B: CASE WHEN VÀ UPDATE (VD7–VD10)

---

#### VD7: CASE WHEN trong SELECT (phân hạng khách)

**Đề:** Phân hạng khách theo tổng chi tiêu COMPLETED: từ 40000 là `VIP`, từ 25000 là `Than thiet`, còn lại `Thuong`. Khách chưa mua cũng phải xuất hiện.

**Phân tích:** Cần cả khách chưa mua → `LEFT JOIN` từ `CUSTOMER`. Điều kiện `COMPLETED` nằm ở bảng bên phải → đặt trong `ON`. Tổng có thể NULL (khách chưa mua) → `COALESCE`. Phân hạng → `CASE WHEN`.

**Xây từng bước:**

*Bước 1: tổng theo khách với LEFT JOIN.*
```sql
SELECT c.CustName, SUM(o.TotalAmount) AS Tong
FROM CUSTOMER c
LEFT JOIN SALEORDER o ON o.CustID = c.CustID AND o.Status = 'COMPLETED'
GROUP BY c.CustID, c.CustName;
```
| CustName | Tong |
|---|---|
| Nguyen Van An | 26500.00 |
| Tran Thi Binh | 42800.00 |
| Le Van Cuong | 30300.00 |
| Pham Thi Dung | 17500.00 |
| Hoang Van Em | 19000.00 |
| Vu Thi Phuong | **NULL** |

*Bước 2: `COALESCE(SUM(...), 0)`* → Phuong thành 0.
*Bước 3: bọc `CASE WHEN`.*

**SQL hoàn chỉnh:**
```sql
SELECT c.CustName,
       COALESCE(SUM(o.TotalAmount), 0) AS Tong,
       CASE
           WHEN COALESCE(SUM(o.TotalAmount), 0) >= 40000 THEN 'VIP'
           WHEN COALESCE(SUM(o.TotalAmount), 0) >= 25000 THEN 'Than thiet'
           ELSE 'Thuong'
       END AS Hang
FROM CUSTOMER c
LEFT JOIN SALEORDER o ON o.CustID = c.CustID AND o.Status = 'COMPLETED'
GROUP BY c.CustID, c.CustName;
```
**Giải thích:**
- `LEFT JOIN ... AND o.Status = 'COMPLETED'` (trong `ON`): giữ khách chưa mua hoặc không có đơn COMPLETED.
- `CASE` xét từ trên xuống, gặp điều kiện đúng đầu tiên thì dừng, nên nhánh `>= 40000` phải đứng trước nhánh `>= 25000`.
- Có thể thay bằng một CTE tính `Tong` một lần (Chương 10) để không lặp biểu thức.

**Kết quả:**
| CustName | Tong | Hang |
|---|---|---|
| Nguyen Van An | 26500.00 | Than thiet |
| Tran Thi Binh | 42800.00 | VIP |
| Le Van Cuong | 30300.00 | Than thiet |
| Pham Thi Dung | 17500.00 | Thuong |
| Hoang Van Em | 19000.00 | Thuong |
| Vu Thi Phuong | 0 | Thuong |

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| `WHERE o.Status = 'COMPLETED'` | Khách Phuong biến mất (LEFT JOIN thành INNER) | Điều kiện trong `ON` |
| Nhánh `>= 25000` đặt trước `>= 40000` | Binh bị xếp "Than thiet" | Nhánh hẹp nhất lên trước |
| Quên `ELSE` | Phuong ra NULL | Thêm `ELSE` |

---

#### VD8: CASE WHEN trong UPDATE

**Đề:** Tăng giá 5% cho nhóm Electronics và 2% cho các nhóm còn lại.

**Phân tích:** Sửa dữ liệu → `UPDATE`. Mỗi dòng được tăng theo **tỷ lệ khác nhau** tùy nhóm → một `UPDATE` với `CASE`, không cần `WHERE` (cố ý áp dụng cho mọi dòng).

**Xây từng bước:**

*Bước 1: xem trước bằng SELECT.*
```sql
SELECT ProdName, Category, Price,
       CASE Category WHEN 'Electronics' THEN Price * 1.05 ELSE Price * 1.02 END AS GiaMoi
FROM PRODUCT;
```
*Bước 2: đổi thành UPDATE (trong transaction).*

**SQL hoàn chỉnh:**
```sql
START TRANSACTION;
UPDATE PRODUCT
SET Price = CASE Category
                WHEN 'Electronics' THEN Price * 1.05
                ELSE Price * 1.02
            END;
SELECT ProdName, Price FROM PRODUCT;   -- kiểm tra
ROLLBACK;                              -- hoặc COMMIT nếu hài lòng
```
**Giải thích:** `CASE Category WHEN 'Electronics' ...` là dạng so sánh bằng; `ELSE` bao phủ mọi nhóm còn lại, nên **không dòng nào bị NULL**. Không có `WHERE` là chủ ý: nhớ cảnh báo thiếu `WHERE`.

**Kết quả (giá mới):**
| ProdName | Giá cũ | Giá mới |
|---|---|---|
| Laptop Dell | 15000 | 15750 |
| Mouse Logitech | 300 | 306 |
| Keyboard Mechanical | 1200 | 1224 |
| Monitor 24 inch | 4000 | 4200 |
| Headphone | 800 | 816 |
| USB 64GB | 250 | 255 |
| Smartphone | 9000 | 9450 |
| Webcam | 700 | 714 |

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| Quên `ELSE` | Nhóm không khớp bị gán NULL → lỗi vì cột `NOT NULL` | Có `ELSE` |
| Chạy lệnh hai lần | Giá tăng chồng | Chạy một lần / dùng transaction |
| Hai lệnh `UPDATE` riêng cho từng nhóm, dùng giá đã cập nhật | Dễ nhầm | Một `UPDATE` + `CASE` |

---

#### VD9: UPDATE + WHERE + IN + Subquery

**Đề:** Tăng tồn kho thêm 20 đơn vị cho các sản phẩm có mặt trong đơn PENDING.

**Phân tích:** Tồn kho ở `PRODUCT`; việc sản phẩm có trong đơn PENDING nằm ở `ORDER_DETAIL` + `SALEORDER`. Không cần hiển thị gì từ hai bảng đó, chỉ cần **danh sách `ProdID`** → subquery với `IN`.

**Xây từng bước:**

*Bước 1: chạy riêng subquery.*
```sql
SELECT od.ProdID
FROM ORDER_DETAIL od JOIN SALEORDER o ON o.OrderID = od.OrderID
WHERE o.Status = 'PENDING';
```
→ `6, 2, 7` (đơn 6: USB và Mouse; đơn 10: Smartphone).

*Bước 2: xem trước sẽ sửa dòng nào.*
```sql
SELECT ProdID, ProdName, Stock, Stock + 20 AS StockMoi
FROM PRODUCT WHERE ProdID IN (6, 2, 7);
```
*Bước 3: ghép subquery vào UPDATE.*

**SQL hoàn chỉnh:**
```sql
UPDATE PRODUCT
SET Stock = Stock + 20
WHERE ProdID IN (
    SELECT od.ProdID
    FROM ORDER_DETAIL od
    JOIN SALEORDER o ON o.OrderID = od.OrderID
    WHERE o.Status = 'PENDING'
);
```
**Giải thích:** câu ngoài chỉ nhìn cột của `PRODUCT`; câu trong chỉ nhìn cột của `ORDER_DETAIL`/`SALEORDER`; hai câu trao đổi với nhau bằng `ProdID`.

**Kết quả:**
| ProdID | ProdName | Stock trước | Stock sau |
|---|---|---|---|
| 2 | Mouse Logitech | 100 | 120 |
| 6 | USB 64GB | 200 | 220 |
| 7 | Smartphone | 25 | 45 |

Các sản phẩm khác giữ nguyên.

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| `IN (SELECT ProdID, Quantity ...)` | Lỗi 1241 (2 cột) | Chỉ 1 cột |
| Quên lọc `Status = 'PENDING'` | Sửa cả sản phẩm của đơn đã xong | Giữ `WHERE` trong subquery |
| `SET Stock = 20` | Ghi đè thay vì cộng thêm | `Stock = Stock + 20` |

---

#### VD10: UPDATE + JOIN dựa trên SUM của bảng khác

**Đề:** Thưởng cho mỗi nhân viên một khoản bằng 10 lần tổng doanh thu COMPLETED của họ, cộng vào lương.

**Phân tích:** Lương ở `EMPLOYEE`; doanh thu cần **tính bằng SUM + GROUP BY** từ `SALEORDER`. `UPDATE ... JOIN (bảng dẫn xuất)` cho phép lấy số đã tổng hợp ghép vào từng nhân viên.

**Xây từng bước:**

*Bước 1: bảng dẫn xuất `t`.*
```sql
SELECT EmpID, SUM(TotalAmount) AS Tong
FROM SALEORDER WHERE Status = 'COMPLETED' GROUP BY EmpID;
```
| EmpID | Tong |
|---|---|
| 2 | 98100.00 |
| 3 | 31800.00 |
| 4 | 6200.00 |

*Bước 2: SELECT xem trước khi JOIN.*
```sql
SELECT e.EmpID, e.EmpName, e.Salary, e.Salary + 10 * t.Tong AS LuongMoi
FROM EMPLOYEE e
JOIN (SELECT EmpID, SUM(TotalAmount) AS Tong
      FROM SALEORDER WHERE Status = 'COMPLETED' GROUP BY EmpID) t ON t.EmpID = e.EmpID;
```
*Bước 3: đổi thành UPDATE.*

**SQL hoàn chỉnh:**
```sql
UPDATE EMPLOYEE e
JOIN (
    SELECT EmpID, SUM(TotalAmount) AS Tong
    FROM SALEORDER
    WHERE Status = 'COMPLETED'
    GROUP BY EmpID
) t ON t.EmpID = e.EmpID
SET e.Salary = e.Salary + 10 * t.Tong;
```
**Giải thích:** `t` là bảng tạm 3 dòng; `JOIN` (inner) chỉ giữ nhân viên có trong `t`; `SET` cộng thưởng cho đúng những người đó.

**Kết quả:**
| EmpID | Lương trước | Thưởng (10 × Tong) | Lương sau |
|---|---|---|---|
| 2 | 15,000,000 | 981,000 | 15,981,000 |
| 3 | 14,000,000 | 318,000 | 14,318,000 |
| 4 | 13,000,000 | 62,000 | 13,062,000 |
| 1, 5 | không đổi (không có trong `t`) | | |

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| `LEFT JOIN` rồi `+ 10 * t.Tong` | NV 1, 5: `Salary + NULL` = NULL (vi phạm `NOT NULL` hoặc mất lương) | `JOIN`, hoặc `COALESCE(t.Tong, 0)` |
| Quên `GROUP BY` trong `t` | Lỗi hoặc nhiều dòng/nhân viên | `GROUP BY EmpID` |
| Dùng `SUM(TotalAmount)` trực tiếp trong `SET` | Lỗi 1111 | Tính trong bảng dẫn xuất |

---

### NHÓM C: INSERT ... SELECT (VD11–VD12)

---

#### VD11: INSERT INTO + SELECT + WHERE

**Đề:** Tạo bảng `PRODUCT_ELEC(ProdID, ProdName, Price)` và sao chép vào đó các sản phẩm Electronics.

**Phân tích:** "sao chép từ bảng này sang bảng khác" → `INSERT INTO ... SELECT`; "Electronics" → `WHERE` trong phần `SELECT`.

**Xây từng bước:**

*Bước 1: viết và chạy riêng SELECT.*
```sql
SELECT ProdID, ProdName, Price FROM PRODUCT WHERE Category = 'Electronics';
```
→ 3 dòng: (1, Laptop Dell, 15000), (4, Monitor 24 inch, 4000), (7, Smartphone, 9000).

*Bước 2: tạo bảng đích với số cột và kiểu khớp SELECT (theo vị trí).*
*Bước 3: ghép `INSERT INTO ... (cột đích)` lên đầu SELECT.*

**SQL hoàn chỉnh:**
```sql
CREATE TABLE PRODUCT_ELEC (
    ProdID   INT PRIMARY KEY,
    ProdName VARCHAR(100),
    Price    DECIMAL(12,2)
);

INSERT INTO PRODUCT_ELEC (ProdID, ProdName, Price)
SELECT ProdID, ProdName, Price
FROM PRODUCT
WHERE Category = 'Electronics';
```
**Giải thích:** không có từ `VALUES`; số dòng được thêm = số dòng SELECT trả về; cột thứ 1 → `ProdID`, thứ 2 → `ProdName`, thứ 3 → `Price`.

**Kết quả:** `PRODUCT_ELEC` có 3 dòng.

| ProdID | ProdName | Price |
|---|---|---|
| 1 | Laptop Dell | 15000.00 |
| 4 | Monitor 24 inch | 4000.00 |
| 7 | Smartphone | 9000.00 |

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| `SELECT ProdName, ProdID, Price` (đảo thứ tự) | Lỗi 1366 (chữ vào cột số) | Đúng thứ tự cột đích |
| `INSERT ... VALUES (SELECT ...)` | Lỗi cú pháp | Bỏ `VALUES` |
| Chạy lại lần 2 | Lỗi 1062 trùng khóa chính | `TRUNCATE` trước, hoặc `ON DUPLICATE KEY UPDATE` |

---

#### VD12: INSERT INTO + SELECT + JOIN + GROUP BY + HAVING

**Đề:** Lưu vào bảng `CUSTOMER_LOYAL(CustName, SoDon, Tong)` các khách có ít nhất 2 đơn COMPLETED, kèm số đơn và tổng tiền.

**Phân tích:** Đây là VD4 mở rộng (thêm `SUM`) + `INSERT ... SELECT`. Tên khách → JOIN `CUSTOMER`; đếm + tổng → `GROUP BY`; "ít nhất 2" → `HAVING`.

**Xây từng bước:**

*Bước 1: SELECT cho đến khi đúng.*
```sql
SELECT c.CustName, COUNT(*) AS SoDon, SUM(o.TotalAmount) AS Tong
FROM CUSTOMER c JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.Status = 'COMPLETED'
GROUP BY c.CustID, c.CustName
HAVING COUNT(*) >= 2;
```
| CustName | SoDon | Tong |
|---|---|---|
| Nguyen Van An | 3 | 26500.00 |
| Tran Thi Binh | 2 | 42800.00 |
| Pham Thi Dung | 2 | 17500.00 |

*Bước 2: tạo bảng đích (3 cột: chữ, số nguyên, tiền).*
*Bước 3: bọc `INSERT INTO ... (3 cột)`; **kiểm tra thứ tự**: `CustName, SoDon, Tong` ↔ `COUNT(*)`, `SUM(...)`.*

**SQL hoàn chỉnh:**
```sql
CREATE TABLE CUSTOMER_LOYAL (
    CustName VARCHAR(100),
    SoDon    INT,
    Tong     DECIMAL(12,2)
);

INSERT INTO CUSTOMER_LOYAL (CustName, SoDon, Tong)
SELECT c.CustName, COUNT(*), SUM(o.TotalAmount)
FROM CUSTOMER c
JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.Status = 'COMPLETED'
GROUP BY c.CustID, c.CustName
HAVING COUNT(*) >= 2;
```
**Giải thích:** phần `SELECT ... HAVING` hoàn toàn độc lập, chạy ra 3 dòng; `INSERT` chỉ việc ghi 3 dòng đó vào bảng đích theo vị trí cột.

**Kết quả:** 3 dòng như bảng ở Bước 1. Kiểm tra: `SELECT * FROM CUSTOMER_LOYAL;`.

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| `SELECT ..., SUM(o.TotalAmount), COUNT(*)` (đảo) | Không báo lỗi, `SoDon = 26500`, `Tong = 3` | Đúng thứ tự |
| Điều kiện `COUNT(*) >= 2` ở `WHERE` | Lỗi 1111 | `HAVING` |
| Bảng đích thiếu cột | Lỗi 1136 | Khớp số cột |

---

### NHÓM D: SUBQUERY, EXISTS, UNION, DELETE (VD13–VD21)

---

#### VD13: Subquery + EXISTS

**Đề:** Liệt kê nhân viên từng bán sản phẩm Smartphone (ProdID 7) trong bất kỳ đơn nào.

**Phân tích:** Chỉ cần thông tin của `EMPLOYEE`, còn việc "đã bán Smartphone" là điều kiện **tồn tại** ở bảng khác → `EXISTS` (tránh nhân dòng, không cần `DISTINCT`).

**Xây từng bước:**

*Bước 1: đơn nào có Smartphone, của nhân viên nào?*
```sql
SELECT o.OrderID, o.EmpID
FROM SALEORDER o JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
WHERE od.ProdID = 7;
```
| OrderID | EmpID |
|---|---|
| 3 | 3 |
| 7 | 3 |
| 10 | 3 |
| 12 | 2 |

*Bước 2: biến thành điều kiện tương quan cho từng nhân viên `e`:* "có dòng nào ở trên mà `EmpID` = `e.EmpID`?".

**SQL hoàn chỉnh:**
```sql
SELECT e.EmpName
FROM EMPLOYEE e
WHERE EXISTS (
    SELECT 1
    FROM SALEORDER o
    JOIN ORDER_DETAIL od ON od.OrderID = o.OrderID
    WHERE o.EmpID = e.EmpID
      AND od.ProdID = 7
);
```
**Giải thích:** với **mỗi** nhân viên `e`, MySQL chạy subquery; `o.EmpID = e.EmpID` buộc subquery gắn với nhân viên đang xét; `SELECT 1` vì chỉ quan tâm có dòng hay không.

**Kết quả:**
| EmpName |
|---|
| Nguyen Thu Ha |
| Tran Quoc Huy |

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| Quên `o.EmpID = e.EmpID` | Subquery luôn có dòng → **mọi** nhân viên đều được chọn | Có điều kiện tương quan |
| Dùng `JOIN` thay `EXISTS` mà không `DISTINCT` | Huy xuất hiện 3 lần | `DISTINCT` hoặc `EXISTS` |

---

#### VD14: Subquery trả về một giá trị trong WHERE

**Đề:** Liệt kê các đơn COMPLETED có tổng tiền cao hơn **trung bình** các đơn COMPLETED.

**Phân tích:** "cao hơn trung bình" → so sánh với một giá trị tính bằng `AVG` → subquery scalar. Phải dùng **cùng điều kiện lọc** (COMPLETED) ở cả câu trong và câu ngoài.

**Xây từng bước:**

*Bước 1: tính trung bình riêng.*
```sql
SELECT AVG(TotalAmount) FROM SALEORDER WHERE Status = 'COMPLETED';   -- 15122.222222 (136100 / 9)
```
*Bước 2: dùng số đó để lọc.*
```sql
SELECT OrderID, TotalAmount FROM SALEORDER
WHERE Status = 'COMPLETED' AND TotalAmount > 15122.22;
```
*Bước 3: thay con số bằng subquery để tự cập nhật theo dữ liệu.*

**SQL hoàn chỉnh:**
```sql
SELECT OrderID, TotalAmount
FROM SALEORDER
WHERE Status = 'COMPLETED'
  AND TotalAmount > (
        SELECT AVG(TotalAmount)
        FROM SALEORDER
        WHERE Status = 'COMPLETED'
      );
```
**Giải thích:** subquery chạy một lần, trả đúng 1 giá trị; dòng nào có `TotalAmount` lớn hơn giá trị đó được giữ.

**Kết quả:**
| OrderID | TotalAmount |
|---|---|
| 1 | 15600.00 |
| 3 | 18800.00 |
| 5 | 30300.00 |
| 9 | 19000.00 |
| 12 | 24000.00 |

**Lỗi phổ biến:**
| Sai | Hậu quả | Đúng |
|---|---|---|
| Quên lọc COMPLETED trong subquery | Trung bình thành 13475 → kết quả khác (thêm đơn 4: 15000) | Lọc cùng điều kiện |
| `= (SELECT TotalAmount ...)` trả nhiều dòng | Lỗi 1242 | Hàm tổng hợp hoặc `IN` |

---

#### VD15: Subquery trong FROM (bảng dẫn xuất)

**Đề:** Tính trung bình tổng chi tiêu của mỗi khách (các khách có đơn).

**Phân tích:** Phải tổng hợp **hai tầng**: `SUM` theo khách, rồi `AVG` các tổng. SQL không cho `AVG(SUM(...))` lồng trực tiếp → tầng một đặt trong `FROM`.

**Xây từng bước:**

*Bước 1: tổng mỗi khách.*
```sql
SELECT CustID, SUM(TotalAmount) AS Tong FROM SALEORDER GROUP BY CustID;
```
| CustID | Tong |
|---|---|
| 1 | 26500.00 |
| 2 | 57800.00 |
| 3 | 31900.00 |
| 4 | 17500.00 |
| 5 | 28000.00 |

*Bước 2: bọc làm bảng dẫn xuất `t` rồi `AVG(t.Tong)`.*

**SQL hoàn chỉnh:**
```sql
SELECT AVG(t.Tong) AS TBChiTieu
FROM (
    SELECT CustID, SUM(TotalAmount) AS Tong
    FROM SALEORDER
    GROUP BY CustID
) AS t;
```
**Kết quả:** `32340.000000` (= 161700 / 5).

**Lỗi phổ biến:** thiếu bí danh `AS t` → lỗi 1248; `SELECT AVG(SUM(TotalAmount))` → lỗi 1111; `AVG(TotalAmount)` trực tiếp ra 13475 (trung bình **mỗi đơn**, không phải mỗi khách).

---

#### VD16: NOT EXISTS

**Đề:** Sản phẩm chưa từng được bán trong bất kỳ đơn COMPLETED nào.

**Phân tích:** "chưa từng" → phủ định của tồn tại → `NOT EXISTS`, an toàn với NULL.

**Xây từng bước:**

*Bước 1: sản phẩm đã bán trong đơn COMPLETED.*
```sql
SELECT DISTINCT od.ProdID
FROM ORDER_DETAIL od JOIN SALEORDER o ON o.OrderID = od.OrderID
WHERE o.Status = 'COMPLETED';          -- 1, 2, 3, 4, 5, 6, 7
```
→ chỉ thiếu ProdID 8.

**SQL hoàn chỉnh:**
```sql
SELECT p.ProdID, p.ProdName
FROM PRODUCT p
WHERE NOT EXISTS (
    SELECT 1
    FROM ORDER_DETAIL od
    JOIN SALEORDER o ON o.OrderID = od.OrderID
    WHERE od.ProdID = p.ProdID
      AND o.Status = 'COMPLETED'
);
```
**Kết quả:** `8 | Webcam`.

**Lỗi phổ biến:** dùng `NOT IN` khi cột có thể NULL → rỗng; bỏ `od.ProdID = p.ProdID` → mọi dòng bị loại hoặc không loại nào.

---

#### VD17: LEFT JOIN + IS NULL (anti-join)

**Đề:** Liệt kê nhân viên chưa lập đơn hàng nào.

**Phân tích:** Giữ **mọi** nhân viên (bảng trái), nối đơn của họ; ai không có đơn thì cột bên phải NULL → lọc `IS NULL`.

**Xây từng bước:**

*Bước 1: LEFT JOIN, nhìn thử.*
```sql
SELECT e.EmpName, o.OrderID
FROM EMPLOYEE e LEFT JOIN SALEORDER o ON o.EmpID = e.EmpID
ORDER BY e.EmpID;
```
→ Do Minh Quan: `NULL`; Nguyen Thu Ha: 1, 2, 5, 9, 12; ...; Pham Duc Minh: `NULL`.
*Bước 2: giữ dòng có `o.OrderID IS NULL`.*

**SQL hoàn chỉnh:**
```sql
SELECT e.EmpName
FROM EMPLOYEE e
LEFT JOIN SALEORDER o ON o.EmpID = e.EmpID
WHERE o.OrderID IS NULL;
```
**Kết quả:**
| EmpName |
|---|
| Do Minh Quan |
| Pham Duc Minh |

**Lỗi phổ biến:** kiểm tra `IS NULL` trên cột của bảng **trái**; dùng `INNER JOIN` (mất hẳn các dòng cần tìm); `= NULL` thay `IS NULL`.

---

#### VD18: UNION ALL

**Đề:** Hiển thị trong một bảng kết quả: đơn nhỏ nhất và đơn lớn nhất.

**Phân tích:** Hai kết quả cùng cấu trúc nhưng từ hai câu hỏi khác nhau → nối **theo chiều dọc**: `UNION ALL` (không cần loại trùng). Mỗi vế có `ORDER BY ... LIMIT` riêng nên phải bọc ngoặc.

**Xây từng bước:**
```sql
SELECT OrderID, TotalAmount FROM SALEORDER ORDER BY TotalAmount ASC  LIMIT 1;   -- 6, 1600
SELECT OrderID, TotalAmount FROM SALEORDER ORDER BY TotalAmount DESC LIMIT 1;   -- 5, 30300
```
Thêm cột hằng `Loai` để biết dòng nào là dòng nào, rồi nối.

**SQL hoàn chỉnh:**
```sql
(SELECT 'Nho nhat' AS Loai, OrderID, TotalAmount
   FROM SALEORDER ORDER BY TotalAmount ASC  LIMIT 1)
UNION ALL
(SELECT 'Lon nhat',          OrderID, TotalAmount
   FROM SALEORDER ORDER BY TotalAmount DESC LIMIT 1);
```
**Kết quả:**
| Loai | OrderID | TotalAmount |
|---|---|---|
| Nho nhat | 6 | 1600.00 |
| Lon nhat | 5 | 30300.00 |

**Lỗi phổ biến:** không bọc ngoặc quanh từng vế có `LIMIT` → lỗi cú pháp; hai vế khác số cột → lỗi 1222; tên cột lấy từ vế đầu.

---

#### VD19: DELETE + Subquery

**Đề:** Xóa các dòng chi tiết của các đơn đã bị huỷ (CANCELLED).

**Phân tích:** Xóa → `DELETE`; xóa ở bảng **con** (`ORDER_DETAIL`) theo điều kiện thuộc bảng **cha** (`SALEORDER`) → subquery `IN`.

**Xây từng bước:**

*Bước 1: SELECT xem sẽ xóa gì.*
```sql
SELECT * FROM ORDER_DETAIL
WHERE OrderID IN (SELECT OrderID FROM SALEORDER WHERE Status = 'CANCELLED');
```
→ 1 dòng: `(OrderID 4, ProdID 1, Quantity 1, UnitPrice 15000)`.
*Bước 2: đổi `SELECT *` thành `DELETE`.*

**SQL hoàn chỉnh:**
```sql
START TRANSACTION;
DELETE FROM ORDER_DETAIL
WHERE OrderID IN (SELECT OrderID FROM SALEORDER WHERE Status = 'CANCELLED');
-- kiểm tra rồi ROLLBACK hoặc COMMIT
ROLLBACK;
```
**Kết quả:** mất 1 dòng. Nếu muốn xóa luôn đơn 4: `DELETE FROM SALEORDER WHERE Status = 'CANCELLED';` **sau** lệnh này (con trước, cha sau).

**Lỗi phổ biến:** xóa đơn trước chi tiết → lỗi 1451; quên `WHERE` → xóa **toàn bộ** chi tiết; subquery trỏ chính bảng đang xóa → lỗi 1093.

---

#### VD20: DELETE + LEFT JOIN

**Đề:** Xóa các khách hàng chưa có đơn hàng nào.

**Phân tích:** Tìm "chưa có" bằng `LEFT JOIN ... IS NULL` rồi chỉ định **xóa từ bảng nào** bằng `DELETE c`.

**Xây từng bước:**
```sql
SELECT c.CustID, c.CustName
FROM CUSTOMER c LEFT JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.OrderID IS NULL;               -- 6 | Vu Thi Phuong
```
→ đổi `SELECT ...` thành `DELETE c`.

**SQL hoàn chỉnh:**
```sql
DELETE c
FROM CUSTOMER c
LEFT JOIN SALEORDER o ON o.CustID = c.CustID
WHERE o.OrderID IS NULL;
```
**Giải thích:** `DELETE c` nghĩa là xóa các dòng của bảng bí danh `c`; `o` chỉ dùng để lọc.

**Kết quả:** xóa khách 6 (Vu Thi Phuong); 5 khách còn lại giữ nguyên.

**Lỗi phổ biến:** viết `DELETE FROM CUSTOMER c LEFT JOIN ...` (thiếu tên bảng đích sau `DELETE`); bỏ `WHERE` (xóa mọi khách có đơn lẫn không có thì bị khóa ngoại chặn).

---

#### VD21: Subquery tương quan trong SELECT

**Đề:** Hiển thị mỗi sản phẩm kèm tổng số lượng đã bán trong đơn COMPLETED (0 nếu chưa bán).

**Phân tích:** Cần **mọi sản phẩm** (kể cả Webcam) và một con số tính riêng cho từng sản phẩm → subquery tương quan đặt trong `SELECT`; `COALESCE` đổi NULL thành 0.

**Xây từng bước:**

*Bước 1: số lượng bán của riêng sản phẩm 1 (thử tay).*
```sql
SELECT SUM(od.Quantity)
FROM ORDER_DETAIL od JOIN SALEORDER o ON o.OrderID = od.OrderID
WHERE od.ProdID = 1 AND o.Status = 'COMPLETED';      -- 5
```
*Bước 2: thay `1` bằng `p.ProdID` của dòng ngoài → tương quan.*
*Bước 3: bọc `COALESCE(..., 0)` cho sản phẩm không có dòng nào.*

**SQL hoàn chỉnh:**
```sql
SELECT p.ProdName,
       COALESCE((
           SELECT SUM(od.Quantity)
           FROM ORDER_DETAIL od
           JOIN SALEORDER o ON o.OrderID = od.OrderID
           WHERE od.ProdID = p.ProdID
             AND o.Status = 'COMPLETED'
       ), 0) AS DaBan
FROM PRODUCT p;
```
**Kết quả:**
| ProdName | DaBan |
|---|---|
| Laptop Dell | 5 |
| Mouse Logitech | 6 |
| Keyboard Mechanical | 3 |
| Monitor 24 inch | 4 |
| Headphone | 4 |
| USB 64GB | 2 |
| Smartphone | 4 |
| Webcam | 0 |

**Lỗi phổ biến:** thiếu `COALESCE` → Webcam ra `NULL`; subquery trả nhiều dòng (quên `SUM`) → lỗi 1242; quên `od.ProdID = p.ProdID` → mọi sản phẩm cùng một con số.

---

### NHÓM E: NGÀY THÁNG VÀ THỐNG KÊ (VD22–VD24)

---

#### VD22: GROUP BY theo quý (hàm ngày tháng)

**Đề:** Doanh thu COMPLETED theo từng quý của năm 2025.

**Phân tích:** "theo quý" → `GROUP BY` một biểu thức ngày: `QUARTER(OrderDate)` (1–4; giống `MONTH` nhưng cho quý). Lọc năm + COMPLETED → `WHERE`.

**Xây từng bước:**

*Bước 1: doanh thu theo tháng (để thấy dữ liệu thô).*
```sql
SELECT MONTH(OrderDate) AS Thang, SUM(TotalAmount) AS DoanhThu
FROM SALEORDER WHERE Status = 'COMPLETED' GROUP BY MONTH(OrderDate);
```
| Thang | DoanhThu |
|---|---|
| 1 | 15600.00 |
| 2 | 28000.00 |
| 3 | 30300.00 |
| 4 | 13000.00 |
| 5 | 23500.00 |
| 6 | 1700.00 |
| 7 | 24000.00 |

*Bước 2: gom 3 tháng một quý:* Q1 = 15600 + 28000 + 30300 = 73900; Q2 = 13000 + 23500 + 1700 = 38200; Q3 = 24000.

**SQL hoàn chỉnh:**
```sql
SELECT QUARTER(OrderDate) AS Quy,
       SUM(TotalAmount)   AS DoanhThu
FROM SALEORDER
WHERE Status = 'COMPLETED'
  AND OrderDate >= '2025-01-01' AND OrderDate < '2026-01-01'
GROUP BY QUARTER(OrderDate)
ORDER BY Quy;
```
**Giải thích:** lọc năm bằng khoảng ngày (nhanh, tận dụng chỉ mục) thay vì `YEAR(...) = 2025`; `GROUP BY` cùng biểu thức với `SELECT`.

**Kết quả:**
| Quy | DoanhThu |
|---|---|
| 1 | 73900.00 |
| 2 | 38200.00 |
| 3 | 24000.00 |

Kiểm tra: 73900 + 38200 + 24000 = 136100.

**Lỗi phổ biến:** gom theo `MONTH` rồi cộng lẫn năm khác nhau (nếu dữ liệu nhiều năm, phải gom thêm `YEAR`); `BETWEEN '2025-01-01' AND '2025-12-31'` trên cột `DATETIME` bỏ sót giờ ngày 31/12.

---

#### VD23: CASE WHEN trong hàm tổng hợp (pivot)

**Đề:** Với mỗi đơn COMPLETED, hiển thị tiền hàng Electronics và tiền hàng Accessories ở hai cột riêng.

**Phân tích:** Một đơn có nhiều dòng chi tiết thuộc nhiều nhóm hàng; muốn "xoay" nhóm hàng thành **cột** → `SUM(CASE WHEN nhóm = ... THEN thành_tiền ELSE 0 END)`, gom theo đơn.

**Xây từng bước:**

*Bước 1: từng dòng chi tiết kèm nhóm hàng và thành tiền (đơn 1 và 8, ví dụ).*
```sql
SELECT od.OrderID, p.Category, od.Quantity * od.UnitPrice AS ThanhTien
FROM ORDER_DETAIL od JOIN PRODUCT p ON p.ProdID = od.ProdID
WHERE od.OrderID IN (1, 8);
```
| OrderID | Category | ThanhTien |
|---|---|---|
| 1 | Electronics | 15000.00 |
| 1 | Accessories | 600.00 |
| 8 | Accessories | 2400.00 |
| 8 | Accessories | 1600.00 |
| 8 | Accessories | 500.00 |

*Bước 2: `CASE` đưa thành tiền vào đúng cột, ngoài nhóm thì cho 0.*
*Bước 3: `SUM` + `GROUP BY OrderID`.* Đơn 1 → (15000, 600); đơn 8 → (0, 4500).

**SQL hoàn chỉnh:**
```sql
SELECT od.OrderID,
       SUM(CASE WHEN p.Category = 'Electronics'
                THEN od.Quantity * od.UnitPrice ELSE 0 END) AS Electronics,
       SUM(CASE WHEN p.Category = 'Accessories'
                THEN od.Quantity * od.UnitPrice ELSE 0 END) AS Accessories
FROM ORDER_DETAIL od
JOIN PRODUCT   p ON p.ProdID  = od.ProdID
JOIN SALEORDER o ON o.OrderID = od.OrderID
WHERE o.Status = 'COMPLETED'
GROUP BY od.OrderID
ORDER BY od.OrderID;
```
**Kết quả:**
| OrderID | Electronics | Accessories |
|---|---|---|
| 1 | 15000.00 | 600.00 |
| 2 | 8000.00 | 1200.00 |
| 3 | 18000.00 | 800.00 |
| 5 | 30000.00 | 300.00 |
| 7 | 13000.00 | 0.00 |
| 8 | 0.00 | 4500.00 |
| 9 | 19000.00 | 0.00 |
| 11 | 0.00 | 1700.00 |
| 12 | 24000.00 | 0.00 |

Kiểm tra: mỗi dòng cộng hai cột bằng `TotalAmount` của đơn (ví dụ đơn 1: 15000 + 600 = 15600).

**Lỗi phổ biến:** quên `ELSE 0` (không sai nhưng ra `NULL` khi không có dòng nào khớp); quên `GROUP BY` (lỗi 1140); lấy `SUM(o.TotalAmount)` thay vì thành tiền chi tiết (bị nhân dòng).

---

#### VD24: Lọc theo ngày + GROUP BY + HAVING

**Đề:** Khách có ít nhất 2 đơn (mọi trạng thái) đặt trong khoảng 2025-02-01 → 2025-05-31.

**Phân tích:** Ngày → điều kiện từng dòng → `WHERE`; "mỗi khách" → `GROUP BY CustID`; "ít nhất 2" → `HAVING COUNT(*) >= 2`.

**Xây từng bước:**

*Bước 1: các đơn trong khoảng ngày (`WHERE`): còn 8 dòng.*
| OrderID | CustID | OrderDate |
|---|---|---|
| 2 | 1 | 2025-02-10 |
| 3 | 2 | 2025-02-14 |
| 4 | 2 | 2025-03-03 |
| 5 | 3 | 2025-03-12 |
| 6 | 3 | 2025-04-01 |
| 7 | 4 | 2025-04-15 |
| 8 | 4 | 2025-05-02 |
| 9 | 5 | 2025-05-20 |

*Bước 2: gom theo `CustID`:* KH1 {2}, KH2 {3, 4}, KH3 {5, 6}, KH4 {7, 8}, KH5 {9} → đếm: 1, 2, 2, 2, 1.
*Bước 3: `HAVING COUNT(*) >= 2`* loại KH1 và KH5.

**SQL hoàn chỉnh:**
```sql
SELECT CustID, COUNT(*) AS SoDon
FROM SALEORDER
WHERE OrderDate >= '2025-02-01'
  AND OrderDate <= '2025-05-31'
GROUP BY CustID
HAVING COUNT(*) >= 2;
```
**Kết quả:**
| CustID | SoDon |
|---|---|
| 2 | 2 |
| 3 | 2 |
| 4 | 2 |

**Lỗi phổ biến:** đưa điều kiện ngày vào `HAVING` (chạy muộn, và `OrderDate` không còn ở mức nhóm); quên giới hạn ngày làm KH1, KH5 có thể thành 3 và 2 đơn (kết quả khác).

---

### NHÓM F: CTE VÀ WINDOW FUNCTIONS (VD25–VD30)

---

#### VD25: CTE + JOIN

**Đề:** Hiển thị doanh thu COMPLETED của mỗi nhân viên và tỷ trọng (%) trên tổng.

**Phân tích:** Cần dùng lại kết quả "doanh thu mỗi nhân viên" hai lần (hiển thị và tính tổng) → đặt vào **CTE** cho gọn.

**Xây từng bước:**

*Bước 1: CTE `rev`.*
```sql
SELECT EmpID, SUM(TotalAmount) AS Tong
FROM SALEORDER WHERE Status = 'COMPLETED' GROUP BY EmpID;
```
→ (2, 98100), (3, 31800), (4, 6200).
*Bước 2: tổng chung = `SELECT SUM(Tong) FROM rev` = 136100.*
*Bước 3: JOIN tên + chia.*

**SQL hoàn chỉnh:**
```sql
WITH rev AS (
    SELECT EmpID, SUM(TotalAmount) AS Tong
    FROM SALEORDER
    WHERE Status = 'COMPLETED'
    GROUP BY EmpID
)
SELECT e.EmpName,
       r.Tong,
       ROUND(r.Tong * 100 / (SELECT SUM(Tong) FROM rev), 1) AS TyTrong
FROM rev r
JOIN EMPLOYEE e ON e.EmpID = r.EmpID;
```
**Kết quả:**
| EmpName | Tong | TyTrong |
|---|---|---|
| Nguyen Thu Ha | 98100.00 | 72.1 |
| Tran Quoc Huy | 31800.00 | 23.4 |
| Le Thi Lan | 6200.00 | 4.6 |

**Lỗi phổ biến:** quên đây là **một** `WITH` cho nhiều CTE (ngăn bằng dấu phẩy); chia số nguyên không nhân 100 trước (ra 0.xx); CTE chỉ tồn tại trong **một** câu lệnh.

---

#### VD26: Window Function + PARTITION BY

**Đề:** Với mỗi nhân viên, tìm đơn COMPLETED có tổng tiền lớn nhất.

**Phân tích:** "lớn nhất của mỗi ..." và cần giữ cả thông tin đơn → `ROW_NUMBER() OVER (PARTITION BY EmpID ORDER BY TotalAmount DESC)` rồi lấy `rn = 1`. Window function không dùng được trong `WHERE` → bọc CTE.

**Xây từng bước:**

*Bước 1: đánh số thứ tự trong từng nhân viên.*
```sql
SELECT EmpID, OrderID, TotalAmount,
       ROW_NUMBER() OVER (PARTITION BY EmpID ORDER BY TotalAmount DESC) AS rn
FROM SALEORDER WHERE Status = 'COMPLETED';
```
| EmpID | OrderID | TotalAmount | rn |
|---|---|---|---|
| 2 | 5 | 30300.00 | 1 |
| 2 | 12 | 24000.00 | 2 |
| 2 | 9 | 19000.00 | 3 |
| 2 | 1 | 15600.00 | 4 |
| 2 | 2 | 9200.00 | 5 |
| 3 | 3 | 18800.00 | 1 |
| 3 | 7 | 13000.00 | 2 |
| 4 | 8 | 4500.00 | 1 |
| 4 | 11 | 1700.00 | 2 |

*Bước 2: bọc CTE, giữ `rn = 1`.*

**SQL hoàn chỉnh:**
```sql
WITH r AS (
    SELECT EmpID, OrderID, TotalAmount,
           ROW_NUMBER() OVER (PARTITION BY EmpID ORDER BY TotalAmount DESC) AS rn
    FROM SALEORDER
    WHERE Status = 'COMPLETED'
)
SELECT EmpID, OrderID, TotalAmount
FROM r
WHERE rn = 1;
```
**Kết quả:**
| EmpID | OrderID | TotalAmount |
|---|---|---|
| 2 | 5 | 30300.00 |
| 3 | 3 | 18800.00 |
| 4 | 8 | 4500.00 |

**Lỗi phổ biến:** `WHERE rn = 1` trong cùng `SELECT` đã tạo `rn` → lỗi 1054; quên `PARTITION BY` → chỉ có **một** đơn lớn nhất cho cả công ty; muốn lấy cả đơn đồng hạng → `RANK()` thay `ROW_NUMBER()`.

---

#### VD27: AVG() OVER

**Đề:** So giá từng sản phẩm với giá trung bình của nhóm hàng đó.

**Phân tích:** Cần **giữ từng sản phẩm** và hiển thị cạnh trung bình nhóm → window function (nếu dùng `GROUP BY` sẽ mất từng sản phẩm).

**Xây từng bước:**
*Bước 1:* trung bình theo nhóm bằng `GROUP BY`: Electronics 9333.33; Accessories 650.
*Bước 2:* cùng số đó nhưng **giữ từng dòng**: `AVG(Price) OVER (PARTITION BY Category)`.
*Bước 3:* trừ để ra chênh lệch.

**SQL hoàn chỉnh:**
```sql
SELECT ProdName, Category, Price,
       ROUND(AVG(Price) OVER (PARTITION BY Category), 2)         AS TB_Nhom,
       ROUND(Price - AVG(Price) OVER (PARTITION BY Category), 2) AS ChenhLech
FROM PRODUCT
ORDER BY ProdID;
```
**Kết quả:**
| ProdName | Category | Price | TB_Nhom | ChenhLech |
|---|---|---|---|---|
| Laptop Dell | Electronics | 15000.00 | 9333.33 | 5666.67 |
| Mouse Logitech | Accessories | 300.00 | 650.00 | -350.00 |
| Keyboard Mechanical | Accessories | 1200.00 | 650.00 | 550.00 |
| Monitor 24 inch | Electronics | 4000.00 | 9333.33 | -5333.33 |
| Headphone | Accessories | 800.00 | 650.00 | 150.00 |
| USB 64GB | Accessories | 250.00 | 650.00 | -400.00 |
| Smartphone | Electronics | 9000.00 | 9333.33 | -333.33 |
| Webcam | Accessories | 700.00 | 650.00 | 50.00 |

**Lỗi phổ biến:** thêm `GROUP BY` làm mất từng dòng; quên `PARTITION BY` → trung bình toàn bảng (3906.25).

---

#### VD28: CTE nhiều bước

**Đề:** Liệt kê khách có tổng chi tiêu COMPLETED cao hơn **mức trung bình của các khách**.

**Phân tích:** Hai tầng: (1) tổng mỗi khách; (2) trung bình các tổng; (3) so sánh. CTE cho phép đọc theo thứ tự các bước.

**Xây từng bước:**
*Bước 1: CTE `t`:* (1, 26500), (2, 42800), (3, 30300), (4, 17500), (5, 19000).
*Bước 2: trung bình* `SELECT AVG(Tong) FROM t` = (26500 + 42800 + 30300 + 17500 + 19000) / 5 = **27220**.
*Bước 3: lọc `Tong > 27220` và JOIN lấy tên.*

**SQL hoàn chỉnh:**
```sql
WITH t AS (
    SELECT CustID, SUM(TotalAmount) AS Tong
    FROM SALEORDER
    WHERE Status = 'COMPLETED'
    GROUP BY CustID
)
SELECT c.CustName, t.Tong
FROM t
JOIN CUSTOMER c ON c.CustID = t.CustID
WHERE t.Tong > (SELECT AVG(Tong) FROM t);
```
**Kết quả:**
| CustName | Tong |
|---|---|
| Tran Thi Binh | 42800.00 |
| Le Van Cuong | 30300.00 |

(Khách An có 26500 < 27220 nên bị loại.)

**Lỗi phổ biến:** dùng `AVG(TotalAmount)` trực tiếp (trung bình **mỗi đơn**: 15122.22, ra danh sách khác); tham chiếu CTE ở câu lệnh khác (CTE chỉ sống trong câu đang chạy).

---

#### VD29: RANK() để lấy sản phẩm bán chạy nhất (kể cả đồng hạng)

**Đề:** Tìm sản phẩm có tổng số lượng bán ra nhiều nhất; nếu nhiều sản phẩm đồng hạng thì lấy tất cả.

**Phân tích:** `ORDER BY ... LIMIT 1` bỏ sót đồng hạng → dùng `RANK()` và lấy `hang = 1`. Hai tầng (tổng, xếp hạng) → hai CTE.

**Xây từng bước:**

*Bước 1: CTE `s`:* Mouse 8; Laptop 6; USB 6; Smartphone 5; Monitor 4; Headphone 4; Keyboard 3.
*Bước 2: CTE `k`:* thêm `RANK() OVER (ORDER BY DaBan DESC)`: 1, 2, 2, 4, 5, 5, 7.
*Bước 3: lọc `hang = 1`.*

**SQL hoàn chỉnh:**
```sql
WITH s AS (
    SELECT p.ProdName, SUM(od.Quantity) AS DaBan
    FROM PRODUCT p
    JOIN ORDER_DETAIL od ON od.ProdID = p.ProdID
    GROUP BY p.ProdID, p.ProdName
),
k AS (
    SELECT ProdName, DaBan, RANK() OVER (ORDER BY DaBan DESC) AS hang
    FROM s
)
SELECT ProdName, DaBan
FROM k
WHERE hang = 1;
```
**Kết quả:** `Mouse Logitech | 8`. Nếu hai sản phẩm cùng 8 thì cả hai đều hiện.

**Lỗi phổ biến:** `ROW_NUMBER()` thay `RANK()` → chỉ một dòng; viết hai `WITH` riêng (đúng: một `WITH`, các CTE ngăn bằng dấu phẩy).

---

#### VD30: INSERT INTO + CTE + Window Function

**Đề:** Lưu đơn lớn nhất của mỗi khách hàng vào bảng `TOP_ORDER(CustID, OrderID, TotalAmount)`.

**Phân tích:** "lưu vào bảng" → `INSERT ... SELECT`; "lớn nhất của mỗi khách" → `ROW_NUMBER() OVER (PARTITION BY CustID ...)` trong CTE.

**Xây từng bước:**
*Bước 1: SELECT lõi + CTE (như VD26) cho kết quả đúng.*
```sql
WITH r AS (
    SELECT CustID, OrderID, TotalAmount,
           ROW_NUMBER() OVER (PARTITION BY CustID ORDER BY TotalAmount DESC) AS rn
    FROM SALEORDER
)
SELECT CustID, OrderID, TotalAmount FROM r WHERE rn = 1;
```
→ (1, 1, 15600), (2, 12, 24000), (3, 5, 30300), (4, 7, 13000), (5, 9, 19000).
*Bước 2: tạo bảng đích; bọc `INSERT INTO ... (3 cột)` lên trước `WITH` (MySQL 8 cho phép).*

**SQL hoàn chỉnh:**
```sql
CREATE TABLE TOP_ORDER (
    CustID      INT PRIMARY KEY,
    OrderID     INT,
    TotalAmount DECIMAL(12,2)
);

INSERT INTO TOP_ORDER (CustID, OrderID, TotalAmount)
WITH r AS (
    SELECT CustID, OrderID, TotalAmount,
           ROW_NUMBER() OVER (PARTITION BY CustID ORDER BY TotalAmount DESC) AS rn
    FROM SALEORDER
)
SELECT CustID, OrderID, TotalAmount
FROM r
WHERE rn = 1;
```
**Kết quả:**
| CustID | OrderID | TotalAmount |
|---|---|---|
| 1 | 1 | 15600.00 |
| 2 | 12 | 24000.00 |
| 3 | 5 | 30300.00 |
| 4 | 7 | 13000.00 |
| 5 | 9 | 19000.00 |

**Lỗi phổ biến:** thứ tự cột trong `SELECT` không khớp bảng đích (ghép theo vị trí); dùng MySQL 5.7 (không có CTE/window); chạy lần hai gặp lỗi 1062.

---

> Cùng với ví dụ **UPDATE lương theo doanh thu** ở mục 8.11 (phân tích rất chi tiết), tài liệu có **31 ví dụ tổng hợp**.

---

## PHỤ LỤC A: TỔNG HỢP CÚ PHÁP

### A.1. DDL (cấu trúc)
```sql
CREATE DATABASE [IF NOT EXISTS] db CHARACTER SET utf8mb4;
USE db;
CREATE TABLE t (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE,
    qty  INT NOT NULL DEFAULT 0 CHECK (qty >= 0),
    ref  INT,
    FOREIGN KEY (ref) REFERENCES other(id)
);
ALTER TABLE t ADD COLUMN c INT;
ALTER TABLE t MODIFY COLUMN c BIGINT NOT NULL DEFAULT 0;
ALTER TABLE t RENAME COLUMN c TO d;
ALTER TABLE t DROP COLUMN d;
RENAME TABLE t TO t2;
TRUNCATE TABLE t;          -- xóa hết dữ liệu, không rollback được
DROP TABLE [IF EXISTS] t;
DESCRIBE t;  SHOW TABLES;  SHOW CREATE TABLE t;
```

### A.2. DML (dữ liệu)
```sql
INSERT INTO t (a, b) VALUES (1, 'x'), (2, 'y');
INSERT INTO t (a, b) SELECT x, y FROM s WHERE ...;
INSERT INTO t (a, b) VALUES (1, 'x') ON DUPLICATE KEY UPDATE b = VALUES(b);

UPDATE t SET a = 1, b = b * 1.1 WHERE ...;
UPDATE t JOIN s ON s.id = t.id SET t.a = s.a WHERE ...;
UPDATE t SET a = CASE WHEN ... THEN ... ELSE ... END;
UPDATE t SET a = 1 WHERE id IN (SELECT id FROM s GROUP BY id HAVING SUM(x) > n);

DELETE FROM t WHERE ...;
DELETE t FROM t JOIN s ON s.id = t.id WHERE ...;
```

### A.3. SELECT đầy đủ
```sql
[WITH cte AS (SELECT ...)]
SELECT [DISTINCT] cot | bieu_thuc [AS bi_danh], ham_tong_hop(...), ham() OVER (...)
FROM bang [AS bd]
[INNER|LEFT|RIGHT|CROSS] JOIN bang2 [AS bd2] ON dieu_kien
WHERE dieu_kien_dong
GROUP BY cot1, cot2
HAVING dieu_kien_nhom
ORDER BY cot [ASC|DESC]
LIMIT n [OFFSET m];

SELECT ... UNION [ALL] SELECT ...;
```
**Thứ tự chạy:** `FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT`.

### A.4. Toán tử
| Nhóm | Toán tử |
|---|---|
| So sánh | `=  <>  !=  <  >  <=  >=  <=>` |
| Logic | `AND  OR  NOT` (ưu tiên: NOT > AND > OR) |
| Khoảng, tập | `BETWEEN a AND b`, `IN (...)`, `NOT IN (...)` |
| Chuỗi | `LIKE '%x%'` (`%` nhiều ký tự, `_` một ký tự) |
| NULL | `IS NULL`, `IS NOT NULL` |
| Tập con | `EXISTS`, `NOT EXISTS`, `ANY`, `ALL` |
| Số học | `+ - * / DIV %` |

---

## PHỤ LỤC B: CHEAT SHEET TRA CỨU NHANH

### B.1. Chọn công cụ theo đề bài

| Đề bài | Dùng |
|---|---|
| Lọc dòng | `WHERE` |
| Lọc nhóm (trên tổng/đếm) | `GROUP BY` + `HAVING` |
| Ghép thông tin từ nhiều bảng | `JOIN` |
| Giữ cả dòng không khớp | `LEFT JOIN` |
| "Chưa từng..." | `LEFT JOIN ... IS NULL` / `NOT EXISTS` |
| "Có ít nhất một..." | `EXISTS` / `IN` |
| So sánh với trung bình/tối đa | Subquery scalar |
| Xếp hạng, top-N mỗi nhóm | `ROW_NUMBER`/`RANK` + CTE |
| Lũy kế, tỷ trọng | `SUM() OVER` |
| Gộp danh sách cùng dạng | `UNION [ALL]` |
| Phân loại, pivot | `CASE WHEN` |
| Lưu kết quả vào bảng | `INSERT INTO ... SELECT` |

### B.2. Hàm thường dùng
| Nhóm | Hàm |
|---|---|
| Chuỗi | `CONCAT`, `CONCAT_WS`, `UPPER`, `LOWER`, `LEFT`, `RIGHT`, `SUBSTRING`, `LENGTH`, `CHAR_LENGTH`, `TRIM`, `REPLACE`, `LOCATE`, `SUBSTRING_INDEX` |
| Số | `ABS`, `ROUND`, `CEIL`, `FLOOR`, `MOD`, `POWER`, `SQRT` |
| Tổng hợp | `COUNT(*)`, `COUNT(col)`, `COUNT(DISTINCT col)`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP_CONCAT` |
| NULL | `IFNULL`, `COALESCE`, `NULLIF` |
| Điều kiện | `IF`, `CASE WHEN` |
| Ngày | `NOW`, `CURDATE`, `CURTIME`, `YEAR`, `MONTH`, `DAY`, `QUARTER`, `DATEDIFF`, `TIMESTAMPDIFF`, `DATE_ADD`, `DATE_SUB`, `DATE_FORMAT` |
| Khác | `CAST`, `CONVERT`, `GREATEST`, `LEAST` |
| Window | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `SUM/AVG/COUNT() OVER` |

### B.3. 12 quy tắc vàng
1. Luôn viết `SELECT` kiểm tra trước khi `UPDATE`/`DELETE`, thử trong `START TRANSACTION ... ROLLBACK`.
2. Không bao giờ `= NULL`; dùng `IS NULL`.
3. Dùng ngoặc khi trộn `AND` và `OR`.
4. Điều kiện từng dòng → `WHERE`; điều kiện trên tổng/đếm → `HAVING`.
5. Cột trong `SELECT` (không nằm trong hàm tổng hợp) phải có trong `GROUP BY`.
6. Gom nhóm theo khóa chính (`CustID`), không chỉ theo tên.
7. `LEFT JOIN`: điều kiện lọc bảng phải đặt ở `ON`; đếm bằng `COUNT(cột_bên_phải)`.
8. Cẩn thận nhân dòng khi JOIN bảng "nhiều" rồi `SUM` cột của bảng "một".
9. `NOT IN` + NULL = rỗng; ưu tiên `NOT EXISTS`.
10. `INSERT ... SELECT` ghép cột theo **vị trí**.
11. Xóa dữ liệu: con trước, cha sau.
12. Xây câu truy vấn từ trong ra ngoài, chạy thử từng lớp, kiểm tra tổng.

### B.4. Bảng lỗi MySQL thường gặp
| Mã | Ý nghĩa | Hướng xử lý |
|---|---|---|
| 1046 | No database selected | `USE db;` |
| 1048 | Column cannot be null | Điền giá trị / bỏ `NOT NULL` |
| 1052 | Ambiguous column | Thêm tiền tố bí danh |
| 1055 / 1140 | Cột không có trong GROUP BY / trộn cột với hàm tổng hợp | Thêm vào `GROUP BY` hoặc bọc hàm |
| 1062 | Duplicate entry | Trùng khóa chính / UNIQUE |
| 1093 | Bảng đích nằm trong subquery | Bọc thêm lớp derived table / JOIN |
| 1111 | Invalid use of group function | Dùng `HAVING` thay `WHERE` |
| 1136 | Số cột không khớp | Kiểm tra số cột `INSERT`/`SELECT` |
| 1175 | Safe update mode | Thêm `WHERE` theo khóa chính |
| 1241 / 1242 | Subquery sai số cột / nhiều dòng | `IN`, một cột |
| 1248 | Derived table cần alias | Thêm `AS t` |
| 1451 / 1452 | Vi phạm khóa ngoại | Xóa con trước; thêm cha trước |
| 1366 | Sai kiểu dữ liệu | Kiểm tra kiểu cột |

---

## PHỤ LỤC C: KHÁC BIỆT MYSQL / SQL SERVER / POSTGRESQL

| Chủ đề | MySQL | SQL Server | PostgreSQL |
|---|---|---|---|
| Giới hạn dòng | `LIMIT n OFFSET m` | `TOP n` / `OFFSET m ROWS FETCH NEXT n ROWS ONLY` | `LIMIT n OFFSET m` |
| Nối chuỗi | `CONCAT(a, b)` | `a + b` hoặc `CONCAT` | `a \|\| b` |
| Ngày giờ hiện tại | `NOW()`, `CURDATE()` | `GETDATE()` | `NOW()`, `CURRENT_DATE` |
| Cộng ngày | `DATE_ADD(d, INTERVAL 1 DAY)` | `DATEADD(day, 1, d)` | `d + INTERVAL '1 day'` |
| Hiệu ngày | `DATEDIFF(a, b)` | `DATEDIFF(day, b, a)` | `a - b` |
| Xử lý NULL | `IFNULL`, `COALESCE` | `ISNULL`, `COALESCE` | `COALESCE` |
| Tự tăng | `AUTO_INCREMENT` | `IDENTITY(1,1)` | `SERIAL` / `GENERATED ... AS IDENTITY` |
| Trích dẫn tên | `` `ten` `` | `[ten]` | `"ten"` |
| UPDATE + JOIN | `UPDATE t JOIN s ON ... SET ...` | `UPDATE t SET ... FROM t JOIN s ON ...` | `UPDATE t SET ... FROM s WHERE ...` |
| FULL OUTER JOIN | Không có (giả lập bằng UNION) | Có | Có |
| LIKE phân biệt hoa/thường | Không (mặc định) | Tùy collation | Có (`ILIKE` để không phân biệt) |
| Chia số nguyên `7/2` | `3.5` (`DIV` cho nguyên) | `3` | `3` |
| Xóa UNIQUE | `DROP INDEX` | `DROP CONSTRAINT` | `DROP CONSTRAINT` |
| `GROUP BY` chuẩn | `ONLY_FULL_GROUP_BY` (bản 5.7.5+) | Luôn chặt | Luôn chặt |

---

## PHỤ LỤC D: ĐƯA CƠ SỞ DỮ LIỆU VỀ TRẠNG THÁI GỐC

Sau khi làm các bài `UPDATE`, `DELETE`, `INSERT`, dữ liệu sẽ khác với các bảng minh họa. Có ba cách đưa về trạng thái gốc:

**Cách 1 — Chạy lại toàn bộ script** ở phần *Chuẩn bị* (hoặc dùng file `shop_db_reset.sql` đi kèm tài liệu). Script bắt đầu bằng `DROP DATABASE IF EXISTS shop_db;` nên xóa sạch mọi thay đổi và các bảng phụ do bài tập tạo ra (`ORDER_ARCHIVE`, `CUSTOMER_SUMMARY`, `TOP_ORDER`...). Đây là cách chắc chắn nhất.

**Cách 2 — Thử trong transaction** để không phải reset:
```sql
START TRANSACTION;
-- chạy các lệnh UPDATE / DELETE / INSERT cần thử
SELECT ...;          -- kiểm tra kết quả
ROLLBACK;            -- đưa mọi thứ về như trước (chỉ với INSERT/UPDATE/DELETE, không với DDL)
```
**Cách 3 — Dọn riêng các bảng phụ** mà bài tập đã tạo:
```sql
DROP TABLE IF EXISTS ORDER_ARCHIVE, ORDER_REPORT, CUSTOMER_SUMMARY, CUSTOMER_VIP, CUSTOMER_LOYAL,
                     EMP_REVENUE, EMP_STATS, VIP_NAMES, DEAD_STOCK, BIG_ORDER, TOP_ORDER, TOP_PRODUCT,
                     PRODUCT_ELEC, PRODUCT_ACC, MONTHLY_REVENUE, PROSPECT, HIGH_VALUE_ORDER,
                     PRODUCT_SALES, CITY_SUMMARY, ORDER_CLASS, student_demo;
DROP TABLE IF EXISTS DEMO_ENROLL, DEMO_LOG, DEMO_BOOK, DEMO_STUDENT, DEMO_CLASS;
```
**Nhắc lại thứ tự học:** (1) chạy script; (2) làm một nhóm bài; (3) reset; (4) sang nhóm tiếp theo. Nên reset **trước mỗi nhóm bài về UPDATE/DELETE** (Chương 3, Dạng 8–11 của Chương 13, các VD8–10, 19–20 của Chương 14).

---

## LỜI KẾT: CÁCH ÔN TẬP

1. **Tuần 1:** Chương 1–4. Tự gõ lại script, làm hết bài tập.
2. **Tuần 2:** Chương 5–6. Chạy từng JOIN, đếm số dòng kết quả và giải thích tại sao.
3. **Tuần 3:** Chương 7–8, **làm chậm**. Với mỗi câu `GROUP BY`, hãy dùng `GROUP_CONCAT` để *nhìn các hộp*, vẽ 6 bước như mục 7.8.
4. **Tuần 4:** Chương 9–11, rồi Chương 12–14: luyện đề theo quy trình 10 câu hỏi, tự làm trước khi xem đáp án.

*Hết tài liệu.*
