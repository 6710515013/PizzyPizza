from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = sqlite3.Row
    return conn

# หน้าแสดงผลรายการสั่งซื้อ
@app.route('/')
def index():
    conn = get_db_connection()
    # ดึงข้อมูลมาโชว์ในหน้า user.html
    orders = conn.execute('SELECT * FROM TOTAL_ORDER').fetchall()
    conn.close()
    return render_template('user.html', orders=orders)

# Route สำหรับรับข้อมูลจากฟอร์มการสั่งอาหาร
@app.route('/order', methods=['POST'])
def place_order():
    # 1. ดึงข้อมูลจากฟอร์ม
    table_no = request.form['table_no']
    menu_name = request.form['menu_name']
    quantity = int(request.form['quantity'])
    
    # 2. เชื่อมต่อฐานข้อมูล
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    # 3. สมมติราคา (ตามที่ตกลงกันไว้)
    price = 399.0 if menu_name == 'Seafood Deluxe' else 299.0
    subtotal = price * quantity
    
    # 4. บันทึกลงตาราง (สร้าง ORDER ก่อน แล้วค่อยสร้าง TOTAL_ORDER)
    # ใส่ customer_no เป็น 101 ไปก่อนตามตัวอย่าง
    cursor.execute("INSERT INTO `ORDER` (order_no, customer_no) VALUES (?, ?)", (None, 101))
    order_id = cursor.lastrowid # ดึงเลข ID ล่าสุดที่เพิ่ง Auto Increment มา
    
    cursor.execute("INSERT INTO TOTAL_ORDER VALUES (?, ?, ?, ?)", 
                   (order_id, menu_name, quantity, subtotal))
    
    conn.commit()
    conn.close()
    
    # สั่งเสร็จให้เด้งกลับไปหน้าแรกเพื่อดูรายการที่เพิ่งสั่ง
    return redirect(url_for('index'))

# บรรทัดนี้ต้องอยู่ล่างสุดเสมอ!
if __name__ == '__main__':
    app.run(debug=True)