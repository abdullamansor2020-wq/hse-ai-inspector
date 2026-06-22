import streamlit as st
from groq import Groq
from PIL import Image
import io
import base64

# إعدادات واجهة التطبيق
st.set_page_config(
    page_title="مفتش السلامة الذكي الاحترافي | HSE AI Groq", 
    layout="wide", 
    page_icon="🦺"
)

# التنسيق والتصميم الاحترافي لسهولة القراءة بروح هندسية
css_style = """
<style>
.main { text-align: right; direction: rtl; }
div.stButton > button:first-child {
    background-color: #00a86b; color: white; width: 100%; font-size: 20px; font-weight: bold;
}
.report-box { padding: 15px; border-radius: 10px; background-color: #f8f9fa; border-right: 5px solid #00a86b; margin-bottom: 15px; direction: rtl; text-align: right; }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

st.title("🦺 نظام فحص ومطابقة مخاطر السلامة (HSE) المستقر")
st.write("نظام ذكي متكامل يعمل عبر المحرك المستقر لـ Groq لفحص وتحليل صور المواقع الإنشائية وإصدار التقارير الهندسية الفورية مجاناً.")

# إدخال مفتاح الـ API الخاص بـ Groq في القائمة الجانبية
st.sidebar.header("🔑 إعدادات منصة Groq")
groq_api_key = st.sidebar.text_input("أدخل مفتاح Groq API الخاص بك:", type="password")

st.sidebar.markdown("""
---
**💡 خطوات التشغيل السريع:**
1. أدخل مفتاح Groq الخاص بك.
2. ارفع صور الموقع الميدانية.
3. أضف توجيهاتك الخاصة ثم اضغط ابدأ التحليل الفوري.
""")

# تقسيم واجهة المستخدم لرفع البيانات ومعاينتها
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 رفع صور الموقع الإنشائي")
    uploaded_files = st.file_uploader(
        "اسحب وأفلت الصور هنا (يمكنك رفع عدة صور للموقع دفعة واحدة):", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )
    
    st.markdown("---")
    user_comments = st.text_area(
        "✍️ إضافة توجيهاتك أو تعليقاتك الخاصة بالموقع (ليأخذها المحرك في الحسبان):", 
        placeholder="مثال: ركز على حواجز الحماية حول الحفر، أو تجاهل غياب الخوذات لأن هذه المنطقة مخصصة للاستراحة فقط...",
        height=150
    )

with col2:
    st.subheader("📊 التقرير الهندسي الفوري (HSE Analytics)")
    
    if not groq_api_key:
        st.warning("⚠️ يرجى إدخال مفتاح Groq API في القائمة الجانبية لتنشيط الفحص الفوري.")
    elif uploaded_files and groq_api_key:
        
        if st.button("🚀 ابدأ الفحص الفوري الممتد وتوليد التقرير"):
            final_report_text = "=== تقرير فحص السلامة المهنية والمطابقة الذكي (Groq) ===\n\n"
            
            # تهيئة عميل Groq
            client = Groq(api_key=groq_api_key)
            
            with st.spinner("جاري تحليل الصور وتطبيق توجيهاتك الهندسية عبر الموديل المستقر..."):
                
                # صياغة التوجيه الهندسي المحكم
                prompt = f"""
                You are a senior professional HSE Auditor and Safety Inspector. Analyze the uploaded construction site image.
                
                CRITICAL USER CONTEXT/COMMENTS TO INTEGRATE:
                "{user_comments}"
                
                Provide a structured, professional inspection report IN ARABIC. For each hazard found, create a clear structure:
                1. مستوى الخطورة (عالي جداً، متوسط، منخفض)
                2. المخالفة/الخطر المرصود بدقة في الصورة
                3. الإجراء التصحيحي الفوري المطلوب (Corrective Action)
                4. المعيار الدولي المتوافق معه (مثل OSHA أو معايير السلامة الإنشائية العالمية)
                
                Ensure your analysis takes the user'
