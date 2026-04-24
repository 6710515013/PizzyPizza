from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = sqlite3.Row # ช่วยให้เรียกข้อมูลด้วยชื่อคอลัมน์ได้ เช่น row['menu_name']
    return conn

# หน้าแสดงผล POS สำหรับแคชเชียร์
@app.route('/')
def index():
    conn = get_db_connection()
    
    # 1. ดึงรายการเมนูทั้งหมดมาโชว์เพื่อให้แคชเชียร์เลือก
    menus = conn.execute('SELECT * FROM menu').fetchall()
    
    # 2. ดึงรายการสั่งซื้อล่าสุด (Join กับตาราง menu เพื่อเอาชื่อเมนูมาแสดง)
    # เราจะแสดงรายการจาก menu_quantity และเรียงตามลำดับคิวล่าสุดขึ้นก่อน
    orders = conn.execute('''
        SELECT mq.order_no, m.menu_name, mq.quantity, mq.subtotal 
        FROM menu_quantity mq 
        JOIN menu m ON mq.menu_id = m.menu_id
        ORDER BY mq.qnumber DESC
    ''').fetchall()
    
    conn.close()
    return render_template('user.html', menus=menus, orders=orders)

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

if __name__ == '__main__':
    app.run(debug=True)