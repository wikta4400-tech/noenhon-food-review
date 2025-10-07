import streamlit as st

st.set_page_config(page_title="รีวิวร้านอาหารเนินหอม", layout="wide")
st.title("🍽️ รีวิวร้านอาหารแถวเนินหอม จังหวัดปราจีนบุรี")

# รวมร้านอาหารทั้งหมด
restaurants = [
    # ร้านเดิม
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

    # ร้านใหม่แถวเนินหอม
    {"name": "Noen Homme Cafe", "desc": "ร้านกาแฟบ้านดินดีไซน์เก๋ ใกล้ป่าเขาใหญ่", "lat": 14.051, "lng": 101.381, "category": "คาเฟ่"},
    {"name": "DR Dimsum", "desc": "ร้านติ่มซำยอดนิยมในปราจีนบุรี รสชาติเด็ด", "lat": 14.052, "lng": 101.382, "category": "ติ่มซำ"},
    {"name": "Bloom Restaurant @ Siamdasada", "desc": "ร้านอาหารฟิวชั่นในรีสอร์ตหรู บรรยากาศดี", "lat": 14.053, "lng": 101.383, "category": "ฟิวชั่น"},
    {"name": "Nunou Café", "desc": "คาเฟ่สายธรรมชาติ ทางขึ้นเขาใหญ่ฝั่งปราจีนบุรี", "lat": 14.054, "lng": 101.384, "category": "คาเฟ่"},
    {"name": "BAN PUNN Steak Cafe Bar", "desc": "ร้านสเต๊กบรรยากาศดี เหมาะกับมื้อเย็น", "lat": 14.055, "lng": 101.385, "category": "สเต๊ก"},
    {"name": "Happy Bew", "desc": "ร้านเบเกอรี่เล็ก ๆ น่ารัก มีเค้กและขนมโฮมเมด", "lat": 14.056, "lng": 101.386, "category": "เบเกอรี่"},
    {"name": "ตีนเขา Food & Camping", "desc": "ร้านอาหารแนวแคมป์ปิ้ง ใกล้ธรรมชาติ", "lat": 14.057, "lng": 101.387, "category": "แคมป์ปิ้ง"},
    {"name": "ปั่นในป่าคาเฟ่", "desc": "คาเฟ่เครื่องดื่มแนวสุขภาพ บรรยากาศร่มรื่น", "lat": 14.058, "lng": 101.388, "category": "น้ำผลไม้"},
    {"name": "ร้านก๋วยเตี๋ยวไก่ ข้าวมันไก่ เบตง", "desc": "เมนูหลากหลาย ทั้งก๋วยเตี๋ยว ข้าวมันไก่", "lat": 14.059, "lng": 101.389, "category": "อาหารจานเดียว"},
    {"name": "สวนอาหารบ้านเนินน้ำ", "desc": "ร้านริมน้ำวิวสวย เมนูเด็ดคือกุ้งแม่น้ำเผา", "lat": 14.060, "lng": 101.390, "category": "ซีฟู้ด"},
]

# ระบบค้นหาและกรอง
search = st.text_input("🔍 ค้นหาร้านอาหารตามชื่อ")
category = st.selectbox("🍽️ เลือกประเภทอาหาร", ["ทั้งหมด"] + sorted(set(r["category"] for r in restaurants)))

filtered = [r for r in restaurants if search.lower() in r["name"].lower()]
if category != "ทั้งหมด":
    filtered = [r for r in filtered if r["category"] == category]

# อัปโหลดรูปภาพ
st.sidebar.header("📸 อัปโหลดรูปภาพร้านอาหาร")
uploaded_image = st.sidebar.file_uploader("เลือกรูปภาพ", type=["jpg", "png"])
if uploaded_image:
    st.sidebar.image(uploaded_image, caption="รูปที่อัปโหลด", use_column_width=True)

# แสดงร้านอาหาร
for r in filtered:
    st.subheader(f"{r['name']}")
    st.write(r['desc'])
    map_url = f"https://maps.google.com/maps?q={r['lat']},{r['lng']}&hl=th&z=16&output=embed"
    st.markdown(f"<iframe src='{map_url}' width='100%' height='200'></iframe>", unsafe_allow_html=True)
    rating = st.slider(f"ให้คะแนนร้าน {r['name']}", 1, 5, 3)
    st.write(f"⭐ คุณให้คะแนน: {rating}/5")
    comment = st.text_area(f"💬 แสดงความคิดเห็นเกี่ยวกับร้าน {r['name']}")
    if st.button(f"ส่งความคิดเห็นร้าน {r['name']}"):
        st.success(f"คุณแสดงความคิดเห็นว่า: {comment}")
    st.markdown("---")

# รีวิวเว็บไซต์
st.header("📝 รีวิวเว็บไซต์นี้")

with st.form("site_review_form"):
    site_rating = st.slider("ให้คะแนนเว็บไซต์นี้", 1, 5, 4)
    site_comment = st.text_area("แสดงความคิดเห็นเกี่ยวกับเว็บไซต์")
    submitted = st.form_submit_button("ส่งรีวิวเว็บไซต์")

if submitted:
    st.success("✅ ขอบคุณสำหรับรีวิวเว็บไซต์!")
    st.markdown(f"⭐ คุณให้คะแนนเว็บไซต์นี้: **{site_rating}/5**")
    st.markdown(f"💬 ความคิดเห็นของคุณ: _{site_comment}_")
