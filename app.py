from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = sqlite3.Row # ช่วยให้เรียกข้อมูลด้วยชื่อคอลัมน์ได้ เช่น row['menu_name']
    return conn

# หน้าแสดงผล POS สำหรับแคชเชียร์
# แก้ไขใน app.py
@app.route('/')
def index():
    conn = get_db_connection()
    # ดึงข้อมูลจากฐานข้อมูล
    db_menus = conn.execute('SELECT * FROM menu').fetchall()
    
    # --- สำคัญ: สร้างตัวแปรชื่อ menu_data เพื่อส่งให้ HTML ---
    menu_data = {'pizza': [], 'snack': [], 'drink': []}
    
    for row in db_menus:
        item = {
            'id': row['menu_id'],
            'name': row['menu_name'],
            'price': row['price']
        }
        
        # แปลงทุกอย่างเป็นตัวพิมพ์เล็กเพื่อลดความผิดพลาดในการเช็กชื่อ
        menu_name = row['menu_name'].lower()
        db_category = row['category'].lower()
        
        # 1. แยกกลุ่ม Drinks (อันนี้มักจะไม่มีปัญหาเพราะหมวดแยกชัดเจน)
        if db_category == 'drinks' or db_category == 'drink':
            menu_data['drink'].append(item)
            
        # 2. แยกกลุ่ม Food ออกเป็น Pizza และ Snack
        elif db_category == 'food':
            # เช็กคีย์เวิร์ดที่อาจจะเป็นพิซซ่าทั้งหมด
            pizza_keywords = ['pizza', 'supreme', 'pepperoni', 'cocktail', 'cheese']
            
            # ถ้ามีคำใดคำหนึ่งใน pizza_keywords อยู่ในชื่อเมนู ให้ลงหมวด pizza
            if any(word in menu_name for word in pizza_keywords):
                menu_data['pizza'].append(item)
            else:
                # ถ้าเป็น Food แต่ไม่มีคำพวกนั้น (เช่น French Fries, Spaghetti, Sticks) ให้ลง Snack
                menu_data['snack'].append(item)
            
    conn.close()
    
    # --- ส่ง menu_data ออกไป (ชื่อต้องตรงกับที่ใช้ใน {{ ... }}) ---
    return render_template('cashier.html', menu_data=menu_data)

# Route สำหรับรับออเดอร์
@app.route('/order', methods=['POST'])
def place_order():
    # 1. ดึงข้อมูลจากฟอร์ม (เปลี่ยนจากชื่อเป็น ID และจำนวน)
    menu_id = request.form['menu_id']
    quantity = int(request.form['quantity'])
    
    conn = get_db_connection()
    
    # 2. ไปดึงราคาจากฐานข้อมูลตาม menu_id (ไม่ต้อง Hardcode ในโค้ดแล้ว)
    menu_data = conn.execute('SELECT price FROM menu WHERE menu_id = ?', (menu_id,)).fetchone()
    
    if menu_data:
        price = menu_data['price']
        subtotal = price * quantity
        
        # 3. สร้างเลขคิว (order_no) 
        # ในโปรเจคแรกแบบง่าย: ให้หาเลขคิวล่าสุดแล้วบวก 1 ถ้ายังไม่มีออเดอร์เลยให้เริ่มที่ 1001
        last_order = conn.execute('SELECT MAX(order_no) FROM menu_quantity').fetchone()[0]
        new_order_no = (last_order + 1) if last_order else 1001
        
        # 4. บันทึกลงตาราง menu_quantity
        conn.execute('''
            INSERT INTO menu_quantity (order_no, menu_id, quantity, subtotal)
            VALUES (?, ?, ?, ?)
        ''', (new_order_no, menu_id, quantity, subtotal))
        
        conn.commit()
    
    conn.close()
    
    # สั่งเสร็จให้เด้งกลับไปหน้าแรกเพื่อดูคิวที่เพิ่งสร้าง
    return redirect(url_for('index'))

@app.route('/api/menus')
def get_menus_api():
    conn = get_db_connection()
    db_menus = conn.execute('SELECT * FROM menu').fetchall()
    
    menu_data = {'pizza': [], 'snack': [], 'drink': []}
    
    for row in db_menus:
        item = {
            'id': row['menu_id'],
            'name': row['menu_name'],
            'price': row['price']
        }
        
        db_category = row['category'].lower()
        menu_name = row['menu_name'].lower()
        
        # 1. แยกกลุ่มเครื่องดื่ม
        if db_category in ['drinks', 'drink']:
            menu_data['drink'].append(item)
            
        # 2. แยกกลุ่มของว่าง (เช็กจากหมวดหมู่ 'snack' ใน DB โดยตรง)
        elif db_category == 'snack':
            menu_data['snack'].append(item)
            
        # 3. แยกกลุ่มอาหาร (Food) ซึ่งส่วนใหญ่คือพิซซ่า
        elif db_category == 'food':
            # รายการคำค้นหาพิซซ่า
            pizza_keywords = ['pizza', 'supreme', 'pepperoni', 'cocktail', 'cheese', 'hawaiian', 'kung']
            
            if any(word in menu_name for word in pizza_keywords):
                menu_data['pizza'].append(item)
            else:
                # กรณีฉุกเฉินถ้าเป็น Food แต่ไม่มีคำว่าพิซซ่า ให้ลง Snack
                menu_data['snack'].append(item)
                
    conn.close()
    return jsonify(menu_data)

if __name__ == '__main__':
    app.run(debug=True)