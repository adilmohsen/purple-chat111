import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="محادثة بنون الحلوة", page_icon="💜")

# التنسيق البنفسجي (CSS)
st.markdown(f"""
    <style>
    /* تغيير الخلفية للون بنفسجي فاتح أو صورة بنفسجية */
    [data-testid="stAppViewContainer"] {{
        background-color: #f3e5f5; 
        background-image: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
    }}
    
    /* تنسيق أزرار البنفسجي */
    .stButton>button {{
        background-color: #9c27b0 !important;
        color: white !important;
        border-radius: 20px !important;
    }}
    
    /* تنسيق نص العنوان */
    h1 {{
        color: #7b1fa2 !important;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# المخزن المشترك (الذاكرة المشتركة للكل)
@st.cache_resource
def get_global_messages():
    return []

all_msgs = get_global_messages()

# --- شاشة تسجيل الدخول ---
if "user_name" not in st.session_state:
    st.title("💜 أهلاً بيكم بچات بنون الحلوة")
    name_input = st.text_input("لطفاً، ادخل اسمك المستعار:")
    if st.button("دخول للدردشة"):
        if name_input:
            st.session_state.user_name = name_input
            st.rerun()
        else:
            st.error("الاسم مطلوب للدخول!")
    st.stop()

# --- واجهة الچات بعد تسجيل الدخول ---

# القائمة الجانبية
st.sidebar.title(f"المستخدم: {st.session_state.user_name} ✨")
if st.sidebar.button("مسح السجل 🗑️"):
    all_msgs.clear()
    st.rerun()

if st.sidebar.button("خروج ⬅️"):
    del st.session_state.user_name
    st.rerun()

st.title("💜 بنون الحلوة ✨")

# عرض الرسائل
for chat in all_msgs:
    with st.chat_message("user"):
        st.write(f"**{chat['name']}:** {chat['msg']}")

# صندوق الكتابة
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    all_msgs.append({"name": st.session_state.user_name, "msg": prompt})
    st.rerun()