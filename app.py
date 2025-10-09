import streamlit as st
import urllib.parse 

st.set_page_config(page_title="รีวิวร้านอาหารปราจีนบุรี", layout="centered")

# -----------------------------------------------------------
# --- CSS: บังคับตัวอักษรดำ + แก้ไขปุ่มให้มีขอบชัดเจน (Wongnai Style) ---
# -----------------------------------------------------------
st.markdown(
    """
    <style>
    /* 1. พื้นหลังหลัก (ขาวสะอาด) */
    .stApp {
        background-color: #FFFFFF !important; 
    }
    
    /* 2. บังคับตัวอักษรหลักทั้งหมดเป็นสีดำสนิท */
    .stApp, .stMarkdown, .stText {
        color: #000000 !important; 
    }
    
    /* 3. บังคับให้ Sidebar เป็นสีขาว */
    .css-1d3f9sd, .css-1dp5q0n {
        background-color: #FFFFFF !important;
    }

    /* 4. หัวข้อหลัก (Title, Subheader) ใช้สีน้ำเงินเข้มแบบ Wongnai */
    h1, h2, h3 {
        color: #002244 !important; /* น้ำเงินเข้ม */
    }

    /* 5. บังคับตัวอักษรใน Input/Textarea/Password/Slider/Alerts ให้เป็นสีดำ */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stSlider label,
    .stAlert {
        color: #000000 !important;
    }
    /* Placeholder text (ตัวอักษรแนะนำในช่องว่าง) */
    input::placeholder {
        color: #666666 !important; 
    }

    /* 6. ปุ่มหลัก (Primary) - สีส้มสไตล์ Wongnai (ใช้สำหรับ ส่งรีวิว, เข้าสู่ระบบ) */
    .stButton>button {
        background-color: #FF5722; /* สีส้มแบบ Wongnai */
        color: #FFFFFF !important; /* ตัวอักษรสีขาวในปุ่มส้ม */
        border: 1px solid #FF5722;
        border-radius: 8px;
        font-weight: bold; /* ตัวหนา */
    }
    
    /* 7. ปุ่มรอง (Secondary) - ปุ่มที่มีสัญลักษณ์ (ร้านทั้งหมด, ร้านที่ถูกใจ, Favorite) */
    .stButton>button:has(.streamlit-emoji-icon) {
        background-color: #FFFFFF; 
        color: #002244 !important; /* ตัวอักษรน้ำเงินเข้ม */
        border: 2px solid #002244; /* เพิ่มขอบน้ำเงินเข้มเพื่อให้โดดเด่นจากพื้นหลังขาว */
    }
    
    /* 8. Input Fields - พื้นหลังเทาอ่อนและขอบเทา */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea {
        background-color: #F8F8F8;
        border: 1px solid #CCCCCC;
        border-radius: 4px;
    }

    /* 9. กล่องข้อมูล (st.info) */
    .stAlert:has(.streamlit-badge-info) {
        background-color: #E6F7FF; /* ฟ้าอ่อน */
        border: 1px solid #002244;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# -----------------------------------------------------------

# -----------------------------------------------------------
# --- โลโก้ ---
# -----------------------------------------------------------
# ❗❗ คุณต้องเปลี่ยน URL/ชื่อไฟล์ด้านล่างนี้ ❗❗
st.image(
    "https://i.ibb.co/your-logo-image.png", # <--- แทนที่ด้วย URL โลโก้ของคุณ (หรือชื่อไฟล์ เช่น "my_logo.png")
    width=150
)
# -----------------------------------------------------------


# -------------------------------
# 🔐 ระบบผู้ใช้ (จำลอง)
# -------------------------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234", "user01": "pass"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "favorites" not in st.session_state:
    st.session_state.favorites = {} # {username: set_of_restaurant_names}
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "all" # 'all' หรือ 'favorites'
if "search_input_key" not in st.session_state:
    st.session_state.search_input_key = ""
if "reviews" not in st.session_state:
    st.session_state.reviews = []
    

# ----------------------------------------------------------------------------------
# 🛠️ ฟังก์ชันสร้าง Google Maps URL (แก้ไขให้ใช้ URL มาตรฐาน)
# ----------------------------------------------------------------------------------
def create_google_maps_url(name, town="ปราจีนบุรี"):
    """สร้าง URL แผนที่ Google Maps โดยใช้รูปแบบ URL มาตรฐานสำหรับการค้นหา (Search Query)"""
    
    # 1. เข้ารหัสชื่อร้านและจังหวัด
    query = f"{name} {town}"
    encoded_query = urllib.parse.quote_plus(query)
    
    # 2. ใช้ URL มาตรฐานของ Google Maps โดยตรง: "https://www.google.com/maps/search/?api=1&query="
    # การใช้รูปแบบนี้จะมั่นใจได้ว่าเบราว์เซอร์จะเปิด Google Maps จริงๆ 
    return f"https://www.google.com/maps/search/?api=1&query={encoded_query}"


# ----------------------------------------------------------------------------------
# ❗ ฟังก์ชันหลัก
# ----------------------------------------------------------------------------------
def set_search_from_button(query):
    """ตั้งค่า st.session_state.search_input_key จากปุ่มเคลียร์ค้นหา และสั่ง Rerun"""
    st.session_state.search_input_key = query 
    
    query_to_save = query.strip()
    if query_to_save and query_to_save not in st.session_state.search_history:
        st.session_state.search_history.insert(0, query_to_save)
        st.session_state.search_history = st.session_state.search_history[:5]
        
    st.rerun()

def reset_search():
    """ฟังก์ชันสำหรับตั้งค่า Search เป็นค่าว่าง, ตั้ง View Mode เป็น 'all' และสั่ง rerun"""
    st.session_state.view_mode = "all"
    set_search_from_button("") 

def switch_to_favorites():
    st.session_state.view_mode = "favorites"
    st.session_state.search_input_key = "" # เคลียร์ช่องค้นหาเมื่อเปลี่ยนโหมด
    st.rerun()

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

def add_to_history():
    query = st.session_state.search_input_key.strip()
    if query and query not in st.session_state.search_history:
        st.session_state.search_history.insert(0, query)
        st.session_state.search_history = st.session_state.search_history[:5]

def get_star_rating_emoji(score):
    """แปลงคะแนนตัวเลข (0-5) เป็นสัญลักษณ์ดาว (เช่น ⭐⭐⭐⭐½)"""
    full_star = "⭐"
    half_star = "½"
    empty_star = "☆"
    score = round(score * 2) / 2 
    
    stars = ""
    for i in range(1, 6):
        if score >= i:
            stars += full_star
        elif score == i - 0.5:
            stars += half_star
        else:
            stars += empty_star
            
    return stars

# -------------------------------
# 📦 ข้อมูลร้านอาหาร (ใช้ชื่อที่ชัดเจนที่สุดในการค้นหาแผนที่)
# -------------------------------
# ❗❗ ใช้ฟิลด์ "Town" เพื่อระบุอำเภอ/พื้นที่ให้ Google Maps ค้นหาได้แม่นยำขึ้น ❗❗
restaurants_raw = [
    {"ชื่อร้าน": "ครัวอากู๋", "ประเภท": "อาหารไทย / ซีฟู้ด", "ราคา": "฿250–450", "เบอร์ติดต่อ": "083-966-9997", "Town": "กบินทร์บุรี"}, 
    {"ชื่อร้าน": "Cafe Kantary 304", "ประเภท": "เบเกอรี่ & คาเฟ่", "ราคา": "฿90–200", "เบอร์ติดต่อ": "037-239-777", "Town": "ศรีมหาโพธิ"}, 
    {"ชื่อร้าน": "ก๋วยเตี๋ยวกากหมูลานบริบูรณ์", "ประเภท": "ก๋วยเตี๋ยว / อาหารท้องถิ่น", "ราคา": "฿50–100", "เบอร์ติดต่อ": "089-995-8359", "Town": "เมืองปราจีนบุรี"}, 
    {"ชื่อร้าน": "ซินจ่าว2", "ประเภท": "ไทย & เวียดนาม", "ราคา": "฿100–250", "เบอร์ติดต่อ": "086-567-8901", "Town": "เมืองปราจีนบุรี"}, 
    {"ชื่อร้าน": "Bloom Restaurant Siamdasada", "ประเภท": "อาหารฟิวชั่น / อาหารไทย", "ราคา": "฿300–600", "เบอร์ติดต่อ": "037-216-800", "Town": "เขาใหญ่ฝั่งปราจีนบุรี"}, 
    {"ชื่อร้าน": "ก๋วยเตี๋ยวเรือนายติณณ์", "ประเภท": "ก๋วยเตี๋ยว / อาหารท้องถิ่น", "ราคา": "฿50–100", "เบอร์ติดต่อ": "096-618-5163", "Town": "เมืองปราจีนบุรี"}, 
    {"ชื่อร้าน": "อีสานเฮาส์ 304", "ประเภท": "อาหารอีสาน / จิ้มจุ่ม", "ราคา": "฿150–300", "เบอร์ติดต่อ": "096-383-8183", "Town": "ศรีมหาโพธิ"}, 
    {"ชื่อร้าน": "Myrrh Cafe (มายร์ คาเฟ่)", "ประเภท": "คาเฟ่ / กาแฟ / วิวเขา", "ราคา": "฿80–180", "เบอร์ติดต่อ": "089-887-8125", "Town": "เนินหอม"},
    {"ชื่อร้าน": "เจ๊นิด กุ้งเผา", "ประเภท": "กุ้งเผา / ซีฟู้ด", "ราคา": "฿300–700", "เบอร์ติดต่อ": "091-456-7890", "Town": "เมืองปราจีนบุรี"},
    {"ชื่อร้าน": "ครัวปราจีน", "ประเภท": "อาหารไทย / อาหารป่า", "ราคา": "฿250–500", "เบอร์ติดต่อ": "064-678-9010", "Town": "บ้านสร้าง"}, 
    {"ชื่อร้าน": "ร้านข้าวต้มกุ๊ยนายพล", "ประเภท": "ข้าวต้ม / อาหารไทย", "ราคา": "฿100–300", "เบอร์ติดต่อ": "065-123-4560", "Town": "เมืองปราจีนบุรี"}, 
    {"ชื่อร้าน": "เรือนไทยอาหารไทย", "ประเภท": "อาหารไทยโบราณ / บรรยากาศ", "ราคา": "฿300–600", "เบอร์ติดต่อ": "086-234-5670", "Town": "เนินหอม"}, 
    {"ชื่อร้าน": "ก๋วยเตี๋ยวต้มยำโบราณ", "ประเภท": "ก๋วยเตี๋ยว / ต้มยำ", "ราคา": "฿50–100", "เบอร์ติดต่อ": "083-419-4411", "Town": "เมืองปราจีนบุรี"}, 
    {"ชื่อร้าน": "ร้านขนมไทยคุณย่า", "ประเภท": "ขนมไทย / น้ำกะทิ", "ราคา": "฿40–80", "เบอร์ติดต่อ": "089-789-0120", "Town": "เมืองปราจีนบุรี"}, 
    {"ชื่อร้าน": "ข้าวมันไก่ตอนฮกเกี้ยน", "ประเภท": "ข้าวมันไก่ / อาหารจีน", "ราคา": "฿60–120", "เบอร์ติดต่อ": "037-216-919", "Town": "เมืองปราจีนบุรี"}, 
]

# ประมวลผลข้อมูลเพื่อสร้างลิงก์ Google Maps ที่ใช้ได้จริง
restaurants = []
for r in restaurants_raw:
    # ❗ ใช้ฟังก์ชันค้นหาจากชื่อร้าน + อำเภอ
    r["แผนที่"] = create_google_maps_url(r["ชื่อร้าน"], r["Town"])
    restaurants.append(r)


# -------------------------------
# 🧾 หน้าเข้าสู่ระบบ / สมัครสมาชิก
# -------------------------------
if not st.session_state.logged_in:
    st.title("🔐 เข้าสู่ระบบ / สมัครสมาชิก")
    tab1, tab2 = st.tabs(["เข้าสู่ระบบ", "สมัครสมาชิก"])

    with tab1:
        username = st.text_input("ชื่อผู้ใช้", key="login_user")
        password = st.text_input("รหัสผ่าน", type="password", key="login_pass")
        # ปุ่มเข้าสู่ระบบ (Primary style - สีส้ม)
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
        # ปุ่มสมัครสมาชิก (Primary style - สีส้ม)
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
                st.error("กรุณา กรอกข้อมูลให้ครบ")
    st.stop()

# -------------------------------
# 🔓 ปุ่มออกจากระบบ
# -------------------------------
with st.sidebar:
    st.write(f"👤 ผู้ใช้งาน: **{st.session_state.current_user}**")
    # ปุ่มออกจากระบบ (Secondary style - มีขอบน้ำเงินเข้ม)
    if st.button("ออกจากระบบ", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.rerun()

# -------------------------------
# 🔍 ช่องค้นหาร้าน
# -------------------------------
st.title("🍽️ รีวิวร้านอาหารในปราจีนบุรี (ร้านดัง)")

# รับค่าค้นหาจากผู้ใช้
search_query = st.text_input("🔍 ค้นหาร้านอาหารตามชื่อ ประเภท หรือชื่อร้าน", 
                             key="search_input_key", 
                             on_change=add_to_history) 

# -------------------------------
# 🎯 การกำหนดรายการร้านที่จะแสดง
# -------------------------------
current_user_favorites = st.session_state.favorites.get(st.session_state.current_user, set())

# 🆕 ส่วนสลับหน้าแสดงผล
col_all, col_fav, _ = st.columns([1, 1, 2])

with col_all:
    # ปุ่มแสดงร้านทั้งหมด (Secondary style - มีขอบน้ำเงินเข้ม)
    if st.button("🏠 ร้านทั้งหมด", disabled=(st.session_state.view_mode == "all" and not search_query.strip()), on_click=reset_search, use_container_width=True):
        pass

with col_fav:
    # ปุ่มแสดงร้านที่ถูกใจ (Secondary style - มีขอบน้ำเงินเข้ม)
    fav_count = len(current_user_favorites)
    if st.button(f"❤️ ร้านที่ถูกใจ ({fav_count})", disabled=(st.session_state.view_mode == "favorites" and not search_query.strip()), on_click=switch_to_favorites, use_container_width=True):
        pass

st.markdown("---")


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

# 🔄 ปุ่มย้อนกลับ (สำหรับเคลียร์คำค้นหาเมื่อมีการค้นหาอยู่)
is_search_active = search_query.strip()
is_not_all_mode = st.session_state.view_mode != "all"

# แสดงปุ่มย้อนกลับ เมื่อมีการค้นหาอยู่ในโหมดใดๆ
if is_search_active:
    
    button_label = "⬅️ ย้อนกลับสู่รายการทั้งหมด"
    if is_not_all_mode:
        button_label = "⬅️ ย้อนกลับสู่ร้านที่ถูกใจทั้งหมด" 

    # ปุ่มย้อนกลับ (Secondary style - มีขอบน้ำเงินเข้ม)
    if st.button(button_label, on_click=set_search_from_button, args=("",), use_container_width=True): 
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
        heart_icon = "❤️" if is_fav else "🤍"
        
        # ใช้ st.columns เพื่อวางชื่อร้านและปุ่มกดใจในบรรทัดเดียวกัน
        col_title, col_fav_btn = st.columns([3, 1])
        
        with col_title:
            st.subheader(f"🏠 {r['ชื่อร้าน']}")
        
        with col_fav_btn:
            # ปุ่ม Favorite (Secondary style - มีขอบน้ำเงินเข้ม)
            st.button(
                f"{heart_icon} Favorite", 
                key=f"fav_btn_{r['ชื่อร้าน']}", 
                on_click=toggle_favorite, 
                args=(r["ชื่อร้าน"],),
                use_container_width=True
            )

        # แสดงเบอร์ติดต่อ
        st.markdown(f"**📞 ติดต่อ:** **{r['เบอร์ติดต่อ']}**") # เน้นเบอร์ติดต่อ
        st.markdown(f"**ประเภท:** {r['ประเภท']} | **ราคา:** {r['ราคา']}")
        
        # ❗ ใช้ st.link_button เพื่อเปิด Google Maps จริง (ด้วยการค้นหาชื่อร้าน) 
        # ปุ่ม Link Button (Secondary style - มีขอบน้ำเงินเข้ม)
        st.link_button(
            "🌐 เปิด Google Maps", 
            url=r['แผนที่'], # URL ที่สร้างจากการค้นหาชื่อร้าน (รูปแบบมาตรฐาน)
            use_container_width=True
        )

        # รีวิวเฉลี่ย
        ratings = [rev["คะแนนจำนวน"] for rev in st.session_state.reviews if rev["ร้าน"] == r["ชื่อร้าน"]]
        if ratings:
            avg = sum(ratings) / len(ratings)
            avg_rounded = round(avg, 2)
            stars_emoji = get_star_rating_emoji(avg) 
            st.markdown(f"**คะแนนเฉลี่ย:** {stars_emoji} **{avg_rounded}** ({len(ratings)} รีวิว)")
        else:
            st.markdown("**คะแนนเฉลี่ย:** ยังไม่มีคะแนน")

        # ส่วนแสดงรีวิวที่มีอยู่
        all_comments = [rev for rev in st.session_state.reviews if rev["ร้าน"] == r["ชื่อร้าน"]]
        if all_comments:
            with st.expander(f"ดูความคิดเห็นทั้งหมด ({len(all_comments)})"):
                for comment_item in all_comments:
                    comment_stars = get_star_rating_emoji(comment_item['คะแนนจำนวน'])
                    st.info(f"**{comment_item['ผู้ใช้']}** | {comment_stars}\n\n{comment_item['ความคิดเห็น']}")


        # ฟอร์มรีวิว
        with st.form(f"form_{r['ชื่อร้าน']}"):
            st.markdown("### 📝 รีวิวร้านนี้")
            rating = st.slider("ให้คะแนน (ดาว)", 1, 5, 3, key=f"rating_{r['ชื่อร้าน']}")
            comment = st.text_area("ความคิดเห็น", key=f"comment_{r['ชื่อร้าน']}")
            # ปุ่มส่งรีวิว (Primary style - สีส้ม)
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
