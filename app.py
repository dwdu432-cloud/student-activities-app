import streamlit as st
import sqlite3
import os
import pandas as pd
import base64

# كود لإخفاء العناصر غير المرغوبة (الهيدر، الفوتر، وعلامة Hosted with Streamlit)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            div[data-testid="stDecoration"] {display: none;}
            .viewerBadge_container__1S-td {display: none !important;}
            div[class*="viewerBadge"] {display: none !important;}
            a[class*="viewerBadge"] {display: none !important;}
            iframe[title="streamlit_badge"] {display: none !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 1. إعداد الصفحة
st.set_page_config(
    page_title="Student Activities System",
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
    /* 1. إعدادات خلفية التطبيق والخطوط */
    .stApp {
        background-color: #f8f9fa !important;
        color: #1a202c !important;
    }

    /* 2. تصميم الهيدر التفاعلي (Responsive Header) */
    .header-box {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
        padding: 5px 0 !important;
        gap: 8px !important;
    }

    .header-logo {
        flex: 0 0 auto !important;
        display: flex !important;
        align-items: center !important;
    }

    .header-logo img {
        height: 55px !important;
        width: auto !important;
        object-fit: contain !important;
    }

    .header-text {
        flex: 1 1 auto !important;
        text-align: center !important;
        padding: 0 5px !important;
    }

    .header-text h3 {
        font-size: 1.15rem !important;
        color: #1e3a8a !important;
        margin: 0 !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
    }

    .header-text h5 {
        font-size: 0.8rem !important;
        color: #4b5563 !important;
        margin: 3px 0 0 0 !important;
        font-weight: 600 !important;
        line-height: 1.2 !important;
    }

    /* 3. تعديل حجم الهيدر خصيصاً للشاشات الصغيرة (الموبايل) */
    @media (max-width: 600px) {
        .header-logo img {
            height: 40px !important;
        }
        .header-text h3 {
            font-size: 0.85rem !important;
            white-space: nowrap !important;
        }
        .header-text h5 {
            font-size: 0.6rem !important;
            white-space: nowrap !important;
        }
    }

    /* 4. إصلاح حقول الإدخال ومنع السواد في الموبايل واللابتوب */
    div[data-baseweb="input"], input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-radius: 8px !important;
    }

    .stTextInput input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
    }

    .stTextInput label p, label[data-testid="stWidgetLabel"] p {
        color: #1e293b !important;
        font-weight: 600 !important;
    }

    /* 5. الأزرار */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button {
        background-color: #1e3a8a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        width: 100% !important;
    }

    /* 6. بطاقة إجمالي النقاط */
    .score-card {
        background-color: #ffffff;
        border-left: 5px solid #1e3a8a;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* 7. إخفاء زوائد Streamlit والشارة الحمراء بالكامل */
    #MainMenu, header, footer, 
    div[data-testid="stHeader"], 
    div[data-testid="stToolbar"],
    [data-testid="manage-app-button"],
    .stAppDeployButton,
    div[class*="viewerBadge"], 
    iframe[title="streamlit_badge"] {
        display: none !important;
        visibility: hidden !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== عرض الهيدر الموحد ====================
st.markdown(f"""
    <div class="header-box">
        <div class="header-logo">{logo_uni_html}</div>
        <div class="header-text">
            <h3>Al-Mustaqbal University</h3>
            <h5>Department of Artificial Intelligence Engineering</h5>
        </div>
        <div class="header-logo">{logo_dept_html}</div>
    </div>
    <hr style="margin: 10px 0 20px 0; border: none; border-top: 1px solid #e2e8f0;">
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
        status TEXT DEFAULT 'Under Review',
        points INTEGER DEFAULT 0,
        rejection_reason TEXT DEFAULT '',
        FOREIGN KEY (student_id) REFERENCES students (student_id)
    )
''')
conn.commit()

# إضافة عمود rejection_reason إذا كانت قاعدة البيانات قديمة
try:
    cursor.execute("ALTER TABLE submissions ADD COLUMN rejection_reason TEXT DEFAULT ''")
    conn.commit()
except sqlite3.OperationalError:
    pass  # العمود موجود بالفعل

cursor.execute("SELECT COUNT(*) FROM activities")
if cursor.fetchone()[0] == 0:
    default_activities = [("AI Workshop",), ("C++ Programming Course",), ("IoT Workshop",)]
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
    st.markdown("<h2 style='text-align:center;'>⚙️ Department Head Dashboard</h2>", unsafe_allow_html=True)

    if not st.session_state.get('admin_logged_in', False):
        with st.form("admin_login_form"):
            admin_pass = st.text_input("Department Head Password:", type="password")
            submit_admin = st.form_submit_button("Login")

            if submit_admin:
                if admin_pass == "1234":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid password!")
    else:
        st.sidebar.write("⚙️ **Department Head Account**")
        if st.sidebar.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        with st.expander("➕ Add New Activity / Workshop"):
            new_act = st.text_input("Name of the new workshop:")
            if st.button("Add Workshop"):
                if new_act.strip():
                    cursor.execute("INSERT INTO activities (title) VALUES (?)", (new_act.strip(),))
                    conn.commit()
                    st.success(f"Successfully added ({new_act})!")
                    st.rerun()

        # ==================== الفلترة والبحث المتقدم ====================
        st.subheader("🔍 Search & Filter Requests")
        col_search, col_status, col_activity = st.columns([2, 1, 1])

        with col_search:
            search_query = st.text_input("Search by Student Name or ID:", placeholder="Type name or ID...")

        with col_status:
            status_filter = st.selectbox("Filter Status:", ["All", "Under Review", "Approved", "Rejected"])

        cursor.execute("SELECT title FROM activities")
        all_activities = ["All Activities"] + [row[0] for row in cursor.fetchall()]
        with col_activity:
            activity_filter = st.selectbox("Filter Activity:", all_activities)

        # بناء الاستعلام الهجين
        sql_query = '''
            SELECT s.id, st.full_name, s.student_id, s.activity_title, s.file_path, s.status, s.points, s.rejection_reason 
            FROM submissions s
            JOIN students st ON s.student_id = st.student_id
            WHERE 1=1
        '''
        params = []

        if search_query.strip():
            sql_query += " AND (st.full_name LIKE ? OR s.student_id LIKE ?)"
            params.extend([f"%{search_query.strip()}%", f"%{search_query.strip()}%"])

        if status_filter != "All":
            sql_query += " AND s.status = ?"
            params.append(status_filter)

        if activity_filter != "All Activities":
            sql_query += " AND s.activity_title = ?"
            params.append(activity_filter)

        sql_query += " ORDER BY s.id DESC"

        cursor.execute(sql_query, params)
        filtered_submissions = cursor.fetchall()

        st.subheader("📥 Submissions List")

        if filtered_submissions:
            for sub_id, full_name, std_id, act_title, f_path, status, points, reason in filtered_submissions:
                with st.expander(f"📌 [{status}] - {full_name} ({std_id}) - {act_title}", expanded=(status == 'Under Review')):
                    st.write(f"👤 **Student Name:** {full_name}")
                    st.write(f"🆔 **University ID:** {std_id}")
                    st.write(f"🎯 **Activity:** {act_title}")
                    st.write(f"📊 **Current Status:** {status}")

                    if status == "Approved":
                        st.success(f"Grade Assigned: {points} Points")
                    elif status == "Rejected":
                        st.error(f"Rejection Reason: {reason}")

                    if os.path.exists(f_path):
                        if f_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                            st.image(f_path, use_container_width=True)
                        else:
                            st.write("📄 The attached file is a PDF document.")
                    else:
                        st.warning("File path not found.")

                    # خيارات الاعتماد والرفض متاحة بشكل ديناميكي
                    st.markdown("---")
                    action_col1, action_col2 = st.columns(2)

                    with action_col1:
                        st.markdown("##### ✅ Approve Certificate")
                        pts = st.number_input("Grade to assign:", min_value=1, max_value=20, value=5, key=f"pts_{sub_id}")
                        if st.button(f"Approve Grade #{sub_id}", key=f"btn_app_{sub_id}"):
                            cursor.execute(
                                "UPDATE submissions SET status = 'Approved', points = ?, rejection_reason = '' WHERE id = ?",
                                (pts, sub_id)
                            )
                            conn.commit()
                            st.success("Successfully approved the certificate!")
                            st.rerun()

                    with action_col2:
                        st.markdown("##### ❌ Reject Certificate")
                        rej_reason = st.text_input("Reason for rejection:", key=f"reason_{sub_id}", placeholder="e.g., Unclear image, invalid date...")
                        if st.button(f"Reject Submission #{sub_id}", key=f"btn_rej_{sub_id}"):
                            if rej_reason.strip():
                                cursor.execute(
                                    "UPDATE submissions SET status = 'Rejected', points = 0, rejection_reason = ? WHERE id = ?",
                                    (rej_reason.strip(), sub_id)
                                )
                                conn.commit()
                                st.warning("Submission has been rejected with feedback saved.")
                                st.rerun()
                            else:
                                st.error("Please enter a rejection reason before proceeding.")

        else:
            st.info("No matching requests found based on your search/filter criteria.")

        st.subheader("📋 General Log Table")
        df_all = pd.read_sql_query('''
            SELECT s.id AS 'Request ID', st.full_name AS 'Student Name', s.student_id AS 'University ID', 
                   s.activity_title AS 'Activity', s.status AS 'Status', s.points AS 'Grade', s.rejection_reason AS 'Rejection Reason'
            FROM submissions s
            JOIN students st ON s.student_id = st.student_id
            ORDER BY s.id DESC
        ''', conn)
        st.dataframe(df_all, use_container_width=True)

# ==================== 2. واجهة الطلاب ====================
else:
    if not st.session_state.logged_in:
        st.markdown("<h2 style='text-align: center; color: #1e293b; font-weight: 800; margin-bottom: 5px;'>🎓 Student Activities System Portal</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.95rem;'>Welcome, student! Please log in to track your activities.</p>", unsafe_allow_html=True)

        with st.form("student_login_form"):
            s_id = st.text_input("University ID:")
            s_name = st.text_input("Full Name:")
            submit_login = st.form_submit_button("Login")

            if submit_login:
                if s_id.strip() and s_name.strip():
                    cursor.execute("INSERT OR REPLACE INTO students (student_id, full_name) VALUES (?, ?)", (s_id.strip(), s_name.strip()))
                    conn.commit()
                    
                    st.session_state.logged_in = True
                    st.session_state.student_id = s_id.strip()
                    st.session_state.student_name = s_name.strip()
                    st.rerun()
                else:
                    st.error("Please enter the university ID and full name completely.")

    else:
        st.sidebar.write(f"👤 **Student:** {st.session_state.student_name}")
        st.sidebar.write(f"🆔 **University ID:** {st.session_state.student_id}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.student_id = None
            st.session_state.student_name = None
            st.rerun()

        st.title("📄 Student Dashboard")

        cursor.execute("SELECT SUM(points) FROM submissions WHERE student_id = ? AND status = 'Approved'", (st.session_state.student_id,))
        total_points = cursor.fetchone()[0] or 0

        st.markdown(f"""
            <div class="score-card">
                <h3 style="margin:0; color:#1e3a8a !important;">Total Points Earned: {total_points} Points</h3>
                <p style="margin:5px 0 0 0; color:#6b7280 !important;">Points are added automatically once the certificate is verified by the department.</p>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📤 Upload New Certificate", "📊 Request Status"])

        with tab1:
            cursor.execute("SELECT title FROM activities")
            activities = [row[0] for row in cursor.fetchall()]

            with st.form("upload_form", clear_on_submit=True):
                selected_activity = st.selectbox("Select Activity / Workshop:", activities)
                uploaded_file = st.file_uploader("Upload Certificate Image (PNG, JPG, PDF):", type=['png', 'jpg', 'jpeg', 'pdf'])
                submit_cert = st.form_submit_button("Submit Certificate")

                if submit_cert:
                    if uploaded_file and selected_activity:
                        cursor.execute(
                            "SELECT COUNT(*) FROM submissions WHERE student_id = ? AND activity_title = ? AND status != 'Rejected'", 
                            (st.session_state.student_id, selected_activity)
                        )
                        already_submitted = cursor.fetchone()[0]

                        if already_submitted > 0:
                            st.error("⚠️ Alert: You have already uploaded an active certificate for this activity!")
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
                            st.success("Certificate uploaded successfully! It is now under review.")
                    else:
                        st.error("Please select an activity and attach a certificate file.")

        with tab2:
            st.subheader("Certificate Submission Log")
            df_sub = pd.read_sql_query(
                """SELECT activity_title AS 'Activity', status AS 'Request Status', 
                          points AS 'Grade', rejection_reason AS 'Rejection Reason / Notes' 
                   FROM submissions WHERE student_id = ? ORDER BY id DESC""",
                conn, params=(st.session_state.student_id,)
            )
            if not df_sub.empty:
                st.dataframe(df_sub, use_container_width=True)
            else:
                st.info("You have not uploaded any certificates yet.")
