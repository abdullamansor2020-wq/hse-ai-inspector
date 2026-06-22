import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# إعدادات واجهة التطبيق
st.set_page_config(
    page_title="مفتش السلامة الذكي | HSE AI Auditor", 
    layout="wide", 
    page_icon="🦺"
)

# التنسيق والتصميم الاحترافي (تم تصحيح الدالة هنا)
css_style = """
<style>
.main { text-align: right; direction: rtl; }
div.stButton > button:first-child {
    background-color: #FF4B4B; color: white; width: 100%; font-size: 20px; font-weight: bold;
}
.report-box { padding: 15px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 15px; direction: rtl; text-align: right; }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

st.title("🦺 نظام فحص وتقييم مخاطر الأمن والسلامة بالذكاء الاصطناعي")
st.write("مرحباً بك. هذا النظام يساعدك على رفع صور الموقع الإنشائية وتفنيد المخالفات بناءً على معايير السلامة الدولية وتوجيهاتك الخاصة.")

# إدخل مفتاح الـ API بأمان من قبل المستخدم
st.sidebar.header("🔑 إعدادات النظام")
api_key = st.sidebar.text_input("أدخل مفتاح Google Gemini API الخاص بك:", type="password")
selected_model = st.sidebar.selectbox("اختر محرك الذكاء الاصطناعي:", ["gemini-1.5-flash (أسرع)", "gemini-1.5-pro (أدق وأعمق)"])

st.sidebar.markdown("""
---
**💡 كيف يعمل النظام؟**
1. ارفع صور الموقع.
2. أضف أي ملاحظات سياقية (مثلاً: الموقع تحت الإنشاء، أو السقالات مرخصة).
3. اضغط تحليل، وسيقوم الذكاء الاصطناعي بدمج ملاحظاتك مع تفاصيل الصورة لتوليد التقرير.
""")

# تقسيم واجهة المستخدم
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 رفع صور الموقع والمعاينة")
    uploaded_files = st.file_uploader(
        "اسحب وأفلت الصور هنا أو تصفح من جهازك (يمكنك اختيار عدة صور):", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )
    
    st.markdown("---")
    user_comments = st.text_area(
        "✍️ ملاحظات وتعليقات خاصة بالموقع (سيتم دمجها في التحليل):", 
        placeholder="مثال: خذ بعين الاعتبار أن العمال يرتدون أحزمة أمان ولكن المشكلة في نقطة التثبيت، أو ركز على السقالات بالموقع...",
        height=150
    )

with col2:
    st.subheader("📊 تقرير فحص السلامة (HSE Report)")
    
    if not api_key:
        st.warning("⚠️ يرجى إدخال مفتاح الـ API الخاص بك في القائمة الجانبية لتفعيل النظام.")
    elif uploaded_files and api_key:
        # تفعيل الـ API
        model_name = "gemini-1.5-flash" if "flash" in selected_model else "gemini-1.5-pro"
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        if st.button("🚀 ابدأ التحليل الفوري واصدار التقرير"):
            final_report_text = "=== تقرير فحص السلامة المهنية الذكي ===\n\n"
            
            with st.spinner("جاري فحص الصور ومطابقتها وتطبيق تعليقاتك..."):
                
                # صياغة الأمر الهندسي المحكم للذكاء الاصطناعي
                prompt = f"""
                You are a senior professional HSE Auditor and Safety Inspector. Analyze the uploaded construction site image.
                
                CRITICAL USER CONTEXT/COMMENTS TO INTEGRATE:
                "{user_comments}"
                
                Provide a structured, professional inspection report IN ARABIC. For each hazard found, create a clear structure:
                1. مستوى الخطورة (عالي جداً، متوسط، منخفض)
                2. المخالفة/الخطر المرصود بدقة
                3. الإجراء التصحيحي الفوري المطلوب (Corrective Action)
                4. المعيار الدولي المتوافق معه (مثل OSHA أو معايير السلامة الإنشائية العالمية)
                
                Ensure your analysis takes the user's comments into consideration. If the user provided a comment clearing a potential hazard, acknowledge it and adjust the risk rating accordingly.
                """
                
                for idx, file in enumerate(uploaded_files):
                    img = Image.open(file)
                    st.image(img, caption=f"صورة رقم {idx+1}: {file.name}", use_column_width=True)
                    
                    # استدعاء الذكاء الاصطناعي للتحليل (وتم تصحيح الدالة هنا أيضاً)
                    try:
                        response = model.generate_content([prompt, img])
                        analysis_result = response.text
                        
                        st.markdown(f"#### 📝 نتيجة فحص الصورة {idx+1}:")
                        st.markdown(f"<div class='report-box'>{analysis_result}</div>", unsafe_allow_html=True)
                        
                        final_report_text += f"--- تحليل الصورة رقم {idx+1} ({file.name}) ---\n{analysis_result}\n\n"
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء تحليل الصورة {idx+1}: {str(e)}")
                
                st.session_state['download_ready'] = final_report_text
                st.success("✅ تم الانتهاء من تحليل كافة الصور ومطابقتها بنجاح!")

    elif not uploaded_files:
        st.info("💡 في انتظار رفع الصور لبدء عملية الفحص والتحليل الذكي.")

# زر تحميل التقرير النهائي
if 'download_ready' in st.session_state:
    st.markdown("---")
    st.subheader("💾 حفظ وتصدير التقرير")
    st.download_button(
        label="📥 تحميل التقرير النهائي كملف نصي احترافي",
        data=st.session_state['download_ready'].encode('utf-8-sig'),
        file_name="HSE_Inspection_Report.txt",
        mime="text/plain"
    )
