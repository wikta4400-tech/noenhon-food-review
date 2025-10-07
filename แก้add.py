import streamlit as st

st.set_page_config(page_title="รีวิวร้านอาหารปราจีนบุรี", layout="wide")
st.title("🍽️ รวมร้านเด็ดจังหวัดปราจีนบุรี")

# ข้อมูลร้านอาหาร 20 ร้าน
restaurants = [
    {
        "name": "Bloom Restaurant @ Siamdasada",
        "desc": "ร้านอาหารฟิวชั่นในรีสอร์ตหรู บรรยากาศดี",
        "lat": 14.048, "lng": 101.378,
        "category": "ฟิวชั่น",
        "image": "https://img.wongnai.com/p/1920x0/2023/06/20/fe089df9a442415daa69028b6b685516.jpg"
    },
    {
        "name": "California Steak Restaurant",
        "desc": "ร้านสเต๊กชื่อดังในปราจีนบุรี",
        "lat": 14.049, "lng": 101.379,
        "category": "สเต๊ก",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/4d/california-steak.jpg"
    },
    {
        "name": "The Orchard Restaurant",
        "desc": "อาหารญี่ปุ่นและเมดิเตอร์เรเนียนในบรรยากาศรีสอร์ต",
        "lat": 14.050, "lng": 101.380,
        "category": "ญี่ปุ่น",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/4e/orchard-restaurant.jpg"
    },
    {
        "name": "Palm Sweet Home",
        "desc": "บาร์และอาหารเอเชียในบรรยากาศอบอุ่น",
        "lat": 14.051, "lng": 101.381,
        "category": "บาร์",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/4f/palm-sweet-home.jpg"
    },
    {
        "name": "Cafe Kantary 304",
        "desc": "คาเฟ่สไตล์โมเดิร์นในนิคม 304",
        "lat": 14.052, "lng": 101.382,
        "category": "คาเฟ่",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/50/cafe-kantary.jpg"
    },
    {
        "name": "Baan Nern Nam Restaurant",
        "desc": "ร้านอาหารไทยริมแม่น้ำ บรรยากาศดี",
        "lat": 14.053, "lng": 101.383,
        "category": "ไทย",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/51/baan-nern-nam.jpg"
    },
    {
        "name": "Story Telling House",
        "desc": "ร้านอาหารสุขภาพและไทยฟิวชั่น",
        "lat": 14.054, "lng": 101.384,
        "category": "สุขภาพ",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/52/story-telling-house.jpg"
    },
    {
        "name": "Big Mount Bistro & Restaurant",
        "desc": "ร้านอาหารและคาเฟ่สไตล์บิสโทร",
        "lat": 14.055, "lng": 101.385,
        "category": "บิสโทร",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/53/big-mount.jpg"
    },
    {
        "name": "Japan Station Sushi",
        "desc": "ร้านซูชิและอาหารญี่ปุ่นคุณภาพดี",
        "lat": 14.056, "lng": 101.386,
        "category": "ญี่ปุ่น",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/54/japan-station.jpg"
    },
    {
        "name": "Eat 'Em Up Kabinburi",
        "desc": "ร้านอาหารอิตาเลียนและไทยในกบินทร์บุรี",
        "lat": 14.057, "lng": 101.387,
        "category": "อิตาเลียน",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/55/eat-em-up.jpg"
    },
    {
        "name": "Dan Cafe / Baan Rai Dan Sawan",
        "desc": "คาเฟ่กลางสวนธรรมชาติ",
        "lat": 14.058, "lng": 101.388,
        "category": "คาเฟ่",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/56/dan-cafe.jpg"
    },
    {
        "name": "28 Days Off Specialty Coffee",
        "desc": "ร้านกาแฟพิเศษสำหรับสายดริป",
        "lat": 14.059, "lng": 101.389,
        "category": "กาแฟ",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/57/28-days-off.jpg"
    },
    {
        "name": "Hom Cafe",
        "desc": "คาเฟ่เบเกอรี่โฮมเมด",
        "lat": 14.060, "lng": 101.390,
        "category": "เบเกอรี่",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/58/hom-cafe.jpg"
    },
    {
        "name": "Lek-Was Somtam Shop",
        "desc": "ร้านส้มตำรสจัดจ้าน",
        "lat": 14.061, "lng": 101.391,
        "category": "อีสาน",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/59/lek-was.jpg"
    },
    {
        "name": "Triple 8 Cafe & Restaurant",
        "desc": "ร้านอาหารอิตาเลียนและคาเฟ่",
        "lat": 14.062, "lng": 101.392,
        "category": "อิตาเลียน",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/60/triple-8.jpg"
    },
    {
        "name": "De'Ya Cafe",
        "desc": "คาเฟ่สไตล์มินิมอล",
        "lat": 14.063, "lng": 101.393,
        "category": "คาเฟ่",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/61/de-ya.jpg"
    },
    {
        "name": "Pimlapas Korean BBQ",
        "desc": "ร้านปิ้งย่างเกาหลีในปราจีน",
        "lat": 14.064, "lng": 101.394,
        "category": "เกาหลี",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/62/pimlapas.jpg"
    },
    {
        "name": "Yellow Monday",
        "desc": "ร้านอาหารทะเลและคาเฟ่",
        "lat": 14.065, "lng": 101.395,
        "category": "ซีฟู้ด",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/63/yellow-monday.jpg"
    },
    {
        "name": "Lost Farm",
        "desc": "ร้านพิซซ่าและอาหารสุขภาพ",
        "lat": 14.066, "lng": 101.396,
        "category": "สุขภาพ",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/64/lost-farm.jpg"
    },
    {
        "name": "SAMMA Cafe’ House",
        "desc": "คาเฟ่บรรยากาศอบอุ่น",
        "lat": 14.067, "lng": 101.397,
        "category": "คาเฟ่",
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/1a/2b/3c/65/samma.jpg"
    }
]

# ระบบค้นหาและกรอง
search = st.text
