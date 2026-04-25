from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123' # จำเป็นสำหรับการใช้ flash messages

def get_db_connection():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = sqlite3.Row
    return conn

# 1. หน้าแรก (แสดงหน้า Login)
@app.route('/')
def index():
    return render_template('log_in.html')

# 2. ฟังก์ชันตรวจสอบ Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM manager WHERE user_name = ? AND password = ?',
        (username, password)
    ).fetchone()
    conn.close()

    if user:
        # ✅ Login สำเร็จ -> ไปที่หน้า cashier
        return redirect(url_for('cashier_page'))
    else:
        # ❌ Login ไม่สำเร็จ -> กลับไปหน้า login พร้อมแจ้งเตือน
        flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
        return redirect(url_for('index'))

# 3. หน้าสำหรับแคชเชียร์รับออเดอร์ (เข้าถึงหลัง Login เท่านั้น)
@app.route('/cashier')
def cashier_page():
    conn = get_db_connection()
    # ดึงข้อมูลเมนูไปแสดง
    menus = conn.execute('SELECT * FROM menu').fetchall()
    # ดึงรายการสั่งซื้อล่าสุด
    orders = conn.execute('''
        SELECT mq.order_no, m.menu_name, mq.quantity, mq.subtotal 
        FROM menu_quantity mq 
        JOIN menu m ON mq.menu_name = m.menu_name                                           
        ORDER BY mq.order_no DESC
    ''').fetchall()
    conn.close()
    return render_template('cashier.html', menus=menus, orders=orders)

# 4. Route สำหรับรับออเดอร์ (Action จากหน้า cashier)
@app.route('/order', methods=['POST'])
def place_order():
    menu_id = request.form['menu_id']
    quantity = int(request.form['quantity'])
    
    conn = get_db_connection()
    menu_data = conn.execute('SELECT price FROM menu WHERE menu_id = ?', (menu_id,)).fetchone()
    
    if menu_data:
        price = menu_data['price']
        subtotal = price * quantity
        
        last_order = conn.execute('SELECT MAX(order_no) FROM menu_quantity').fetchone()[0]
        new_order_no = (last_order + 1) if last_order else 1001
        
        conn.execute('''
            INSERT INTO menu_quantity (order_no, menu_name, quantity, subtotal)
            VALUES (?, ?, ?, ?)
        ''', (new_order_no, menu_id, quantity, subtotal))
        conn.commit()
    
    conn.close()
    return redirect(url_for('cashier_page'))

@app.route('/manager')
def manager_page():
    conn = get_db_connection()

    orders = conn.execute('''
        SELECT mq.order_no, m.menu_name, mq.quantity, mq.subtotal
        FROM menu_quantity mq
        JOIN menu m ON mq.menu_name = m.menu_name
        ORDER BY mq.order_no DESC
    ''').fetchall()

    conn.close()

    return render_template('manager.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)