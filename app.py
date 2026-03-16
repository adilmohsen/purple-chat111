import streamlit as st
import json
import os

# إعدادات الصفحة
st.set_page_config(page_title="مخطط الوجبات الذكي", page_icon="🍲", layout="centered")

# تنسيق CSS لجعل الكلام من اليمين لليسار (للغة العربية) ولون خلفية أنيق
st.markdown("""
    <style>
    .stApp { text-align: right; direction: rtl; }
    div[data-baseweb="select"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("👨‍🍳 مخطط الوجبات الذكي")
st.subheader("مريوم، شنو عندج مكونات بالثلاجة؟")

# التأكد من وجود ملف البيانات أو إنشاء بيانات تجريبية إذا نقص
if not os.path.exists('recipes.json'):
    default_recipes = [
        {"name": "مخلمة بيض وطماطم", "ingredients": ["بيض", "طماطم", "بصل"], "cost": "رخيص"},
        {"name": "مجدرة رز وعدس", "ingredients": ["رز", "عدس", "بصل"], "cost": "رخيص"},
        {"name": "معكرونة بالصلصة", "ingredients": ["معكرونة", "طماطم", "ثوم"], "cost": "رخيص"}
    ]
    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(default_recipes, f, ensure_ascii=False)

# تحميل البيانات
with open('recipes.json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)

# استخراج قائمة المكونات
all_ing = sorted(list(set([ing for res in recipes for ing in res['ingredients']])))

# واجهة الاختيار
selected_items = st.multiselect("اختاري المكونات المتوفرة حالياً:", all_ing)

if st.button("اكتشفي الأكلات الممكنة"):
    if selected_items:
        results = [r for r in recipes if all(item in selected_items for item in r['ingredients'])]
        
        if results:
            st.success(f"لقينا لج {len(results)} وجبات تكدرين تسويها!")
            for res in results:
                with st.expander(f"🍴 {res['name']}"):
                    st.write(f"✅ **المكونات:** {', '.join(res['ingredients'])}")
                    st.write(f"💰 **التكلفة التقديرية:** {res['cost']}")
        else:
            st.warning("ماكو وجبة مطابقة تماماً، جربي تضيفين مكونات أكثر.")
    else:
        st.info("حطي المكونات أولاً مريوم.")
