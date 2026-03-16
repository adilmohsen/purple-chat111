import streamlit as st
import json

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="مطبخ مريوم", page_icon="🍲", layout="centered")

# 2. تصميم CSS لجعل الواجهة كلاسيكية ونظيفة مثل الصورة
# جعلنا الخلفية نظيفة واستخدمنا حدوداً خفيفة وأنيقة للأزرار.
page_style = """
<style>
/* تعيين خلفية الموقع لتكون بيضاء ونظيفة */
[data-testid="stAppViewContainer"] {
    background-color: white;
}

/* تنسيق الكلام ليكون عربي ومن اليمين */
.main {
    text-align: right;
    direction: rtl;
    color: black;
}

/* الأيقونات الكلاسيكية في الأعلى والأسفل */
.header-icon {
    width: 250px;
    display: block;
    margin: 20px auto 40px auto;
}
.footer-icon {
    width: 200px;
    display: block;
    margin: 50px auto;
}

/* تنسيق الأزرار المستطيلة ليكون كلاسيكي وأنيق */
div.stButton > button {
    width: 100%;
    height: 70px;
    font-size: 22px !important;
    font-weight: bold;
    border-radius: 12px;
    margin-bottom: 20px;
    background-color: transparent; /* خلفية شفافة */
    color: #4a3e2a; /* لون بني داكن */
    border: 2px solid #bda88a; /* إطار بيج كلاسيكي */
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: rgba(189, 168, 138, 0.1); /* تعتيم قليل */
    border-color: #a08c72;
    transform: scale(1.02);
}

/* حاوية الأكلات */
.recipe-box {
    background-color: rgba(243, 237, 230, 0.8); /* بيج شفاف جداً */
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(189, 168, 138, 0.3); /* إطار شفاف جداً */
    margin-top: 20px;
    color: black;
    direction: rtl;
    text-align: right;
}

/* تنسيق العناوين داخل البطاقة */
.recipe-title {
    color: #4a3e2a;
    font-size: 24px;
    margin-bottom: 10px;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# 3. الأيقونة الكلاسيكية العلوية (مثل الصورة)
# استخدمنا صورة مماثلة لفكرة قبعة الطاهي والأدوات.
st.image("https://images.fineartamerica.com/images/artworkimages/medium/1/chef-hat-spoons-vintage-wood-slice-print-v-2-cherie-w-fine-art-transparent.png", class="header-icon")

# 4. عنوان الموقع الكلاسيكي
st.markdown('<h1 style="text-align: center; color: #4a3e2a; font-size: 40px; margin-bottom: 50px;">🍲 مطبخ مريوم الحلوة</h1>', unsafe_allow_html=True)

# 5. تحميل بيانات الأكلات
try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except Exception as e:
    st.error("أكو مشكلة بملف الـ JSON، تأكدي من رفعه بشكل صحيح مريوم.")
    recipes = []

# 6. الأزرار الكبيرة في المنتصف
btn_main = st.button("🍲 أطباق رئيسية")
btn_dessert = st.button("🍰 حلويات")
btn_side = st.button("🥗 مقبلات")
btn_veggies = st.button("🥦 خضروات")

# 7. الأيقونة الكلاسيكية السفلية (مثل الصورة)
# استخدمنا صورة مماثلة لفكرة البييض والحليب.
st.image("https://images.fineartamerica.com/images/artworkimages/medium/1/baking-watercolor-transparent-cherie-w-fine-art.png", class="footer-icon")

# 8. منطق العرض
selected_cat = None
if btn_main: selected_cat = "اطباق رئيسية"
if btn_dessert: selected_cat = "حلويات"
if btn_side: selected_cat = "مقبلات"
if btn_veggies: selected_cat = "خضروات"

if selected_cat:
    st.markdown(f'<h2 style="color: #4a3e2a; text-align: right;">📋 قائمة {selected_cat}:</h2>', unsafe_allow_html=True)
    
    filtered = [r for r in recipes if r['category'] == selected_cat]
    
    if filtered:
        for res in filtered:
            with st.container():
                st.markdown(f"""
                <div class="recipe-box">
                    <h2 class="recipe-title">✨ {res['name']}</h2>
                    <p style="font-size: 18px; color: black;">💰 <b>التكلفة:</b> {res['cost']}</p>
                    <p style="font-size: 18px; color: black;">📖 <b>طريقة التحضير:</b><br>{res['recipe']}</p>
                </div>
                """, unsafe_allow_html=True)
                # التأكد من استخدام الصور العراقية من ملف الـ JSON
                st.image(res['image'], use_container_width=True)
                st.write("---")
    else:
        st.info("هذا القسم حالياً فارغ، ضيفي أكلات بملف الـ JSON حتى تظهر هنا.")
