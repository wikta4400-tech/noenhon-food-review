import streamlit as st

st.set_page_config(page_title="รีวิวร้านอาหารปราจีนบุรี", layout="centered")

# -------------------------------
# 🔐 ระบบผู้ใช้ (จำลอง)
# -------------------------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234", "user01": "pass"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
# -------------------------------
# 🆕 เพิ่ม: ประวัติการค้นหา
# -------------------------------
if "search_history" not in st.session_state:
    st.session_state.search_history = []
# -------------------------------
# 🆕 เพิ่ม: รายการร้านที่ถูกใจ
# -------------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = {} # {username: set_of_restaurant_names}
# -------------------------------
# 🆕 เพิ่ม: ตัวแปรสำหรับสลับหน้า (เพื่อให้การกดใจไม่หายไปเมื่อกดปุ่มย้อนกลับ)
# -------------------------------
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "all" # 'all' หรือ 'favorites'
# -------------------------------
# 🆕 เพิ่ม: ตัวแปรสำหรับช่องค้นหา (ใช้เป็น key ของ st.text_input)
# -------------------------------
if "search_input_key" not in st.session_state:
    st.session_state.search_input_key = ""


# ----------------------------------------------------------------------------------
# ❗ ฟังก์ชันสำหรับตั้งค่าคำค้นหาจากปุ่ม (แก้ไข: ตั้งค่า st.session_state.search_input_key โดยตรง)
# ----------------------------------------------------------------------------------
def set_search_from_button(query):
    """ตั้งค่า st.session_state.search_input_key จากปุ่มเคลียร์ค้นหา และสั่ง Rerun"""
    # 1. ตั้งค่าช่องค้นหาด้วยค่าที่ถูกรีเซ็ต สำหรับใช้ในรอบถัดไป
    st.session_state.search_input_key = query 
    
    # 2. บันทึกคำค้นหาลงในประวัติ (ถ้าไม่ใช่ค่าว่าง)
    query_to_save = query.strip()
    if query_to_save and query_to_save not in st.session_state.search_history:
        st.session_state.search_history.insert(0, query_to_save)
        st.session_state.search_history = st.session_state.search_history[:5]
        
    # 3. สั่ง Rerun เพื่อให้ค่าใหม่ปรากฏในช่องค้นหา
    st.rerun()

# ----------------------------------------------------------------------------------
# ❗ ฟังก์ชันสำหรับล้างค่าช่องค้นหาทั้งหมด
# ----------------------------------------------------------------------------------
def reset_search():
    """ฟังก์ชันสำหรับตั้งค่า Search เป็นค่าว่าง, ตั้ง View Mode เป็น 'all' และสั่ง rerun"""
    st.session_state.view_mode = "all"
    # ใช้ set_search_from_button เพื่อเคลียร์ค่าในช่องค้นหาและเรียก rerun
    set_search_from_button("") 

# ----------------------------------------------------------------------------------
# ❗ ฟังก์ชันสำหรับสลับไปหน้า Favorites
# ----------------------------------------------------------------------------------
def switch_to_favorites():
    st.session_state.view_mode = "favorites"
    st.session_state.search_input_key = "" # เคลียร์ช่องค้นหาเมื่อเปลี่ยนโหมด
    st.rerun()


# ----------------------------------------------------------------------------------
# ❗ ฟังก์ชันสลับการกดใจ
# ----------------------------------------------------------------------------------
def toggle_favorite(restaurant_name):
    """เพิ่ม/ลบ ร้านจากรายการที่ถูกใจของผู้ใช้ปัจจุบัน"""
    current_user = st.session_state.current_user
    
    if current_user not in st.session_state.favorites:
        st.session_state.favorites[current_user] = set()
        
    user_favorites = st.session_state.favorites[current_user]

    if restaurant_name in user_favorites:
        user_favorites.remove(restaurant_name)
        st.toast(f"💔 ลบ '{restaurant_name}' ออกจากร้านที่ถูกใจแล้ว", icon="💔")
    else:
        user_favorites.add(restaurant_name)
        st.toast(f"❤️ เพิ่ม '{restaurant_name}' ในร้านที่ถูกใจแล้ว!", icon="❤️")
    
    st.rerun() 


