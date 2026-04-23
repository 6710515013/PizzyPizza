PizzyPizza
├── venv/                 
# Virtual Environment (สภาพแวดล้อมแยก)
# ใช้เก็บ library ที่โปรเจกต์นี้ใช้เท่านั้น เช่น Flask
# ช่วยป้องกัน library ชนกับโปรเจกต์อื่น
# ❌ ห้ามแก้ไขไฟล์ข้างในเอง

├── static/               
# เก็บไฟล์ static เช่น
# - รูปภาพ (pizza.jpg)
# - CSS (style.css)
# - JavaScript (script.js)
# ใช้สำหรับตกแต่งหน้าเว็บ

├── templates/            
# เก็บไฟล์ HTML (โครงสร้างหน้าเว็บ)
# ใช้ร่วมกับ :contentReference[oaicite:0]{index=0}

│   ├── index.html
# หน้าแรกของเว็บ (Home page)

│   └── menu.html
# หน้าแสดงเมนูพิซซ่า

├── app.py                
# ไฟล์หลักของโปรแกรม
# ใช้รันเว็บเซิร์ฟเวอร์
# และกำหนด route เช่น / , /menu

├── models.py             
# ใช้สร้างโครงสร้างฐานข้อมูล (Database)
# เช่น ตาราง Pizza, Order
# มักใช้ร่วมกับ ORM เช่น :contentReference[oaicite:1]{index=1}

├── .env                 
# เก็บค่าลับ เช่น
# - password database
# - secret key
# ❌ ห้ามอัปขึ้น Git (ต้องใส่ใน .gitignore)

└── requirements.txt      
# รายการ library ที่ใช้ในโปรเจกต์
# เช่น Flask==3.0.0
# ใช้สำหรับติดตั้งด้วยคำสั่ง:
# pip install -r requirements.txt