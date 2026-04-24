💡 วิธีใช้งาน (How to use)
สำหรับ AI (ChatGPT/Claude/Gemini):

ก่อนจะให้มันเขียนโค้ดฟีเจอร์ใหม่ ให้ Paste ข้อความข้างบนนี้ลงไปก่อน

บอกว่า "นี่คือบริบทโปรเจคของฉัน ช่วยจำไว้หน่อย"

จากนั้นค่อยสั่งงาน เช่น "ช่วยเขียน Code สำหรับฟีเจอร์ Log in โดยยึดตามโครงสร้างตามนี้"

### 1. Project Overview (ภาพรวม)
* **Project Name:** Pizza Fast-Food POS (KFC Model)
* **Goal:** ระบบแคชเชียร์รับออเดอร์หน้าร้านสไตล์ฟาสต์ฟู้ด เน้นความรวดเร็วในการรับออเดอร์ คำนวณเงิน และออกหมายเลขคิว (Queue Number)
* **Key Features (In-Scope):**
    * พนักงานดูเมนูและกดเลือกอาหารลงตะกร้า
    * ระบบคำนวณราคารวม (Total Price)
    * ระบบจำลองการรับชำระเงิน
    * ออกหมายเลขคิวและบันทึกออเดอร์

### 2. Tech Stack (เครื่องมือที่ใช้)
* **Backend:** Python, Flask
* **Database:** SQLite
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS)
* **Deployment & Infrastructure:** รันบนเครื่อง Localhost (เซ็ตอัปง่าย ไม่ซับซ้อน)

### 3. Project Structure (โครงสร้างไฟล์)

```text
PIZZYPIZZA/
│
├── static/                # เก็บไฟล์ Static (ฝั่ง Frontend)
│   ├── css/
│   │   ├── log_in.css
│   │   ├── manager.css
│   │   └── user.css
│   └── js/
│       ├── log_in.js
│       ├── manager.js
│       └── user.js
│
├── templates/             # เก็บไฟล์หน้าจอ HTML
│   ├── log_in.html
│   ├── manager.html
│   └── user.html          
│
├── app.py                 # (Backend) ไฟล์หลักจัดการ Routing รับ-ส่งข้อมูลกับ Frontend
├── models.py              # (Backend) ไฟล์รวมฟังก์ชันจัดการ SQL (ดึง/บันทึก/อัปเดตข้อมูล)
├── init_db.py             # (Backend) สคริปต์รันสร้างตารางฐานข้อมูลและตั้งค่าเริ่มต้น
├── restaurant.db          # ไฟล์ฐานข้อมูล SQLite (จะถูกสร้างเมื่อรัน init_db.py)
│
├── requirements.txt       # รายชื่อ Library ที่จำเป็น (เช่น flask)
├── Document_project.md    # ไฟล์เอกสารของโปรเจค
└── project_prompt.md      # ไฟล์ contex project สำหรับให้ AI อ่าน
```

### 4. Database Schema (ข้อมูลหลัก)
*อ้างอิงจากโค้ด SQLite ที่กำหนด*

* **Table: MANAGER (เก็บข้อมูลผู้ดูแลระบบ/แคชเชียร์)**
    * `manager_id` (PK, int): รหัสผู้จัดการ
    * `user_name` (text): ชื่อผู้ใช้งาน
    * `password` (text): รหัสผ่าน
* **Table: MENU (เก็บรายการอาหาร)**
    * `menu_id` (PK, text): รหัสเมนูอาหาร (เช่น PZ01)
    * `menu_name` (text): ชื่อเมนูอาหาร
    * `price` (int): ราคา
* **Table: MENU_QUANTITY (เก็บรายการอาหารที่ถูกสั่งในแต่ละออเดอร์/คิว)**
    * `QNumber` (PK, int): ลำดับรายการอาหารที่สั่ง
    * `order_no` (int): หมายเลขบิล หรือ หมายเลขคิว (Queue Number)
    * `menu_id` (int, FK): รหัสเมนูอาหาร (อ้างอิงจากตาราง MENU)
    * `quantity` (int): จำนวนที่สั่ง
    * `subtotal` (int): ราคารวมของเมนูนั้น (price * quantity)
* **Table: MANAGER_LOGS (เก็บประวัติการทำงานหรือการเปลี่ยนแปลงระบบ)**
    * `log_id` (PK, int): รหัสบันทึกประวัติ
    * `manager_id` (int, FK): รหัสผู้จัดการที่ทำรายการ (อ้างอิงจากตาราง MANAGER)
    * `action_type` (text): ประเภทการกระทำ (เช่น CREATE, UPDATE, DELETE)
    * `table_name` (text): ชื่อตารางที่มีการเปลี่ยนแปลง
    * `old_value` (text): ค่าข้อมูลเดิม
    * `new_value` (text): ค่าข้อมูลใหม่

### 5. Workflow ตัวอย่าง (ขั้นตอนการทำงานจริงของแคชเชียร์)
**(โมเดลฟาสต์ฟู้ด: สั่ง จ่าย ออกคิว จบ)**

1. **ขั้นตอนการเข้าสู่ระบบ (Login)**
   * พนักงานแคชเชียร์เข้าสู่ระบบด้วย `user_name` และ `password` (ตรวจสอบจากตาราง `MANAGER`)
2. **ขั้นตอนการรับออเดอร์ (Ordering)**
   * ลูกค้าเดินมาที่หน้าเคาน์เตอร์และสั่งอาหาร
   * แคชเชียร์กดเลือกเมนูบนหน้าจอ `pos.html` เข้าตะกร้า (เลือกจำนวน, เพิ่ม/ลดรายการ)
   * JavaScript บนหน้าเว็บคำนวณยอดเงินรวมให้เห็นแบบ Real-time
3. **ขั้นตอนการชำระเงิน (Payment)**
   * เมื่อลูกค้าสั่งครบ แคชเชียร์แจ้งยอดรวม
   * แคชเชียร์กดปุ่ม "ชำระเงิน" (ในระบบถือเป็นการจำลองว่ารับเงินเรียบร้อยแล้ว)
4. **ขั้นตอนการออกคิว (Generate Queue)**
   * Frontend ยิงข้อมูลตะกร้าไปที่ Flask Backend
   * Flask ทำการบันทึกข้อมูลลงตาราง `MENU_QUANTITY` โดยอ้างอิงหมายเลข `order_no` เดียวกันสำหรับรายการอาหารในบิลนั้น
   * หน้าจอแคชเชียร์แสดงหมายเลขคิว (`order_no`) ให้ลูกค้าทราบ ถือว่าเสร็จสิ้นกระบวนการออเดอร์