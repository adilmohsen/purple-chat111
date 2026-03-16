import streamlit as st
import json

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="مطبخ مريوم", layout="wide")

# 2. تصميم CSS احترافي (الخلفية من صورتج، تنسيق الأزرار، وتصغير كروت الأكلات)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        /* تعيين الصورة الخشبية الدافئة كخلفية ثابتة */
        background-image: url("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/454fa9d2e598bae3df9c21c1ccf14889.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        direction: rtl;
    }

    /* العنوان الرئيسي */
    .main-title {
        color: #f39c12; /* لون برتقالي دافئ يناسب الخشب */
        text-align: center;
        font-size: 50px;
        font-weight: 800;
        margin-bottom: 40px;
        text-shadow: 2px 2px 4px #000000; /* ظل لجعل الكلام واضحاً */
    }

    /* تنسيق الأزرار الموزعة 2 بجهة و2 بجهة */
    .stButton > button {
        width: 100%;
        height: 70px;
        font-size: 20px !important;
        background-color: rgba(255, 255, 255, 0.1); /* خلفية شفافة */
        color: #f1c40f; /* لون ذهبي */
        border: 2px solid rgba(243, 156, 18, 0.5); /* إطار شفاف */
        border-radius: 12px;
        backdrop-filter: blur(5px); /* تأثير ضبابي */
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.2);
        border-color: #f1c40f;
        transform: translateY(-3px);
    }

    /* تصغير كروت الأكلات */
    .recipe-card {
        background-color: rgba(0, 0, 0, 0.8); /* خلفية سوداء شفافة لبروز الكلام */
        padding: 15px; /* صغرت الـ Padding */
        border-radius: 15px;
        border: 1px solid #f39c12;
        margin-bottom: 15px; /* صغرت الـ Margin */
        text-align: right;
        direction: rtl;
        color: white;
    }
    
    .recipe-title {
        color: #f39c12;
        font-size: 20px; /* صغرت العنوان */
        margin-bottom: 5px;
    }

    .recipe-info {
        font-size: 14px; /* صغرت الخط */
        color: #ddd;
    }

    .suggestion {
        color: #f1c40f;
        font-weight: bold;
        font-size: 13px; /* صغرت خط البديل */
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# قائمة البدائل الذكية الموسعة والشاملة
alternatives = {
    # مواد أساسية
    "لحم": "دجاج أو فطر",
    "دهن": "زيت نباتي أو زبدة",
    "زيت": "زبدة أو دهن",
    "تمن": "برغل",
    "برغل": "تمن أو كينوا",
    "طحين": "نشاء أو طحين شوفان",
    "بيض": "موز مهروس (للحلو) أو زبادي (للفطاير)",
    "حليب": "زبادي مخفف بماء أو حليب بودرة بماء",
    
    # خضروات
    "سلق": "ورق عنب أو لهانة (ملفوف)",
    "باذنجان": "شجر (كوسا) أو بطاطا",
    "بطاطا": "جزر أو شجر",
    "طماطم": "معجون طماطم مخفف بماء أو عصير طماطم",
    "بصل": "كراث أو بصل أخضر",
    "ثوم": "ثوم بودرة",
    "بقدونس": "كزبرة",
    "نعناع": "ريحان",
    
    # حوامض وبهارات
    "ليمون": "مندوزي (ملح الليمون) أو خل",
    "خل": "ليمون",
    "دبس رمان": "تمر هندي أو عصير ليمون مع شكر",
    "هيل": "قرفة (دارسين)",
    "كاري": "كركم",
    "فلفل أسود": "فلفل حار",
    
    # حلويات
    "تمر": "جوز",
    "سمسم": "فستق حلبي مطحون",
    "جوز": "لوز أو فستق",
    "شكر": "عسل أو دبس تمر"
}

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'category' not in st.session_state: st.session_state.category = None

# تحميل البيانات
try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except:
    recipes = []

# --- الصفحة الرئيسية (تصميم الصورة الموزعة 2x2) ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-title">🍴 مطبخ مريوم الذكي</div>', unsafe_allow_html=True)
    
    # توزيع الأزرار بشكل متناسق (2 بجهة و2 بجهة)
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if st.button("🥘 أطباق رئيسية"):
            st.session_state.category, st.session_state.page = "اطباق رئيسية", 'filter'
            st.rerun()
        if st.button("🥗 مقبلات"):
            st.session_state.category, st.session_state.page = "مقبلات", 'filter'
            st.rerun()
    with col2:
        if st.button("🍰 حلويات"):
            st.session_state.category, st.session_state.page = "حلويات", 'filter'
            st.rerun()
        if st.button("🥦 خضروات"):
            st.session_state.category, st.session_state.page = "خضروات", 'filter'
            st.rerun()

# --- صفحة الفلترة والبدائل ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع للمطبخ"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown(f"<h2 style='text-align:right; color:white;'>شنو مواد متوفرة عندج للـ {st.session_state.category}؟</h2>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([ing for r in cat_recipes for ing in r['ingredients']])))
    
    user_ing = st.multiselect("اختاري المواد المتوفرة:", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        if user_ing:
            for res in cat_recipes:
                missing = [m for m in res['ingredients'] if m not in user_ing]
                
                # اقتراح إذا كانت كل المواد موجودة أو ناقص مادة وحدة بس
                if len(missing) <= 1:
                    st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                    st.markdown(f'<h3 class="recipe-title">{res["name"]}</h3>', unsafe_allow_html=True)
                    
                    if len(missing) == 1:
                        m_item = missing[0]
                        alt_text = alternatives.get(m_item, "مادة ثانية متوفرة عندج")
                        st.markdown(f'<p class="suggestion">💡 ناقصج {m_item}؟ ممكن تستخدمين {alt_text} بداله.</p>', unsafe_allow_html=True)
                    
                    st.markdown(f'<p class="recipe-info">💰 <b>التكلفة:</b> {res["cost"]}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="recipe-info">📖 <b>الطريقة:</b><br>{res["recipe"]}</p>', unsafe_allow_html=True)
                    st.image(res['image'], use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("حبيبتي مريوم، اختاري مادة على الأقل.")