# -------------------------------
# 🧾 หน้าเข้าสู่ระบบ / สมัครสมาชิก
# -------------------------------
if not st.session_state.logged_in:
    st.title("🔐 เข้าสู่ระบบ / สมัครสมาชิก")
    tab1, tab2 = st.tabs(["เข้าสู่ระบบ", "สมัครสมาชิก"])

    with tab1:
        username = st.text_input("ชื่อผู้ใช้", key="login_user")
        password = st.text_input("รหัสผ่าน", type="password", key="login_pass")
        if st.button("เข้าสู่ระบบ"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.session_state.view_mode = "all" 
                st.success(f"ยินดีต้อนรับ {username} ✅")
                st.rerun()
            else:
                st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    with tab2:
        new_user = st.text_input("ชื่อผู้ใช้ใหม่", key="reg_user")
        new_pass = st.text_input("รหัสผ่านใหม่", type="password", key="reg_pass")
        if st.button("สมัครสมาชิก"):
            if new_user in st.session_state.users:
                st.warning("ชื่อผู้ใช้นี้มีอยู่แล้ว")
            elif new_user and new_pass:
                st.session_state.users[new_user] = new_pass
                st.session_state.logged_in = True 
                st.session_state.current_user = new_user
                st.session_state.view_mode = "all"
                st.success("สมัครสมาชิกสำเร็จ! เข้าสู่ระบบแล้ว ✅")
                st.rerun()
            else:
                st.error("กรุณากรอกข้อมูลให้ครบ")
    st.stop()

# -------------------------------
# 🔓 ปุ่มออกจากระบบ
# -------------------------------
with st.sidebar:
    st.write(f"👤 ผู้ใช้งาน: **{st.session_state.current_user}**")
    if st.button("ออกจากระบบ"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.rerun()

# -------------------------------
# 📦 ข้อมูลร้านอาหาร
# -------------------------------
if "reviews" not in st.session_state:
    st.session_state.reviews = []
    
restaurants = [
    {"ชื่อร้าน": "ครัวอากู๋ กบินทร์บุรี", "ประเภท": "อาหารไทย / ซีฟู้ด", "ราคา": "฿250–450", "เบอร์ติดต่อ": "081-123-4567", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.550!3d13.980!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0xc3f0b0e51323c21a!2z4Lir4Liy4Lij4Lix4Lix4Lin4Lij4Liy4LiZ4Lij4Lio4Liy4Lij4LmM4LiB4Lij4LmM!5e0!3m2!1sth!2sth!4v1700000001"},
    {"ชื่อร้าน": "Tas Lit", "ประเภท": "อาหารฟิวชั่น / Homemade", "ราคา": "฿150–350", "เบอร์ติดต่อ": "**097-289-7735**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.480!3d14.050!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0xabcdef123456789!2sTas+Lit+Restaurant!5e0!3m2!1sth!2sth!4v1700000002"},
    {"ชื่อร้าน": "Cafe Kantary ปราจีนบุรี", "ประเภท": "เบเกอรี่ & คาเฟ่", "ราคา": "฿90–200", "เบอร์ติดต่อ": "**037-239-777**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.350!3d14.120!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x28c0c4e72c84210a!2sCafe+Kantary+Prachinburi!5e0!3m2!1sth!2sth!4v1700000003"},
    {"ชื่อร้าน": "ก๋วยเตี๋ยวกากหมูลานบริบูรณ์", "ประเภท": "ก๋วยเตี๋ยว / อาหารท้องถิ่น", "ราคา": "฿50–100", "เบอร์ติดต่อ": "**089-995-8359**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.290!3d14.150!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x1d4a04d16d1d4d1a!2sKuay+Tiew+Kak+Mu!5e0!3m2!1sth!2sth!4v1700000004"},
    {"ชื่อร้าน": "ซินจ่าว2 อาหารไทย-เวียตนาม", "ประเภท": "ไทย & เวียดนาม", "ราคา": "฿100–250", "เบอร์ติดต่อ": "086-567-8901", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.190!3d14.170!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x633190823c91a32a!2sXin+Chao+2!5e0!3m2!1sth!2sth!4v1700000005"},
    {"ชื่อร้าน": "Bloom Restaurant @ Siamdasada Khaoyai", "ประเภท": "อาหารฟิวชั่น / อาหารไทย", "ราคา": "฿300–600", "เบอร์ติดต่อ": "**037-216-800**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.180!3d14.160!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311d0442e3919b51%3A0x33481216893f41e9!2sBloom+Restaurant!5e0!3m2!1sth!2sth!4v1700000006"},
    {"ชื่อร้าน": "บ้านปัณณ์ สเต็ก คาเฟ่ บาร์", "ประเภท": "สเต๊ก / คาเฟ่ / ฟิวชั่น", "ราคา": "฿150–350", "เบอร์ติดต่อ": "087-789-0123", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.310!3d14.090!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37803e7c859d%3A0x62804f326a2490b6!2z4Lir4Liy4LiZ4LmM4Liy4LiE4Lij4Lij!5e0!3m2!1sth!2sth!4v1700000007"},
    {"ชื่อร้าน": "ก๋วยเตี๋ยวเรือนายติณณ์", "ประเภท": "ก๋วยเตี๋ยว / อาหารท้องถิ่น", "ราคา": "฿50–100", "เบอร์ติดต่อ": "**096-618-5163**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.450!3d14.070!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37b12d1b5a59%3A0x868b1a8d46a89c9c!2z4LiZ4Liy4Lih4Liy4LiE4Lir4Lin4LiV4LiU4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000008"},
    {"ชื่อร้าน": "ก๋วยเตี๋ยวเป็ดป้าสาลี่", "ประเภท": "ก๋วยเตี๋ยว / เป็ดพะโล้", "ราคา": "฿60–120", "เบอร์ติดต่อ": "**087-148-3461**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.370!3d14.070!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x8899aabbccddeeff!2z4Lia4Liy4LiL4LiK4Liy4Lin!5e0!3m2!1sth!2sth!4v1700000009"},
    {"ชื่อร้าน": "อีสานเฮาส์ 304", "ประเภท": "อาหารอีสาน / จิ้มจุ่ม", "ราคา": "฿150–300", "เบอร์ติดต่อ": "081-012-3456", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.520!3d14.030!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x66778899aabbccdd!2z4LiI4LiB4Liy4LiV4LiU4LmI!5e0!3m2!1sth!2sth!4v1700000010"},
    {"ชื่อร้าน": "ครัวคุณกุ้ง", "ประเภท": "อาหารไทย / ท่องเที่ยว", "ราคา": "฿200–400", "เบอร์ติดต่อ": "089-123-4560", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.400!3d14.100!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x1122334455667788!2z4Lir4Liy4LiB4LiZ4LmM4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000011"},
    {"ชื่อร้าน": "Myrrh Cafe (มายร์ คาเฟ่)", "ประเภท": "คาเฟ่ / กาแฟ / วิวเขา", "ราคา": "฿80–180", "เบอร์ติดต่อ": "**089-887-8125**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.430!3d14.140!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x9900aa11bb22cc33!2sMyrrh+Cafe!5e0!3m2!1sth!2sth!4v1700000012"},
    {"ชื่อร้าน": "โก๋มุ่ยบะหมี่เกี๊ยว", "ประเภท": "บะหมี่ / อาหารจีนท้องถิ่น", "ราคา": "฿50–100", "เบอร์ติดต่อ": "065-345-6780", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.200!3d14.180!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x445566778899aabb!2z4Lir4Liw4LiH4LmM4Liy4LiZ!5e0!3m2!1sth!2sth!4v1700000013"},
    {"ชื่อร้าน": "ร้านอาหารบ้านสวน (กบินทร์บุรี)", "ประเภท": "อาหารไทย / บรรยากาศสวน", "ราคา": "฿180–350", "เบอร์ติดต่อ": "086-456-7890", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.600!3d13.900!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0xccddff9988776655!2z4Lir4Liy4Lij4Lix4Lix4Lin!5e0!3m2!1sth!2sth!4v1700000014"},
    {"ชื่อร้าน": "ก๋วยเตี๋ยวเรือปากซอย", "ประเภท": "ก๋วยเตี๋ยวเรือ", "ราคา": "฿50–90", "เบอร์ติดต่อ": "**037-214-468**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.320!3d14.080!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x2211443366558877!2z4LiZ4Liy4Lih4Liy4LiE4Lir4LiL4LiK!5e0!3m2!1sth!2sth!4v1700000015"},
    {"ชื่อร้าน": "The Forest Cafe", "ประเภท": "คาเฟ่ / ฟิวชั่น / อาหารไทย", "ราคา": "฿100–300", "เบอร์ติดต่อ": "**094-197-6598**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.390!3d14.110!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x55aa66bb77cc88dd!2sThe+Forest+Cafe!5e0!3m2!1sth!2sth!4v1700000016"},
    {"ชื่อร้าน": "ครัวบ้านเรา", "ประเภท": "อาหารไทย / ซีฟู้ด", "ราคา": "฿200–400", "เบอร์ติดต่อ": "064-789-0120", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.380!3d14.050!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0xaa11bb22cc33dd44!2z4Lir4Liy4LiB4Lix4LiZ4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000017"},
    {"ชื่อร้าน": "ร้านกาแฟบ้านริมน้ำ", "ประเภท": "คาเฟ่ / ริมน้ำ", "ราคา": "฿80–180", "เบอร์ติดต่อ": "090-890-1230", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.355!3d14.040!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0xee55ff66aa77bb88!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000018"},
    {"ชื่อร้าน": "ภูผาผัก", "ประเภท": "สลัด / สุขภาพ / ฟาร์ม", "ราคา": "฿120–300", "เบอร์ติดต่อ": "081-901-2340", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.500!3d14.150!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0xcc99aa00ff11ee22!2z4Lir4Liy4LiZ4LmM4Liy4Lih4Liy4LiZ4LmM4Liy4LiK!5e0!3m2!1sth!2sth!4v1700000019"},
    {"ชื่อร้าน": "ครัวบ้านนา", "ประเภท": "อาหารไทยพื้นบ้าน", "ราคา": "฿150–350", "เบอร์ติดต่อ": "089-012-3450", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.420!3d14.100!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0xbb22cc33dd44ee55!2z4Lir4Liy4LiB4Lix4LiZ4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000020"},
    {"ชื่อร้าน": "ก๋วยเตี๋ยวเนื้อโคขุน", "ประเภท": "ก๋วยเตี๋ยวเนื้อ", "ราคา": "฿70–150", "เบอร์ติดต่อ": "**087-966-4262**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.560!3d13.970!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x1122334455667788!2z4LiZ4Liy4Lih4Liy4LiE4Lir4LiV4LiU4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000021"},
    {"ชื่อร้าน": "บ้านไม้ชายคลอง", "ประเภท": "อาหารไทย / บรรยากาศดี", "ราคา": "฿250–450", "เบอร์ติดต่อ": "065-234-5670", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.340!3d14.060!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0xaa55bb66cc77dd88!2z4Lir4Liy4LiZ4LmM4Liy4LiE4Lij4Lij!5e0!3m2!1sth!2sth!4v1700000022"},
    {"ชื่อร้าน": "คิงคองคาเฟ่", "ประเภท": "คาเฟ่ / ของหวาน", "ราคา": "฿90–200", "เบอร์ติดต่อ": "086-345-6780", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.315!3d14.055!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x99ddff00cc22ee33!2z4Lir4Liy4LiZ4LmM4Liy4LiK!5e0!3m2!1sth!2sth!4v1700000023"},
    {"ชื่อร้าน": "เจ๊นิด กุ้งเผา", "ประเภท": "กุ้งเผา / ซีฟู้ด", "ราคา": "฿300–700", "เบอร์ติดต่อ": "091-456-7890", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.330!3d14.075!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x66ffaa00bb11cc22!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000024"},
    {"ชื่อร้าน": "ร้านอาหารบ้านสวนริมน้ำ", "ประเภท": "อาหารไทย / ริมน้ำ", "ราคา": "฿200–450", "เบอร์ติดต่อ": "087-567-8900", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.365!3d14.055!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0xdd33ff44ee55aa66!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000025"},
    {"ชื่อร้าน": "ครัวปราจีน", "ประเภท": "อาหารไทย / อาหารป่า", "ราคา": "฿250–500", "เบอร์ติดต่อ": "064-678-9010", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.300!3d14.085!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0xaa66bb77cc88dd99!2z4Lir4Liy4LiB4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000026"},
    {"ชื่อร้าน": "ก๋วยจั๊บญวนคุณยาย", "ประเภท": "ก๋วยจั๊บ / อาหารเวียดนาม", "ราคา": "฿60–120", "เบอร์ติดต่อ": "**095-216-6292**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.385!3d14.120!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x2299aa00bb11cc33!2z4LiZ4Liy4Lih4Liy4LiE4Lir4Lin4LiV4LiU4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000027"},
    {"ชื่อร้าน": "มุมอร่อย", "ประเภท": "อาหารตามสั่ง / จานเดียว", "ราคา": "฿50–100", "เบอร์ติดต่อ": "081-890-1230", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.350!3d14.070!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x77aa88bb99cc00dd!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000028"},
    {"ชื่อร้าน": "Coffee Corner by 304", "ประเภท": "คาเฟ่ / กาแฟ / เบเกอรี่", "ราคา": "฿80–180", "เบอร์ติดต่อ": "080-837-9696", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.530!3d14.040!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x11cc22dd33ee44ff!2sCoffee+Corner+304!5e0!3m2!1sth!2sth!4v1700000029"},
    {"ชื่อร้าน": "ส้มตำติดปาก", "ประเภท": "ส้มตำ / อาหารอีสาน", "ราคา": "฿100–250", "เบอร์ติดต่อ": "098-012-3450", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.295!3d14.095!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x55ffaa66bb77cc88!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000030"},
    {"ชื่อร้าน": "ร้านข้าวต้มกุ๊ยนายพล", "ประเภท": "ข้าวต้ม / อาหารไทย", "ราคา": "฿100–300", "เบอร์ติดต่อ": "065-123-4560", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.410!3d14.080!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0xbb88cc99dd00ee11!2z4Lir4Liy4LiB4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000031"},
    {"ชื่อร้าน": "เรือนไทยอาหารไทย", "ประเภท": "อาหารไทยโบราณ / บรรยากาศ", "ราคา": "฿300–600", "เบอร์ติดต่อ": "086-234-5670", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.325!3d14.105!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0xdd55ff66aa77bb88!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000032"},
    {"ชื่อร้าน": "ร้านป้าแมวข้าวแกง", "ประเภท": "อาหารตามสั่ง / แกงใต้", "ราคา": "฿40–80", "เบอร์ติดต่อ": "091-345-6780", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.330!3d14.110!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x1122334455667788!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000033"},
    {"ชื่อร้าน": "ฟาร์มสุข คาเฟ่", "ประเภท": "คาเฟ่ / ฟาร์ม / ธรรมชาติ", "ราคา": "฿90–200", "เบอร์ติดต่อ": "087-456-7890", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.550!3d14.050!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x2233445566778899!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000034"},
    {"ชื่อร้าน": "ก๋วยเตี๋ยวต้มยำโบราณ", "ประเภท": "ก๋วยเตี๋ยว / ต้มยำ", "ราคา": "฿50–100", "เบอร์ติดต่อ": "**083-419-4411**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.380!3d14.080!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x3344556677889900!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000035"},
    {"ชื่อร้าน": "ครัวร่มไม้ไพรวัลย์", "ประเภท": "อาหารป่า / ริมธาร", "ราคา": "฿300–550", "เบอร์ติดต่อ": "090-678-9010", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.290!3d14.120!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x4455667788990011!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000036"},
    {"ชื่อร้าน": "สเต็กลุงหนวด (ปราจีน)", "ประเภท": "สเต๊ก / อาหารฝรั่ง", "ราคา": "฿120–280", "เบอร์ติดต่อ": "081-789-0120", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.400!3d14.070!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x5566778899001122!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000037"},
    {"ชื่อร้าน": "ขนมจีนเจ๊เล็ก", "ประเภท": "ขนมจีน / แกงเขียวหวาน", "ราคา": "฿45–90", "เบอร์ติดต่อ": "**089-134-8757**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.350!3d14.090!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x6677889900112233!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000038"},
    {"ชื่อร้าน": "บ้านไร่ปลายนา", "ประเภท": "อาหารไทย / บรรยากาศทุ่งนา", "ราคา": "฿150–350", "เบอร์ติดต่อ": "098-901-2340", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.450!3d14.130!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x7788990011223344!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000039"},
    {"ชื่อร้าน": "โรตีมัตตาบะ (หน้าสถานี)", "ประเภท": "ของหวาน / โรตี / ชาชัก", "ราคา": "฿30–70", "เบอร์ติดต่อ": "065-012-3450", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.360!3d14.060!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x8899001122334455!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000040"},
    {"ชื่อร้าน": "พิซซ่าเตาถ่านกบินทร์", "ประเภท": "พิซซ่า / อิตาเลียน", "ราคา": "฿180–400", "เบอร์ติดต่อ": "086-123-4560", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.580!3d13.950!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x9900112233445566!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000041"},
    {"ชื่อร้าน": "เจ๊อ้วนอาหารทะเล", "ประเภท": "ซีฟู้ด / เผาอบ", "ราคา": "฿350–750", "เบอร์ติดต่อ": "091-234-5670", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.310!3d14.050!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x0011223344556677!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000042"},
    {"ชื่อร้าน": "ร้านต้มเลือดหมูเฮีย", "ประเภท": "ต้มเลือดหมู / อาหารเช้า", "ราคา": "฿50–100", "เบอร์ติดต่อ": "087-345-6780", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.340!3d14.080!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x1122334455667788!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000043"},
    {"ชื่อร้าน": "กาแฟดริป (เขาใหญ่)", "ประเภท": "คาเฟ่ / กาแฟเฉพาะทาง", "ราคา": "฿100–220", "เบอร์ติดต่อ": "064-456-7890", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.200!3d14.150!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x2233445566778899!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000044"},
    {"ชื่อร้าน": "ครัวปลาเผาปราจีน", "ประเภท": "ปลาเผา / อาหารอีสาน", "ราคา": "฿200–400", "เบอร์ติดต่อ": "090-567-8900", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.480!3d14.070!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x3344556677889900!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000045"},
    {"ชื่อร้าน": "หอยทอดเจ๊แดง", "ประเภท": "หอยทอด / ผัดไท", "ราคา": "฿60–120", "เบอร์ติดต่อ": "081-678-9010", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.370!3d14.040!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x4455667788990011!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000046"},
    {"ชื่อร้าน": "ร้านขนมไทยคุณย่า", "ประเภท": "ขนมไทย / น้ำกะทิ", "ราคา": "฿40–80", "เบอร์ติดต่อ": "089-789-0120", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.355!3d14.075!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x5566778899001122!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000047"},
    {"ชื่อร้าน": "หมูกระทะอินเตอร์", "ประเภท": "หมูกระทะ / บุฟเฟ่ต์", "ราคา": "฿199–399", "เบอร์ติดต่อ": "098-890-1230", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.420!3d14.050!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x6677889900112233!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000048"},
    {"ชื่อร้าน": "ข้าวมันไก่ตอนฮกเกี้ยน", "ประเภท": "ข้าวมันไก่ / อาหารจีน", "ราคา": "฿60–120", "เบอร์ติดต่อ": "**037-216-919**", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.345!3d14.095!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x7788990011223344!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000049"},
    {"ชื่อร้าน": "ร้านส้มตำปูปลาร้าแซ่บ", "ประเภท": "ส้มตำ / ลาบ", "ราคา": "฿80–200", "เบอร์ติดต่อ": "086-012-3450", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.405!3d14.075!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x8899001122334455!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000050"},
    {"ชื่อร้าน": "บะหมี่เกี๊ยวน้ำแดง", "ประเภท": "บะหมี่ / เกี๊ยว", "ราคา": "฿50–100", "เบอร์ติดต่อ": "091-123-4560", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.320!3d14.065!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x9900112233445566!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000051"},
    {"ชื่อร้าน": "ลาบเป็ดอุดร", "ประเภท": "อาหารอีสาน / เป็ด", "ราคา": "฿150–300", "เบอร์ติดต่อ": "087-234-5670", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.500!3d14.030!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x0011223344556677!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000052"},
    {"ชื่อร้าน": "The View Bar & Bistro", "ประเภท": "ผับ & บิสโทร / วิวสวย", "ราคา": "฿350–800", "เบอร์ติดต่อ": "064-345-6780", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.290!3d14.100!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x1122334455667788!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000053"},
    {"ชื่อร้าน": "ข้าวซอยแม่คำ", "ประเภท": "ข้าวซอย / อาหารเหนือ", "ราคา": "฿60–120", "เบอร์ติดต่อ": "090-456-7890", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.430!3d14.110!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x2233445566778899!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000054"},
    {"ชื่อร้าน": "ครัวสวนอาหารป่า", "ประเภท": "อาหารป่า / แกงส้ม", "ราคา": "฿250–500", "เบอร์ติดต่อ": "081-567-8900", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.380!3d14.130!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x3344556677889900!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000055"},
    {"ชื่อร้าน": "ข้าวหมูแดงเจริญ", "ประเภท": "ข้าวหมูแดง / หมูกรอบ", "ราคา": "฿50–100", "เบอร์ติดต่อ": "089-678-9010", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.350!3d14.030!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x4455667788990011!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000056"},
    {"ชื่อร้าน": "ชาบูอินดี้", "ประเภท": "ชาบู / สุกี้", "ราคา": "฿250–450", "เบอร์ติดต่อ": "098-789-0120", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.400!3d14.040!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x5566778899001122!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000057"},
    {"ชื่อร้าน": "เบเกอรี่โฮมเมด", "ประเภท": "เค้ก / ขนมปัง / คาเฟ่", "ราคา": "฿70–150", "เบอร์ติดต่อ": "065-890-1230", "แผนที่": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3875.123!2d101.300!3d14.070!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x311a37a6b99d45e5%3A0x6677889900112233!2z4Lir4Liy4Lij4Lix4Lia4Liy4LiH4LmA4LiK4Liy4Lii!5e0!3m2!1sth!2sth!4v1700000058"}
]


# -------------------------------
# 🔍 ช่องค้นหาร้าน
# -------------------------------

# ฟังก์ชันบันทึกการค้นหา
def add_to_history():
    query = st.session_state.search_input_key.strip()
    if query and query not in st.session_state.search_history:
        st.session_state.search_history.insert(0, query)
        st.session_state.search_history = st.session_state.search_history[:5]
    
# รับค่าค้นหาจากผู้ใช้
search_query = st.text_input("🔍 ค้นหาร้านอาหารตามชื่อ ประเภท หรือชื่อร้าน", 
                            key="search_input_key", 
                            on_change=add_to_history) 

# *** ลบส่วนแสดง 'คำแนะนำ' 'ประวัติการค้นหาล่าสุด' และ 'ร้านแนะนำ' ออกจากโค้ดแล้ว ***

# -------------------------------
# 🎯 การกำหนดรายการร้านที่จะแสดง
# -------------------------------
current_user_favorites = st.session_state.favorites.get(st.session_state.current_user, set())

if st.session_state.view_mode == "favorites":
    all_restaurants_to_display = [r for r in restaurants if r["ชื่อร้าน"] in current_user_favorites]
else:
    all_restaurants_to_display = restaurants

# กรองร้านอาหาร
filtered_restaurants = []
if search_query.strip():
    for r in all_restaurants_to_display:
        if search_query.lower() in r["ชื่อร้าน"].lower() or search_query.lower() in r["ประเภท"].lower():
            filtered_restaurants.append(r)
else:
    filtered_restaurants = all_restaurants_to_display 

# -------------------------------
# 📋 แสดงข้อมูลร้าน + รีวิว
# -------------------------------
st.title("🍽️ ร้านอาหารในปราจีนบุรี")

# 🆕 ส่วนสลับหน้าแสดงผล
col_all, col_fav, _ = st.columns([1, 1, 2])

with col_all:
    # ปุ่มแสดงร้านทั้งหมด
    if st.button("🏠 ร้านทั้งหมด", disabled=(st.session_state.view_mode == "all" and not search_query.strip()), on_click=reset_search):
        pass

with col_fav:
    # ปุ่มแสดงร้านที่ถูกใจ
    fav_count = len(current_user_favorites)
    if st.button(f"❤️ ร้านที่ถูกใจ ({fav_count})", disabled=(st.session_state.view_mode == "favorites" and not search_query.strip()), on_click=switch_to_favorites):
        pass

st.markdown("---")

# 🔄 ปุ่มย้อนกลับ (สำหรับเคลียร์คำค้นหาเมื่อมีการค้นหาอยู่)
is_search_active = search_query.strip()
is_not_all_mode = st.session_state.view_mode != "all"

# แสดงปุ่มย้อนกลับ เมื่อมีการค้นหาอยู่ในโหมดใดๆ
if is_search_active:
    
    button_label = "⬅️ ย้อนกลับสู่รายการทั้งหมด"
    if is_not_all_mode:
        button_label = "⬅️ ย้อนกลับสู่ร้านที่ถูกใจทั้งหมด" 

    # เมื่อกดปุ่มนี้ จะเคลียร์ช่องค้นหา (search_query) เท่านั้น
    if st.button(button_label, on_click=set_search_from_button, args=("",)): 
        pass
        
    st.markdown("---")


# แสดงผลลัพธ์การค้นหา/กรอง
if (search_query.strip() and not filtered_restaurants) or (st.session_state.view_mode == "favorites" and not current_user_favorites and not search_query.strip()):
    if st.session_state.view_mode == "favorites":
        st.warning("คุณยังไม่ได้กดใจร้านอาหารใดๆ 🤍")
    else:
        st.warning(f"ไม่พบร้านอาหารที่ตรงกับคำว่า **'{search_query}'**")

# ถ้ามีร้านอาหารที่ต้องแสดง
if filtered_restaurants:
    for r in filtered_restaurants:
        # กำหนดสถานะหัวใจ
        is_fav = r["ชื่อร้าน"] in current_user_favorites
        # 🌟 ใช้หัวใจสีแดงเมื่อถูกกดใจ และหัวใจขาวเมื่อยังไม่ถูกกดใจ
        heart_icon = "❤️" if is_fav else "🤍"
        
        # ใช้ st.columns เพื่อวางชื่อร้านและปุ่มกดใจในบรรทัดเดียวกัน
        col_title, col_fav_btn = st.columns([3, 1])
        
        with col_title:
            st.subheader(f"🏠 {r['ชื่อร้าน']}")
        
        with col_fav_btn:
            # ใช้ st.button เพื่อให้ตรงตามความต้องการของคุณ
            st.button(
                f"{heart_icon} Favorite", 
                key=f"fav_btn_{r['ชื่อร้าน']}", 
                on_click=toggle_favorite, 
                args=(r["ชื่อร้าน"],),
            )

        # แสดงเบอร์ติดต่อ
        st.markdown(f"**📞 ติดต่อ:** **{r['เบอร์ติดต่อ']}**") # เน้นเบอร์ติดต่อ
        st.markdown(f"**ประเภท:** {r['ประเภท']} | **ราคา:** {r['ราคา']}")
        st.markdown("📍 **แผนที่ร้าน:**")
        
        # เพิ่มโค้ด HTML สำหรับแสดงแผนที่ Google Maps (ใช้ iframe)
        st.markdown(f"""<iframe src="{r['แผนที่']}" width="100%" height="300" style="border:0; border-radius: 8px;" allowfullscreen="" loading="lazy"></iframe>""", unsafe_allow_html=True)

        # รีวิวเฉลี่ย
        ratings = [rev["คะแนนจำนวน"] for rev in st.session_state.reviews if rev["ร้าน"] == r["ชื่อร้าน"]]
        if ratings:
            avg = round(sum(ratings) / len(ratings), 2)
            st.markdown(f"**คะแนนเฉลี่ย:** ⭐ **{avg}** ({len(ratings)} รีวิว)")
        else:
            st.markdown("**คะแนนเฉลี่ย:** ยังไม่มีคะแนน")

        # ส่วนแสดงรีวิวที่มีอยู่
        all_comments = [rev for rev in st.session_state.reviews if rev["ร้าน"] == r["ชื่อร้าน"]]
        if all_comments:
            with st.expander(f"ดูความคิดเห็นทั้งหมด ({len(all_comments)})"):
                for comment_item in all_comments:
                    st.info(f"**{comment_item['ผู้ใช้']}** | ⭐ {comment_item['คะแนนจำนวน']}\n\n{comment_item['ความคิดเห็น']}")


        # ฟอร์มรีวิว
        with st.form(f"form_{r['ชื่อร้าน']}"):
            st.markdown("### 📝 รีวิวร้านนี้")
            rating = st.slider("ให้คะแนน (ดาว)", 1, 5, 3, key=f"rating_{r['ชื่อร้าน']}")
            comment = st.text_area("ความคิดเห็น", key=f"comment_{r['ชื่อร้าน']}")
            submitted = st.form_submit_button("ส่งรีวิว")

            if submitted:
                if not comment:
                    st.error("กรุณาใส่ความคิดเห็นก่อนส่งรีวิว")
                else:
                    st.session_state.reviews.append({
                        "ผู้ใช้": st.session_state.current_user,
                        "ร้าน": r["ชื่อร้าน"],
                        "คะแนนจำนวน": rating,
                        "ความคิดเห็น": comment,
                    })
                    st.success(f"รีวิวของร้าน '{r['ชื่อร้าน']}' ถูกส่งแล้ว!")
                    st.rerun()

        st.markdown("---")
