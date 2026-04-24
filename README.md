# 🍕 PIZZYPIZZA POS System (KFC Model)

## 🚀 การติดตั้งโปรเจคสำหรับทีม (First-time Setup)

ทำตามขั้นตอนด้านล่างนี้เพื่อตั้งค่าโปรเจคในเครื่องของคุณเป็นครั้งแรก

### 1. Clone โปรเจคลงเครื่อง
เปิด Terminal (หรือ Git Bash / WSL) แล้วรันคำสั่ง:
```bash
git clone <ใส่-URL-ของ-Repository-ที่นี่>
cd PizzyPizza
```

### 2. สร้างและเปิดใช้งาน Virtual Environment
เพื่อป้องกันไม่ให้ Library ของโปรเจคนี้ไปตีกับโปรเจคอื่นในเครื่อง ให้สร้างจำลองสภาพแวดล้อมขึ้นมา (สังเกตว่าจะมีโฟลเดอร์ `.venv` ปรากฏขึ้นมา)

**สร้าง Virtual Environment:**
```bash
python -m venv .venv
```

**เปิดใช้งาน (Activate) Virtual Environment:**
* **สำหรับ Windows (Command Prompt / PowerShell):**
  ```cmd
  .\.venv\Scripts\activate
  ```
* **สำหรับ Mac / Linux / WSL:**
  ```bash
  source .venv/bin/activate
  ```
*(ถ้าทำสำเร็จ จะมีคำว่า `(.venv)` ปรากฏอยู่ข้างหน้าชื่อผู้ใช้ใน Terminal)*

### 3. ติดตั้ง Library ที่จำเป็น
เมื่อ Activate แล้ว ให้ติดตั้ง Flask และเครื่องมืออื่นๆ ที่ระบุไว้ใน `requirements.txt`
```bash
pip install -r requirements.txt
```

### 4. สร้างฐานข้อมูล (Database Initialization)
รันคำสั่งนี้ **แค่ครั้งแรกครั้งเดียว** เพื่อสร้างไฟล์ `restaurant.db` และตารางข้อมูลต่างๆ
ติดตั้ง Extension SQLite Viewer เพื่อที่จะสามารถเปิดไฟล์ restaurant.db และดูข้อมูลใน Database
```bash
python init_db.py
```

### 5. รันเซิร์ฟเวอร์
เริ่มการทำงานของเซิร์ฟเวอร์ Flask:
```bash
python app.py
```
เปิดเบราว์เซอร์แล้วเข้าไปที่ `http://127.0.0.1:5000` เพื่อดูผลลัพธ์

---

## 🛠️ ปัญหาที่พบบ่อย (Common Issues)

### ❌ 1. รันรันเซิร์ฟเวอร์แล้วขึ้น `ModuleNotFoundError: No module named 'flask'`
* **สาเหตุ:** ลืมเปิดใช้งาน Virtual Environment หรือลืมรันคำสั่งติดตั้ง requirements
* **วิธีแก้:** เช็คให้แน่ใจว่ามี `(.venv)` อยู่หน้า Terminal ถ้าไม่มีให้รันคำสั่ง Activate (ดูข้อ 2) แล้วรัน `pip install -r requirements.txt` ใหม่อีกครั้ง
