# models.py

# รวมคำสั่ง SQL สำหรับสร้างตารางใหม่ตาม Redesign
TABLE_SCHEMA = '''
-- เปิดการใช้งาน Foreign Key (สำคัญสำหรับ SQLite)
PRAGMA foreign_keys = ON;

-- ลบตารางเก่าทิ้งก่อน (ถ้ามี)
DROP TABLE IF EXISTS manager_logs;
DROP TABLE IF EXISTS menu_quantity;
DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS manager;

-- ========================
-- Table: manager
-- ========================
CREATE TABLE manager (
    manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- ========================
-- Table: menu
-- ========================
CREATE TABLE menu (
    menu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_name VARCHAR(255) UNIQUE,
    price INTEGER NOT NULL,
    category TEXT 
);

-- ========================
-- Table: menu_quantity
-- ========================
CREATE TABLE menu_quantity (
    order_no INTEGER NOT NULL,
    menu_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    subtotal INTEGER NOT NULL,
    -- กำหนดให้ order_no และ menu_name รวมกันเป็น Primary Key
    PRIMARY KEY (order_no, menu_name)
);


-- ========================
-- Table: manager_logs
-- ========================
CREATE TABLE manager_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    manager_id INTEGER,
    action_type VARCHAR(50),
    old_value TEXT,
    new_value TEXT,
    FOREIGN KEY (manager_id) REFERENCES manager (manager_id) ON DELETE SET NULL
);
'''