# init_db.py
import sqlite3
from models import TABLE_SCHEMA

def initialize_database():
    try:
        # เชื่อมต่อฐานข้อมูล
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        
        # รันคำสั่งสร้างตารางใหม่ทั้งหมด
        cursor.executescript(TABLE_SCHEMA)
        
        print("กำลังใส่ข้อมูลตัวอย่าง (Redesign Version)...")
        
        # 1. ใส่ข้อมูลผู้จัดการ (manager_id ปล่อยเป็น NULL เพื่อให้ Auto Increment)
        cursor.execute("INSERT INTO manager (user_name, password) VALUES ('Admin_Pizza', 'pass1234')")
        
        # 2. ใส่ข้อมูลเมนู
        cursor.execute("INSERT INTO menu (menu_name, price) VALUES ('Hawaiian Pizza', 299)")
        cursor.execute("INSERT INTO menu (menu_name, price) VALUES ('Meat Lover', 350)")
        cursor.execute("INSERT INTO menu (menu_name, price) VALUES ('Coke Large', 45)")
        
        # 3. ใส่ข้อมูลออเดอร์ทดสอบ (สมมติ order_no = 1001)
        # ใส่รายการที่ 1: Hawaiian 2 ถาด
        cursor.execute("INSERT INTO menu_quantity (order_no, menu_id, quantity, subtotal) VALUES (1001, 1, 2, 598)")
        # ใส่รายการที่ 2: Coke 1 ขวด
        cursor.execute("INSERT INTO menu_quantity (order_no, menu_id, quantity, subtotal) VALUES (1001, 3, 1, 45)")
        
        # 4. ใส่ Log ตัวอย่าง
        cursor.execute("""
            INSERT INTO manager_logs (manager_id, action_type, table_name, old_value, new_value) 
            VALUES (1, 'CREATE', 'menu', '-', 'Hawaiian Pizza 299')
        """)
        
        conn.commit()
        print("✅ อัปเดตฐานข้อมูลเป็นโครงสร้างใหม่สำเร็จแล้ว!")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    initialize_database()