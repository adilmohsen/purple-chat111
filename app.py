import streamlit as st
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="مطبخ مريوم", layout="centered")

# 2. تصميم CSS احترافي (توسيط العناصر، تكبير الخط، وتنسيق الأزرار)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');

    [data-testid="stAppViewContainer"] {
        background-color: white;
        direction: rtl;
    }
    
    /* جعل كل النصوص بالعربي وفي المنتصف */
    .stMarkdown, h1, h2, h3, p {
        text-align: center !important;
        font-family: 'Cairo', sans-serif !important;
    }

    /* تنسيق الأزرار لتكون في المنتصف وكبيرة */
    .stButton > button {
        display: block;
        margin: 0 auto 15px auto; /* توسيط الزر */
        width: 80%;
        height: 80px;
        font-size: 28px !important; /* تكبير الخط */
        font-weight: bold;
        border-radius: 15px;
        background-color: #fdfaf5;
        color: #5d4037;
        border: 2px solid #d7ccc8;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background-color: #efebe9;
        border-color: #8d6e63;
        transform: scale(1.03);
    }

    /* كرت الأكلة وتنسيق الصور */
    .recipe-card {
        background-color: #fafafa;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #eee;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    img {
        border-radius: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# إدارة الصفحات
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'category' not in st.session_state: st.session_state.category = None

# تحميل البيانات (تأكدي مريوم إن ملف recipes.json مرفوع بـ GitHub)
try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except:
    recipes = []

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    # أيقونة علوية فخمة
    st.image("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/image_bbb3fd.png", use_container_width=True)
    
    st.markdown("<h1 style='color:#5d4037; font-size: 50px;'>🍲 قائمة المطبخ</h1>", unsafe_allow_html=True)
    
    # الأزرار في المنتصف
    if st.button("🥘 أطباق رئيسية"):
        st.session_state.category = "اطباق رئيسية"
        st.session_state.page = 'filter'
        st.rerun()
    if st.button("🍰 حلويات"):
        st.session_state.category = "حلويات"
        st.session_state.page = 'filter'
        st.rerun()
    if st.button("🥗 مقبلات"):
        st.session_state.category = "مقبلات"
        st.session_state.page = 'filter'
        st.rerun()
    if st.button("🥦 خضروات"):
        st.session_state.category = "خضروات"
        st.session_state.page = 'filter'
        st.rerun()

    # أيقونة سفلية
    st.image("https://images.fineartamerica.com/images/artworkimages/medium/1/baking-watercolor-transparent-cherie-w-fine-art.png", use_container_width=True)

# --- صفحة الفلترة ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown(f"<h2 style='color:#8d6e63;'>شنو عندج مواد للـ {st.session_state.category}؟</h2>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([ing for r in cat_recipes for ing in r['ingredients']])))
    
    user_ing = st.multiselect("اختاري من القائمة:", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        if user_ing:
            for res in cat_recipes:
                if any(item in user_ing for item in res['ingredients']):
                    st.markdown(f"""
                    <div class="recipe-card">
                        <h2 style="color:#5d4037;">{res['name']}</h2>
                        <p style="font-size:20px;"><b>💰 التكلفة:</b> {res['cost']}</p>
                        <p style="font-size:20px;"><b>📖 الطريقة:</b><br>{res['recipe']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    # عرض الصورة
                    st.image(res['image'], use_container_width=True)
                    st.markdown("---")
        else:
            st.warning("حبيبتي مريوم، لازم تختارين مكون واحد على الأقل.")
