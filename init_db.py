# init_db.py
import sqlite3
from models import TABLE_SCHEMA

def initialize_database():
    try:
        # เชื่อมต่อฐานข้อมูล (จะสร้างไฟล์ restaurant.db ขึ้นมาโดยอัตโนมัติ)
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        
        # รันคำสั่งสร้างตารางจาก models.py
        cursor.executescript(TABLE_SCHEMA)
        
        # --- ใส่ข้อมูลเริ่มต้น (Seed Data) ---
        print("กำลังใส่ข้อมูลตัวอย่าง...")
        
        cursor.execute("INSERT INTO MANAGER VALUES ('M01', 'Somchai_Admin', 'pizza1234')")
        cursor.execute("INSERT INTO CUSTOMER VALUES (101, 'VIP_Member')")
        cursor.execute("INSERT INTO MENU VALUES ('Seafood Deluxe', 399.00, 'M01')")
        cursor.execute("INSERT INTO MENU VALUES ('Pepperoni', 299.00, 'M01')")
        cursor.execute("INSERT INTO `ORDER` VALUES (501, 101, 'M01')")
        cursor.execute("INSERT INTO TOTAL_ORDER VALUES (501, 'Seafood Deluxe', 2, 798.00)")
        
        conn.commit()
        print("✅ สร้างฐานข้อมูล PizzyPizza และตารางทั้งหมดสำเร็จแล้ว!")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    initialize_database()