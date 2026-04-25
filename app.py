from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123' # จำเป็นสำหรับการใช้ flash messages

def get_db_connection():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# 1. ระบบ LOGIN
# ==========================================

@app.route('/')
def index():
    # หน้าแรกจะแสดงแบบฟอร์ม Log-in
    return render_template('log_in.html')

@app.route('/login', methods=['POST'])
def login():
    # รับค่าจากฟอร์ม login
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    # ตรวจสอบชื่อผู้ใช้และรหัสผ่านในตาราง manager
    user = conn.execute(
        'SELECT * FROM manager WHERE user_name = ? AND password = ?',
        (username, password)
    ).fetchone()
    conn.close()

    if user:
        # ถ้าเจอผู้ใช้ ให้กระโดดไปหน้าแคชเชียร์
        return redirect(url_for('cashier_page'))
    else:
        # ถ้าไม่เจอ ให้แจ้งเตือนและกลับไปหน้า login
        flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง กรุณาลองใหม่')
        return redirect(url_for('index'))

# ==========================================
# 2. ระบบ CASHIER (หน้าสั่งอาหาร)
# ==========================================

@app.route('/cashier')
def cashier_page():
    # แสดงหน้าจอสำหรับแคชเชียร์สั่งอาหาร
    return render_template('cashier.html')

@app.route('/api/menus')
def get_menus_api():
    """ API สำหรับส่งข้อมูลเมนูไปแสดงผลบนหน้าเว็บ (ใช้ JavaScript ดึงไป) """
    conn = get_db_connection()
    db_menus = conn.execute('SELECT * FROM menu').fetchall()
    
    # เตรียมตัวแปรแยกหมวดหมู่
    menu_data = {'pizza': [], 'snack': [], 'drink': []}
    
    for row in db_menus:
        item = {
            'id': row['menu_id'],
            'name': row['menu_name'],
            'price': row['price']
        }
        
        # ตรวจสอบหมวดหมู่ (ถ้าใน DB มีคอลัมน์ category ให้ใช้ได้เลย)
        # หากไม่มี ให้ใช้การเช็กคำสำคัญ (Keyword) จากชื่อเมนูแทน
        cat = str(row['category']).lower() if row['category'] else ""
        name_lower = row['menu_name'].lower()
        
        if 'pizza' in cat or any(w in name_lower for w in ['pizza', 'supreme', 'cheese', 'hawaiian']):
            menu_data['pizza'].append(item)
        elif 'drink' in cat or any(w in name_lower for w in ['coke', 'water', 'drink', 'tea', 'pepsi']):
            menu_data['drink'].append(item)
        else:
            menu_data['snack'].append(item)
            
    conn.close()
    return jsonify(menu_data) # ส่งกลับเป็นรูปแบบ JSON

@app.route('/checkout', methods=['POST'])
def checkout():
    """ ระบบบันทึกออเดอร์ลงฐานข้อมูลเมื่อกดชำระเงิน """
    data = request.get_json() # รับข้อมูล JSON ตะกร้าสินค้าจากหน้าบ้าน
    cart = data.get('cart', [])
    
    if not cart:
        return jsonify({'status': 'error', 'message': 'ไม่มีสินค้าในตะกร้า'}), 400

    conn = get_db_connection()
    try:
        # 1. สร้างเลขที่ออเดอร์ (Order No) ใหม่ โดยหาค่าสูงสุดเดิมแล้ว +1
        last_order = conn.execute('SELECT MAX(order_no) FROM menu_quantity').fetchone()[0]
        new_order_no = (last_order + 1) if last_order else 1001
        
        # 2. วนลูปบันทึกสินค้าแต่ละรายการในตะกร้าลงตาราง menu_quantity
        for item in cart:
            # ใช้ menu_name เป็นตัวบันทึกตามโครงสร้างที่คุณต้องการ
            conn.execute('''
                INSERT INTO menu_quantity (order_no, menu_name, quantity, subtotal)
                VALUES (?, ?, ?, ?)
            ''', (
                new_order_no, 
                item['name'], 
                item['qty'], 
                float(item['price']) * int(item['qty'])
            ))
        
        conn.commit() # ยืนยันการบันทึกข้อมูล
        return jsonify({'status': 'success', 'order_no': new_order_no})
    
    except Exception as e:
        conn.rollback() # หากเกิดข้อผิดพลาด ให้ยกเลิกสิ่งที่ทำค้างไว้
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()

# ==========================================
# 3. ระบบ MANAGER (หน้าดูรายการสั่งซื้อ)
# ==========================================

@app.route('/manager')
def manager_page():
    """ หน้าสำหรับผู้จัดการดูรายงานออเดอร์ทั้งหมด """
    conn = get_db_connection()
    # ดึงข้อมูลการสั่งซื้อทั้งหมด เรียงตามเลขออเดอร์ล่าสุดขึ้นก่อน
    orders = conn.execute('''
        SELECT order_no, menu_name, quantity, subtotal 
        FROM menu_quantity 
        ORDER BY order_no DESC
    ''').fetchall()
    conn.close()
    
    return render_template('manager.html', orders=orders)

# --- สั่งให้โปรแกรมทำงาน ---
if __name__ == '__main__':
    # debug=True ช่วยให้หน้าเว็บอัปเดตอัตโนมัติเมื่อมีการแก้ไขโค้ด Python
    app.run(debug=True)
