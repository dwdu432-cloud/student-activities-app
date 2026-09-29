import streamlit as st
import sqlite3
import os
import pandas as pd
import base64

# 1. إعداد الصفحة
st.set_page_config(
    page_title="نظام الأنشطة الطلابية",
    page_icon="🎓",
    layout="centered"
)

# دالة تحويل الصور إلى Base64 لعرضها بسلاسة داخل HTML
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

img_uni = get_base64_image("logo_uni.png")
img_dept = get_base64_image("logo_dept.png")

logo_uni_html = f'<img src="data:image/png;base64,{img_uni}" style="max-height: 65px; width: auto;">' if img_uni else ''
logo_dept_html = f'<img src="data:image/png;base64,{img_dept}" style="max-height: 65px; width: auto;">' if img_dept else ''

# CSS معدل ومحسّن خصيصاً للشاشات الصغير (Mobile-Friendly)
st.markdown("""
    <style>
    /* خلفية متناسقة للواجهة */
    .stApp {
        background-color: #f8f9fa !important;
        color: #1a202c !important;
    }
    
    /* حاوية الهيدر */
    .header-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        padding: 5px 0;
        gap: 5px;
    }
    
    /* النص الأوسط لمنع التفاف الكلمات */
    .header-text {
        text-align: center;
        white-space: nowrap; /* يمنع انكسار الكلمات مثل المستق-بل */
        flex-shrink: 0;
    }
    
    .header-text h3 {
        font-size: 1.15rem !important;
        color: #1e3a8a !important;
        margin: 0 !important;
        font-weight: 800;
        line-height: 1.2;
    }
    
    .header-text h5 {
        font-size: 0.8rem !important;
        color: #4b5563 !important;
        margin: 3px 0 0 0 !important;
        font-weight: 600;
        line-height: 1.2;
    }

    /* أزرار وكروت النظام */
    .stButton>button {
        background-color: #1e3a8a !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold;
        width: 100%;
    }
    
    .score-card {
        background-color: #ffffff;
        border-right: 5px solid #1e3a8a;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== عرض الهيدر الموحد ====================
st.markdown(f"""
    <div class="header-box">
        <div>{logo_uni_html}</div>
        <div class="header-text">
            <h3>جامعة المستقبل</h3>
            <h5>قسم هندسة تقنيات الذكاء الاصطناعي</h5>
        </div>
        <div>{logo_dept_html}</div>
    </div>
    <hr style="margin: 12px 0 20px 0; border-top: 1px solid #e5e7eb;">
""", unsafe_allow_html=True)

# ==================== قاعدة البيانات ====================
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        activity_title TEXT NOT NULL,
        file_path TEXT NOT NULL,
        status TEXT DEFAULT 'قيد المراجعة',
        points INTEGER DEFAULT 0,
        FOREIGN KEY (student_id) REFERENCES students (student_id)
    )
''')
conn.commit()

cursor.execute("SELECT COUNT(*) FROM activities")
if cursor.fetchone()[0] == 0:
    default_activities = [("ورشة الذكاء الاصطناعي",), ("دورة برمجة C++",), ("ورشة الـ IoT",)]
    cursor.executemany("INSERT INTO activities (title) VALUES (?)", default_activities)
    conn.commit()

os.makedirs("uploaded_certificates", exist_ok=True)

query_params = st.query_params
is_admin_route = query_params.get("admin") == "true"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'student_id' not in st.session_state:
    st.session_state.student_id = None
if 'student_name' not in st.session_state:
    st.session_state.student_name = None

# ==================== 1. لوحة رئيس القسم ====================
if is_admin_route:
    st.markdown("<h2 style='text-align:center;'>⚙️ لوحة تحكم رئيس القسم</h2>", unsafe_allow_html=True)

    if not st.session_state.get('admin_logged_in', False):
        with st.form("admin_login_form"):
            admin_pass = st.text_input("كلمة المرور الخاصة برئيس القسم:", type="password")
            submit_admin = st.form_submit_button("تسجيل الدخول")

            if submit_admin:
                if admin_pass == "1234":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("كلمة المرور غير صحيحة!")
    else:
        st.sidebar.write("⚙️ **حساب رئيس القسم**")
        if st.sidebar.button("تسجيل الخروج"):
            st.session_state.admin_logged_in = False
            st.rerun()

        with st.expander("➕ إضافة نشاط / ورشة جديدة"):
            new_act = st.text_input("اسم الورشة الجديدة:")
            if st.button("إضافة الورشة"):
                if new_act.strip():
                    cursor.execute("INSERT INTO activities (title) VALUES (?)", (new_act.strip(),))
                    conn.commit()
                    st.success(f"تمت إضافة ({new_act}) بنجاح!")
                    st.rerun()

        st.subheader("📥 الطلبات المعلقة للمراجعة")
        query = '''
            SELECT s.id, st.full_name, s.student_id, s.activity_title, s.file_path 
            FROM submissions s
            JOIN students st ON s.student_id = st.student_id
            WHERE s.status = 'قيد المراجعة'
        '''
        cursor.execute(query)
        pending_list = cursor.fetchall()

        if pending_list:
            for sub_id, full_name, std_id, act_title, f_path in pending_list:
                st.markdown("---")
                st.write(f"👤 **الطالب:** {full_name} ({std_id})")
                st.write(f"🎯 **النشاط:** {act_title}")
                if os.path.exists(f_path):
                    if f_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                        st.image(f_path, use_container_width=True)
                    else:
                        st.write("📄 الملف المرفق PDF")
                
                pts = st.number_input(f"الدرجة للطلب #{sub_id}", min_value=1, max_value=20, value=5, key=f"pts_{sub_id}")
                if st.button(f"اعتماد الدرجة #{sub_id}", key=f"btn_{sub_id}"):
                    cursor.execute("UPDATE submissions SET status = 'معتمد', points = ? WHERE id = ?", (pts, sub_id))
                    conn.commit()
                    st.success("تم اعتماد الشهادة ورصد الدرجة!")
                    st.rerun()
        else:
            st.info("لا توجد طلبات معلقة بانتظار المراجعة حالياً.")

        st.subheader("📋 السجل العام لجميع الطلبات")
        df_all = pd.read_sql_query('''
            SELECT s.id AS 'رقم الطلب', st.full_name AS 'اسم الطالب', s.student_id AS 'الرقم الجامعي', 
                   s.activity_title AS 'النشاط', s.status AS 'الحالة', s.points AS 'الدرجة'
            FROM submissions s
            JOIN students st ON s.student_id = st.student_id
        ''', conn)
        st.dataframe(df_all, use_container_width=True)

# ==================== 2. واجهة الطلاب ====================
else:
    if not st.session_state.logged_in:
        st.markdown("<h2 style='text-align: center; color: #1e293b; font-weight: 800; margin-bottom: 5px;'>🎓 بوابة نظام الأنشطة الطلابية</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.95rem;'>مرحباً بك عزيزي الطالب، يرجى تسجيل الدخول لمتابعة أنشطتك.</p>", unsafe_allow_html=True)

        with st.form("student_login_form"):
            s_id = st.text_input("الرقم الجامعي:")
            s_name = st.text_input("اسم الطالب الرباعي:")
            submit_login = st.form_submit_button("دخول الطالب")

            if submit_login:
                if s_id.strip() and s_name.strip():
                    cursor.execute("INSERT OR REPLACE INTO students (student_id, full_name) VALUES (?, ?)", (s_id.strip(), s_name.strip()))
                    conn.commit()
                    
                    st.session_state.logged_in = True
                    st.session_state.student_id = s_id.strip()
                    st.session_state.student_name = s_name.strip()
                    st.rerun()
                else:
                    st.error("يرجى إدخال الرقم الجامعي والاسم كاملاً.")

    else:
        st.sidebar.write(f"👤 **الطالب:** {st.session_state.student_name}")
        st.sidebar.write(f"🆔 **الرقم الجامعي:** {st.session_state.student_id}")
        if st.sidebar.button("تسجيل الخروج"):
            st.session_state.logged_in = False
            st.session_state.student_id = None
            st.session_state.student_name = None
            st.rerun()

        st.title("📄 لوحة الطالب")

        cursor.execute("SELECT SUM(points) FROM submissions WHERE student_id = ? AND status = 'معتمد'", (st.session_state.student_id,))
        total_points = cursor.fetchone()[0] or 0

        st.markdown(f"""
            <div class="score-card">
                <h3 style="margin:0; color:#1e3a8a !important;">مجموع درجاتك المعتمدة: {total_points} درجة</h3>
                <p style="margin:5px 0 0 0; color:#6b7280 !important;">تضاف الدرجات تلقائياً فور توثيق الشهادة من القسم.</p>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📤 رفع شهادة جديدة", "📊 حالة الطلبات"])

        with tab1:
            cursor.execute("SELECT title FROM activities")
            activities = [row[0] for row in cursor.fetchall()]

            with st.form("upload_form", clear_on_submit=True):
                selected_activity = st.selectbox("اختر النشاط / الورشة:", activities)
                uploaded_file = st.file_uploader("ارفق صورة الشهادة (PNG, JPG, PDF):", type=['png', 'jpg', 'jpeg', 'pdf'])
                submit_cert = st.form_submit_button("إرسال الشهادة")

                if submit_cert:
                    if uploaded_file and selected_activity:
                        cursor.execute(
                            "SELECT COUNT(*) FROM submissions WHERE student_id = ? AND activity_title = ?", 
                            (st.session_state.student_id, selected_activity)
                        )
                        already_submitted = cursor.fetchone()[0]

                        if already_submitted > 0:
                            st.error("⚠️ تنبيه: لقد قمت برفع شهادة لهذا النشاط سابقاً!")
                        else:
                            file_ext = os.path.splitext(uploaded_file.name)[1]
                            file_name = f"{st.session_state.student_id}_{selected_activity.replace(' ', '_')}{file_ext}"
                            file_path = os.path.join("uploaded_certificates", file_name)
                            
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())

                            cursor.execute(
                                "INSERT INTO submissions (student_id, activity_title, file_path) VALUES (?, ?, ?)",
                                (st.session_state.student_id, selected_activity, file_path)
                            )
                            conn.commit()
                            st.success("تم رفع الشهادة بنجاح! وهي الآن قيد المراجعة.")
                    else:
                        st.error("يرجى اختيار النشاط وإرفاق ملف الشهادة.")

        with tab2:
            st.subheader("سجل الشهادات المرفوعة")
            df_sub = pd.read_sql_query(
                "SELECT activity_title AS 'النشاط', status AS 'حالة الطلب', points AS 'الدرجة' FROM submissions WHERE student_id = ?",
                conn, params=(st.session_state.student_id,)
            )
            if not df_sub.empty:
                st.dataframe(df_sub, use_container_width=True)
            else:
                st.info("لم تقم برفع أي شهادة حتى الآن.")