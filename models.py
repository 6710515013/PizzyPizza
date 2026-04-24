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
    menu_name VARCHAR(255) NOT NULL,
    price INTEGER NOT NULL
    image_url TEXT,
    category TEXT 
);

-- ========================
-- Table: menu_quantity
-- ========================
CREATE TABLE menu_quantity (
    Qnumber INTEGER PRIMARY KEY AUTOINCREMENT,
    order_no INTEGER NOT NULL,
    menu_id INTEGER,
    quantity INTEGER NOT NULL,
    subtotal INTEGER NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES menu (menu_id) ON DELETE SET NULL
);

-- ========================
-- Table: manager_logs
-- ========================
CREATE TABLE manager_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    manager_id INTEGER,
    action_type VARCHAR(50),
    table_name VARCHAR(50),
    old_value TEXT,
    new_value TEXT,
    FOREIGN KEY (manager_id) REFERENCES manager (manager_id) ON DELETE SET NULL
);
'''