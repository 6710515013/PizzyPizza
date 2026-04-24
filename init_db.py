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
        
        # 1. ข้อมูลผู้จัดการ (manager_id, user_name, password)
        cursor.execute("INSERT INTO MANAGER VALUES ('M01', 'Somchai_Admin', 'pizza1234')")
        
        # 2. ข้อมูลลูกค้า (customer_no, customer_status)
        cursor.execute("INSERT INTO CUSTOMER VALUES (101, 'VIP_Member')")
        
        # 3. ข้อมูลเมนูอาหาร (menu_name, price, category, image_url, description, manager_id)
        # 💡 แก้ไข: เพิ่มข้อมูลให้ครบ 6 คอลัมน์ตาม Schema
        cursor.execute("INSERT INTO MENU VALUES ('Seafood Deluxe', 399.00, 'Pizza', '', 'พิซซ่าหน้าซีฟู้ดเครื่องแน่น', 'M01')")
        cursor.execute("INSERT INTO MENU VALUES ('Pepperoni', 299.00, 'Pizza', '', 'พิซซ่าหน้าเปปเปอโรนีและชีส', 'M01')")
        cursor.execute("INSERT INTO MENU VALUES ('French Fries', 89.00, 'Snack', '', 'มันฝรั่งทอดกรอบ', 'M01')")
        
        # 4. ข้อมูลบิลออเดอร์ (order_no, customer_no, manager_id)
        cursor.execute("INSERT INTO `ORDER` VALUES (501, 101, 'M01')")
        
        # 5. ข้อมูลรายการอาหารในบิลนั้น (order_no, menu_name, quantity, subtotal)
        cursor.execute("INSERT INTO TOTAL_ORDER VALUES (501, 'Seafood Deluxe', 2, 798.00)")
        cursor.execute("INSERT INTO TOTAL_ORDER VALUES (501, 'French Fries', 1, 89.00)")
        
        # ยืนยันการบันทึกข้อมูล
        conn.commit()
        print("✅ สร้างฐานข้อมูล PizzyPizza และตารางทั้งหมดสำเร็จแล้ว!")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
    finally:
        # ปิดการเชื่อมต่อทุกครั้ง
        conn.close()

if __name__ == '__main__':
    initialize_database()