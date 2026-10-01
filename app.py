import streamlit as st
import sqlite3
import os
import pandas as pd
import base64
import streamlit as st

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
    /* 1. إجبار خلفية الصفحة على اللون الفاتح */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #f8f9fa !important;
        color: #1a202c !important;
    }

    /* 2. استهداف حقول الإدخال بالكامل وإلغاء خلفية الداكن */
    div[data-baseweb="input"], 
    div[data-baseweb="base-input"],
    input[class*="st-"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-radius: 8px !important;
    }

    .stTextInput input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        padding: 10px 14px !important;
    }

    /* 3. العناوين والنصوص فوق الحقول */
    .stTextInput label p, label[data-testid="stWidgetLabel"] p {
        color: #1e293b !important;
        font-weight: 600 !important;
    }

    /* 4. الأزرار */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button {
        background-color: #1e3a8a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        width: 100% !important;
    }

    /* 5. إخفاء شريط ووسام Streamlit السفلـي والقوائم */
    #MainMenu, header, footer, 
    div[data-testid="stHeader"], 
    div[data-testid="stToolbar"],
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
        <div>{logo_uni_html}</div>
        <div class="header-text">
            <h3>Al-Mustaqbal University</h3>
            <h5>Department of Artificial Intelligence Engineering</h5>
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
        status TEXT DEFAULT 'Under Review',
        points INTEGER DEFAULT 0,
        FOREIGN KEY (student_id) REFERENCES students (student_id)
    )
''')
conn.commit()

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

        st.subheader("📥 Pending Requests for Review")
        query = '''
            SELECT s.id, st.full_name, s.student_id, s.activity_title, s.file_path 
            FROM submissions s
            JOIN students st ON s.student_id = st.student_id
            WHERE s.status = 'Under Review'
        '''
        cursor.execute(query)
        pending_list = cursor.fetchall()

        if pending_list:
            for sub_id, full_name, std_id, act_title, f_path in pending_list:
                st.markdown("---")
                st.write(f"👤 **Student:** {full_name} ({std_id})")
                st.write(f"🎯 **Activity:** {act_title}")
                if os.path.exists(f_path):
                    if f_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                        st.image(f_path, use_container_width=True)
                    else:
                        st.write("📄 the attached file is a PDF")
                
                pts = st.number_input(f"Grade for request #{sub_id}", min_value=1, max_value=20, value=5, key=f"pts_{sub_id}")
                if st.button(f"Approve Grade #{sub_id}", key=f"btn_{sub_id}"):
                    cursor.execute("UPDATE submissions SET status = 'Approved', points = ? WHERE id = ?", (pts, sub_id))
                    conn.commit()
                    st.success("Successfully approved the certificate and recorded the grade!")
                    st.rerun()
        else:
            st.info("There are currently no pending requests awaiting review.")

        st.subheader("📋 the general log for all requests")
        df_all = pd.read_sql_query('''
            SELECT s.id AS 'Request Number', st.full_name AS 'Student Name', s.student_id AS 'University ID', 
                   s.activity_title AS 'Activity', s.status AS 'Status', s.points AS 'Grade'
            FROM submissions s
            JOIN students st ON s.student_id = st.student_id
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

        st.title("📄Student Dashboard")

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
                            "SELECT COUNT(*) FROM submissions WHERE student_id = ? AND activity_title = ?", 
                            (st.session_state.student_id, selected_activity)
                        )
                        already_submitted = cursor.fetchone()[0]

                        if already_submitted > 0:
                            st.error("⚠️ Alert: You have already uploaded a certificate for this activity!")
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
                "SELECT activity_title AS 'Activity', status AS 'Request Status', points AS 'Grade' FROM submissions WHERE student_id = ?",
                conn, params=(st.session_state.student_id,)
            )
            if not df_sub.empty:
                st.dataframe(df_sub, use_container_width=True)
            else:
                st.info("You have not uploaded any certificates yet.")
