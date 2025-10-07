import streamlit as st

st.set_page_config(page_title="รีวิวร้านอาหารเนินหอม", layout="wide")
st.title("🍽️ รีวิวร้านอาหารแถวเนินหอม จังหวัดปราจีนบุรี")

# ข้อมูลร้านอาหารพร้อมภาพ
restaurants = [
    {
        "name": "ร้านเจ๊อ้อยตามสั่ง",
        "desc": "อาหารตามสั่งเร็วทันใจ",
        "lat": 14.041,
        "lng": 101.371,
        "category": "อาหารตามสั่ง",
        "image": "https://img.wongnai.com/p/1920x0/2020/03/29/138f916c791a4874979af06dd79dbaaf.jpg"
    },
    {
        "name": "ขนมจีนคุณยาย",
        "desc": "น้ำยาเข้มข้น",
        "lat": 14.040,
        "lng": 101.370,
        "category": "ขนมจีน",
        "image": "https://img.wongnai.com/p/1920x0/2021/12/31/9cdc4b16dcf44dc495beca0dcaa79e4a.jpg"
    },
    {
        "name": "ร้านปั่นในป่าคาเฟ่",
        "desc": "คาเฟ่เครื่องดื่มแนวสุขภาพ บรรยากาศร่มรื่น",
        "lat": 14.058,
        "lng": 101.388,
        "category": "น้ำผลไม้",
        "image": "https://10619-2.s.cdn12.com/rests/small/w550/h367/108_510225228.jpg"
    },
    {
        "name": "ร้านก๋วยเตี๋ยวไก่ ข้าวมันไก่ เบตง",
        "desc": "เมนูหลากหลาย ทั้งก๋วยเตี๋ยว ข้าวมันไก่",
        "lat": 14.059,
        "lng": 101.389,
        "category": "อาหารจานเดียว",
        "image": "https://img.wongnai.com/p/1920x0/2024/03/04/85fd2de794ce47eea296fe6d28f3ceb9.jpg"
    },
    {
        "name": "Bloom Restaurant @ Siamdasada",
        "desc": "ร้านอาหารฟิวชั่นในรีสอร์ตหรู บรรยากาศดี",
        "lat": 14.053,
        "lng": 101.383,
        "category": "ฟิวชั่น",
        "image": "https://img.wongnai.com/p/1920x0/2023/06/20/fe089df9a442415daa69028b6b685516.jpg"
    },
    {
        "name": "สวนอาหารบ้านเนินน้ำ",
        "desc": "ร้านริมน้ำวิวสวย เมนูเด็ดคือกุ้งแม่น้ำเผา",
        "lat": 14.060,
        "lng": 101.390,
        "category": "ซีฟู้ด",
        "image": "https://img.wongnai.com/p/1920x0/2020/06/15/77d89c6091244cae977cd8f93178b770.jpg"
    }
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
    st.subheader(r["name"])
    st.write(r["desc"])
    if "image" in r:
        st.image(r["image"], caption=r["name"], use_column_width=True)
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
