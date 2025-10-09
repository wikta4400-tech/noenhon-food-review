import streamlit as st
import urllib.parse 
import json
import os 

# กำหนดชื่อไฟล์สำหรับเก็บข้อมูล
USER_DATA_FILE = "user_data.json"
REVIEW_DATA_FILE = "reviews_data.json" 

# ----------------------------------------------------------------------------------
# 💾 ฟังก์ชันจัดการข้อมูล (Load/Save)
# ----------------------------------------------------------------------------------

def load_user_data():
    """โหลดข้อมูลผู้ใช้จากไฟล์ JSON"""
    if not os.path.exists(USER_DATA_FILE):
        data = {"admin": "1234", "user01": "pass"}
        save_user_data(data)
        return data
    
    try:
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.error("❗ ข้อมูลผู้ใช้ในไฟล์เสีย กรุณาตรวจสอบ user_data.json")
        return {"admin": "1234", "user01": "pass"} 

def save_user_data(data):
    """บันทึกข้อมูลผู้ใช้ลงในไฟล์ JSON"""
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- ฟังก์ชันสำหรับจัดการรีวิว ---
def load_reviews():
    """โหลดข้อมูลรีวิวจากไฟล์ JSON"""
    if not os.path.exists(REVIEW_DATA_FILE):
        return []
    
    try:
        with open(REVIEW_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.warning("❗ ข้อมูลรีวิวในไฟล์เสีย หรือไฟล์ว่างเปล่า จะใช้ข้อมูลเริ่มต้นแทน")
        return []

def save_reviews(reviews_list):
    """บันทึกข้อมูลรีวิวลงในไฟล์ JSON"""
    with open(REVIEW_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(reviews_list, f, indent=4, ensure_ascii=False)


st.set_page_config(page_title="รีวิวร้านอาหารปราจีนบุรี", layout="centered")

# -------------------------------
# 🔐 ระบบผู้ใช้ (Session State Initialization)
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "favorites" not in st.session_state:
    st.session_state.favorites = {} 
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "all" 
if "search_input_key" not in st.session_state:
    st.session_state.search_input_key = ""
    
if "reviews" not in st.session_state:
    st.session_state.reviews = load_reviews() 

    
# ----------------------------------------------------------------------------------
# 🛠️ ฟังก์ชันสร้าง Google Maps URL และตัวช่วย
# ----------------------------------------------------------------------------------
def create_google_maps_url(name, town="ปราจีนบุรี"):
    query = f"{name} {town}"
    encoded_query = urllib.parse.quote_plus(query)
    return f"https://www.google.com/maps/search/?api=1&query={encoded_query}"

def set_search_from_button(query):
    st.session_state.search_input_key = query 
    query_to_save = query.strip()
    if query_to_save and query_to_save not in st.session_state.search_history:
        st.session_state.search_history.insert(0, query_to_save)
        st.session_state.search_history = st.session_state.search_history[:5]
    st.rerun() 

def reset_search():
    st.session_state.view_mode = "all"
    set_search_from_button("") 

def switch_to_favorites():
    st.session_state.view_mode = "favorites"
    st.session_state.search_input_key = "" 
    st.rerun() 

def toggle_favorite(restaurant_name):
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
    
def add_to_history():
    query = st.session_state.search_input_key.strip()
    if query and query not in st.session_state.search_history:
        st.session_state.search_history.insert(0, query)
        st.session_state.search_history = st.session_state.search_history[:5]
    
def get_star_rating_emoji(score):
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
# 📦 ข้อมูลร้านอาหาร (ยังคงเดิม)
# -------------------------------
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
    {"ชื่อร้าน": "ริมบ้านชานเมือง", "ประเภท": "อาหารไทย / บรรยากาศ", "ราคา": "฿200–400", "เบอร์ติดต่อ": "099-449-8099", "Town": "ศรีมหาโพธิ", "Map_URL_Override": "https://maps.google.com/?cid=13007968190188579196&g_mp=Cidnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLlNlYXJjaFRleHQ"},
    {"ชื่อร้าน": "LA VILAS", "ประเภท": "อาหารไทย / นานาชาติ", "ราคา": "฿150–350", "เบอร์ติดต่อ": "037-211-979", "Town": "เมืองปราจีนบุรี", "Map_URL_Override": "https://maps.google.com/?cid=16115973080688479695&g_mp=Cidnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLlNlYXJjaFRleHQ"},
    {"ชื่อร้าน": "ร้านอาหารบ้านริมน้ำ", "ประเภท": "อาหารไทย / ริมน้ำ", "ราคา": "฿250–500", "เบอร์ติดต่อ": "037-212-797", "Town": "เมืองปราจีนบุรี", "Map_URL_Override": "https://maps.google.com/?cid=2273684802098570789&g_mp=Cidnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLlNlYXJjaFRleHQ"},
    {"ชื่อร้าน": "ร้านอาหารร่มไม้", "ประเภท": "อาหารไทย / อาหารตามสั่ง", "ราคา": "฿100–300", "เบอร์ติดต่อ": "037-216-080", "Town": "เมืองปราจีนบุรี", "Map_URL_Override": "https://maps.google.com/?cid=17050586906585157124&g_mp=Cidnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLlNlYXJjaFRleHQ"},
    {"ชื่อร้าน": "บ้านเล่าเรื่อง เมืองสมุนไพรปราจีนบุรี", "ประเภท": "คาเฟ่ / เครื่องดื่มสมุนไพร", "ราคา": "฿80–200", "เบอร์ติดต่อ": "097-021-1037", "Town": "เมืองปราจีนบุรี", "Map_URL_Override": "https://maps.google.com/?cid=6184257939368439003&g_mp=Cidnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLlNlYXJjaFRleHQ"},
]

restaurants = []
for r in restaurants_raw:
    if "Map_URL_Override" in r and r["Map_URL_Override"]:
        r["แผนที่"] = r["Map_URL_Override"]
    else:
        r["แผนที่"] = create_google_maps_url(r["ชื่อร้าน"], r["Town"])
    restaurants.append(r)


# -------------------------------
# 🧾 หน้าเข้าสู่ระบบ / สมัครสมาชิก
# -------------------------------
if not st.session_state.logged_in:
    
    users = load_user_data() 
    
    st.title("🔐 เข้าสู่ระบบ / สมัครสมาชิก")
    tab1, tab2 = st.tabs(["เข้าสู่ระบบ", "สมัครสมาชิก"])

    with tab1:
        username = st.text_input("ชื่อผู้ใช้", key="login_user")
        password = st.text_input("รหัสผ่าน", type="password", key="login_pass")
        if st.button("เข้าสู่ระบบ"):
            if username in users and users[username] == password: 
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
            
            users = load_user_data() 
            
            if new_user in users:
                st.warning("ชื่อผู้ใช้นี้มีอยู่แล้ว")
            elif new_user and new_pass:
                
                users[new_user] = new_pass
                save_user_data(users) 
                
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
    if st.button("ออกจากระบบ", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.rerun()

# -------------------------------
# 🔍 ช่องค้นหาร้าน
# -------------------------------
# 🔴 โค้ดที่แก้ไข: ลบ "(ร้านดัง)" ออกจากหัวข้อ
st.title("🍽️ รีวิวร้านอาหารในปราจีนบุรี") 

search_query = st.text_input("🔍 ค้นหาร้านอาหารตามชื่อ ประเภท หรือชื่อร้าน", 
                             key="search_input_key", 
                             on_change=add_to_history) 

# -------------------------------
# 🎯 การกำหนดรายการร้านที่จะแสดง
# -------------------------------
current_user_favorites = st.session_state.favorites.get(st.session_state.current_user, set())

# ส่วนสลับหน้าแสดงผล
col_all, col_fav, _ = st.columns([1, 1, 2])

with col_all:
    if st.button("🏠 ร้านทั้งหมด", disabled=(st.session_state.view_mode == "all" and not search_query.strip()), on_click=reset_search, use_container_width=True):
        pass

with col_fav:
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

# 🔄 ปุ่มย้อนกลับ
is_search_active = search_query.strip()
is_not_all_mode = st.session_state.view_mode != "all"

if is_search_active:
    
    button_label = "⬅️ ย้อนกลับสู่รายการทั้งหมด"
    if is_not_all_mode:
        button_label = "⬅️ ย้อนกลับสู่ร้านที่ถูกใจทั้งหมด" 

    if st.button(button_label, on_click=set_search_from_button, args=("",), use_container_width=True): 
        pass
        
    st.markdown("---")

# แสดงผลลัพธ์
if (search_query.strip() and not filtered_restaurants) or (st.session_state.view_mode == "favorites" and not current_user_favorites and not search_query.strip()):
    if st.session_state.view_mode == "favorites":
        st.warning("คุณยังไม่ได้กดใจร้านอาหารใดๆ 🤍")
    else:
        st.warning(f"ไม่พบร้านอาหารที่ตรงกับคำว่า **'{search_query}'**")

# ถ้ามีร้านอาหารที่ต้องแสดง (Minimalist Layout)
if filtered_restaurants:
    for r in filtered_restaurants:
        is_fav = r["ชื่อร้าน"] in current_user_favorites
        heart_icon = "❤️" if is_fav else "🤍"
        
        # 1. ชื่อร้าน (หัวข้อใหญ่)
        st.subheader(f"🏠 {r['ชื่อร้าน']}")
        
        # 2. ข้อมูลกระชับ (ประเภท, ราคา, ติดต่อ)
        st.markdown(f"**ประเภท:** {r['ประเภท']} | **ราคา:** {r['ราคา']} | **📞 ติดต่อ:** **{r['เบอร์ติดต่อ']}**") 

        # 3. ปุ่มทั้งหมดอยู่ในแถวเดียว
        col_map, col_fav_btn, _ = st.columns([2, 1.5, 3]) 

        with col_map:
            st.link_button(
                "🌐 เปิด Google Maps", 
                url=r['แผนที่'], 
                use_container_width=True
            )
        
        with col_fav_btn:
            st.button(
                f"{heart_icon} Favorite", 
                key=f"fav_btn_{r['ชื่อร้าน']}", 
                on_click=toggle_favorite, 
                args=(r["ชื่อร้าน"],),
                use_container_width=True
            )

        # 4. รีวิวเฉลี่ย
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
            with st.expander(f"ดูความคิดเห็นทั้งหมด {len(all_comments)}"): 
                for comment_item in all_comments:
                    comment_stars = get_star_rating_emoji(comment_item['คะแนนจำนวน'])
                    st.info(f"**{comment_item['ผู้ใช้']}** | {comment_stars}\n\n{comment_item['ความคิดเห็น']}")


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
                    new_review = {
                        "ผู้ใช้": st.session_state.current_user,
                        "ร้าน": r["ชื่อร้าน"],
                        "คะแนนจำนวน": rating,
                        "ความคิดเห็น": comment,
                    }
                    st.session_state.reviews.append(new_review)
                    
                    save_reviews(st.session_state.reviews) 
                    
                    st.success(f"รีวิวของร้าน '{r['ชื่อร้าน']}' ถูกส่งและบันทึกแล้ว!")
                    st.rerun() 

        st.markdown("---")
