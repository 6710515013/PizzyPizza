# app.py
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    # ดึงข้อมูลมาโชว์ในหน้า user.html
    orders = conn.execute('SELECT * FROM TOTAL_ORDER').fetchall()
    conn.close()
    # เปลี่ยนชื่อไฟล์ html ให้ตรงกับที่คุณมีในโฟลเดอร์ templates
    return render_template('user.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)