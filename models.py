# models.py

# รวมคำสั่ง SQL สำหรับสร้างตารางทั้งหมด
TABLE_SCHEMA = '''
-- ลบตารางเก่าทิ้งก่อน (ถ้ามี)
DROP TABLE IF EXISTS TOTAL_ORDER;
DROP TABLE IF EXISTS `ORDER`;
DROP TABLE IF EXISTS MENU;
DROP TABLE IF EXISTS `TABLE`;
DROP TABLE IF EXISTS CUSTOMER;
DROP TABLE IF EXISTS MANAGER;

-- ========================
-- TABLE: MANAGER
-- ========================
CREATE TABLE MANAGER (
    manager_id VARCHAR(10) PRIMARY KEY,
    user_name VARCHAR(50),
    password VARCHAR(50)
);

-- ========================
-- TABLE: CUSTOMER
-- ========================
CREATE TABLE CUSTOMER (
    customer_no INT PRIMARY KEY,
    customer_status VARCHAR(20)
);

-- ========================
-- TABLE: TABLE (ชื่อชน keyword ต้องใส่ `)
-- ========================
CREATE TABLE `TABLE` (
    table_no INT PRIMARY KEY,
    customer_no INT,
    FOREIGN KEY (customer_no) REFERENCES CUSTOMER(customer_no)
);

-- ========================
-- TABLE: MENU (แก้แล้ว ✨)
-- ========================
CREATE TABLE MENU (
    menu_name VARCHAR(100) PRIMARY KEY,
    price DECIMAL(10, 2),
    category VARCHAR(50),
    image_url VARCHAR(255),
    description TEXT,
    manager_id VARCHAR(10),
    FOREIGN KEY (manager_id) REFERENCES MANAGER(manager_id)
);

-- ========================
-- TABLE: ORDER (keyword ต้องใส่ `)
-- ========================
CREATE TABLE `ORDER` (
    order_no INT PRIMARY KEY,
    customer_no INT,
    manager_id VARCHAR(10),
    FOREIGN KEY (customer_no) REFERENCES CUSTOMER(customer_no),
    FOREIGN KEY (manager_id) REFERENCES MANAGER(manager_id)
);

-- ========================
-- TABLE: TOTAL_ORDER (ตารางกลาง)
-- ========================
CREATE TABLE TOTAL_ORDER (
    order_no INT,
    menu_name VARCHAR(100),
    quantity INT,
    subtotal DECIMAL(10, 2),
    PRIMARY KEY (order_no, menu_name),
    FOREIGN KEY (order_no) REFERENCES `ORDER`(order_no),
    FOREIGN KEY (menu_name) REFERENCES MENU(menu_name)
);
'''