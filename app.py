import streamlit as st

st.set_page_config(page_title="รีวิวร้านอาหารเนินหอม", layout="wide")
st.title("🍽️ รีวิวร้านอาหารแถวเนินหอม")

restaurants = [
    {"name": "ครัวเนินหอม", "desc": "อาหารไทยรสจัดจ้าน", "lat": 14.048, "lng": 101.378, "category": "อาหารไทย"},
    {"name": "ก๋วยเตี๋ยวเรือเจ๊แดง", "desc": "น้ำซุปเข้มข้น", "lat": 14.049, "lng": 101.379, "category": "ก๋วยเตี๋ยว"},
    {"name": "ข้าวมันไก่ตี๋น้อย", "desc": "ไก่นุ่ม น้ำจิ้มเด็ด", "lat": 14.047, "lng": 101.377, "category": "อาหารจานเดียว"},
    {"name": "ตำแซ่บเนินหอม", "desc": "ส้มตำรสจัด", "lat": 14.046, "lng": 101.376, "category": "อาหารอีสาน"},
    {"name": "ร้านกาแฟบ้านไม้", "desc": "กาแฟสด ขนมโฮมเมด", "lat": 14.045, "lng": 101.375, "category": "กาแฟ"},
    {"name": "หมูกระทะริมทาง", "desc": "หมูกระทะร้อนๆ", "lat": 14.044, "lng": 101.374, "category": "หมูกระทะ"},
    {"name": "ข้าวต้มโต้รุ่ง", "desc": "เปิดดึก อาหารหลากหลาย", "lat": 14.043, "lng": 101.373, "category": "เปิดดึก"},
    {"name": "ชาบูชิเนินหอม", "desc": "ชาบูบุฟเฟ่ต์", "lat": 14.042, "lng": 101.372, "category": "ชาบู"},
    {"name": "ร้านเจ๊อ้อยตามสั่ง", "desc": "อาหารตามสั่งเร็วทันใจ", "lat": 14.041, "lng": 101.371, "category": "อาหารตามสั่ง"},
    {"name": "ขนมจีนคุณยาย", "desc": "น้ำยาเข้มข้น", "lat": 14.040, "lng": 101.370, "category": "ขนมจีน"},
]

search = st.text_input("🔍 ค้นหาร้านอาหารตามชื่อ")
category = st.selectbox("🍽️ เลือกประเภทอาหาร", ["ทั้งหมด"] + sorted(set(r["category"] for r in restaurants)))

filtered = [r for r in restaurants if search.lower() in r["name"].lower()]
if category != "ทั้งหมด":
    filtered = [r for r in filtered if r["category"] == category]

st.sidebar.header("📸 อัปโหลดรูปภาพร้านอาหาร")
uploaded_image = st.sidebar.file_uploader("เลือกรูปภาพ", type=["jpg", "png"])
if uploaded_image:
    st.sidebar.image(uploaded_image, caption="รูปที่อัปโหลด", use_column_width=True)

for r in filtered:
    st.subheader(f"{r['name']}")
    st.write(r['desc'])
    map_url = f"https://maps.google.com/maps?q={r['lat']},{r['lng']}&hl=th&z=16&output=embed"
    st.markdown(f"<iframe src='{map_url}' width='100%' height='200'></iframe>", unsafe_allow_html=True)
    rating = st.slider(f"ให้คะแนนร้าน {r['name']}", 1, 5, 3)
    st.write(f"⭐ คุณให้คะแนน: {rating}/5")
    st.markdown("---")

st.header("💬 แสดงความคิดเห็น")
comment = st.text_area("พิมพ์ความคิดเห็นของคุณที่นี่")
if st.button("ส่งความคิดเห็น"):
    st.success(f"คุณแสดงความคิดเห็นว่า: {comment}")
