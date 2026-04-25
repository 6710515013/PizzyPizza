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
        cursor.execute("INSERT INTO menu (menu_name, price, image_url, category) VALUES ('Hawaiian Pizza', 299, '', 'pizza')") 
        cursor.execute("INSERT INTO menu (menu_name, price, image_url, category) VALUES ('Tom Yum Kung', 399, '', 'pizza')")
        cursor.execute("INSERT INTO menu (menu_name, price, image_url, category) VALUES ('Pepperoni', 299, '', 'pizza')")
        cursor.execute("INSERT INTO menu (menu_name, price, image_url, category) VALUES ('Super Supreme', 359, '', 'pizza')")
        cursor.execute("INSERT INTO menu (menu_name, price, image_url, category) VALUES ('Seafood Cocktail', 359, '', 'pizza')")
        cursor.execute("INSERT INTO menu (menu_name, price, image_url, category) VALUES ('Double Cheese', 299, '', 'pizza')")
        cursor.execute("INSERT INTO menu (menu_name, price, image_url, category) VALUES ('French Fries', 79, '', 'snack')")
        cursor.execute("INSERT INTO menu (menu_name, price, image_url, category) VALUES ('Spaghetti Carbonara', 129, '', 'snack')")
        cursor.execute("INSERT INTO menu (menu_name, price, image_url, category) VALUES ('Cheese Sticks', 99, '', 'snack')")
        
        # 3. ใส่ข้อมูลเครื่องดื่ม 
        cursor.execute("INSERT INTO menu (menu_name, price, image_url, category) VALUES ('Refill Soft Drinks', 49, '', 'drink')")
       
        
    
        
        # 4. ใส่ Log ตัวอย่าง
        cursor.execute("""
            INSERT INTO manager_logs (manager_id, action_type, old_value, new_value) 
            VALUES (1, 'CREATE', 'menu', 'Hawaiian Pizza 299')
        """)
        
        conn.commit()
        print("✅ อัปเดตฐานข้อมูลเป็นโครงสร้างใหม่สำเร็จแล้ว!")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    initialize_database()