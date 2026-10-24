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
