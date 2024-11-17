import bcrypt  # type: ignore
import streamlit as st  # type: ignore
import time  # For adding delay
import base64
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
font_css = """
    <style>
    body {
        font-family: 'Times New Roman', Times, serif;
    }
    </style>
"""
st.title("AIR QUALITY INDEX FOR INDIAN CITIES")
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-color: #FFECEB;  
     width: 100%;  /* Ensure full width */
    padding: 0;  /* Remove excess padding */
    margin: 0 auto;  /* Center content horizontally */
}}
[data-testid="stSidebar"] > div:first-child {{
    background-color: #FFECEB; 
}}
[data-testid="stSidebar"] > div {{
    color: black;
    
}}
[data-testid="stHeader"] {{
    background-color: #A84235;  /* Dark blue header */
    color: white;
    width: 100%;  /* Full width for header */
    padding: 10px 0;  /* Adjust padding */
}}
[data-testid="stFooter"] {{
    background-color: #A84235;  /* Dark blue footer */
    color: white;
    width: 100%;  /* Full width for header */
    padding: 10px 0;  /* Adjust padding */
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

sidebar_button_style = """
    <style>
    /* Custom button styling for the sidebar */
    .stButton > button {
        display:block;
        width:80%;
        background-color: #a84235 !important;  /* Red background */
        color: white !important;  /* White text */
        border-radius: 10px;
        padding:18px;
        border: none;
        font-size: 40px;
        margin: 20px auto;
        margin-bottom: 4px;  /* Spacing between buttons */
    } 
    /* Hover effect */
    .stButton > button:hover {
        background-color: #D45343 !important;  /* Darker red */
    }
    /* Active/clicked state */
    .stButton > button:active {
        background-color: #D45343 !important;  /* Even darker red */
    }

     .stDownloadButton > button {
        background-color: #a84235 !important;  /* Red background */
        color: white !important;  /* White text */
        border-radius: 10px;
        padding: 15px;
        border: none;
        font-size: 23px;
        width: 40%;
        margin: 10px auto;
    }
    /* Hover effect for download buttons */
    .stDownloadButton > button:hover {
        background-color: #D45343 !important;  /* Darker red */
    }
    /* Active/clicked state for download buttons */
    .stDownloadButton > button:active {
        background-color: #D45343 !important;  /* Even darker red */
    }
    </style>
"""
st.markdown(sidebar_button_style, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["page"] = "Login"  

if "users" not in st.session_state:
    st.session_state["users"] = {
        "admin": bcrypt.hashpw("password123".encode(), bcrypt.gensalt())
    }

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode(), hashed_password)
def clear_all_inputs():
    st.session_state.clear_inputs = True
smtp_server = "smtp.office365.com"
smtp_port = 587
smtp_user = "support@aptpath.in"
smtp_password = "kjydtmsbmbqtnydk"  
sender_email = "support@aptpath.in"
receiver_emails = "brindaa.b04@gmail.com"

def feedback_page():
    st.markdown("""
        <style>
            .feedback-title {
                font-size: 20px;
                color: black;
            }
            .feedback-input {
                font-size: 18px;
                color: black;
            }
        </style>
    """, unsafe_allow_html=True)
    st.subheader("We Value Your Feedback!")

    st.markdown('<p class="feedback-title">Your Name (Optional):</p>', unsafe_allow_html=True)
    name = st.text_input("Your Name (Optional):")
    
    st.markdown('<p class="feedback-title">Your Email (Optional):</p>', unsafe_allow_html=True)
    email = st.text_input("Your Email (Optional):")

    st.markdown('<p class="feedback-title">Please provide your feedback here:</p>', unsafe_allow_html=True)
    feedback = st.text_area("Please provide your feedback here:")

    st.markdown('<p class="feedback-title">Rate your experience:</p>', unsafe_allow_html=True)
    rating = st.slider("Rate your experience:", 1, 5, 3)

    if st.button("Submit Feedback"):
        if feedback:
            try:
                send_feedback_email(feedback, rating, name, email)
                st.success(f"Thank you for your feedback, {'User' if not name.strip() else name}!")
                st.info("We appreciate your input and will use it to improve our service.")
            except Exception as e:
                st.error(f"Failed to send feedback. Error: {e}")
        else:
            st.warning("Please enter some feedback before submitting.")
    st.write("""
        **  **
        ### You can download the AQI report and the data file from below:
    """)
 
    st.download_button(
        label="Download Data as CSV ⬇️",
        data=open("cleaned_data.csv", "rb").read(),
        file_name="filtered_data.csv",
        mime="text/csv"
    )
    st.download_button(
        label="Download AQI Report as PDF ⬇️",
        data=open("Air Quality Index report.pdf", "rb").read(),
        file_name="AQI_report.pdf",
        mime="application/pdf"
    )
    st.download_button(
        label="Download Power BI Report as PBIX ⬇️",
        data=open("AQI Dataset - Copy.pbix", "rb").read(),
        file_name="your_report.pbix",
        mime="application/octet-stream"
    )
def send_feedback_email(feedback,rating,name,email):
    try:
        name = name.strip() if name.strip() else "Anonymous"
        email = email.strip() if email.strip() else "Not provided"
    
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(smtp_user, smtp_password)
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_emails
        msg['Subject'] = "User Feedback"
        body = f"User feedback from {name} ({email}):\n\n{feedback}\n\nRating: {rating} stars"
        msg.attach(MIMEText(body, 'plain'))
        server.sendmail(sender_email, receiver_emails, msg.as_string())
        server.quit()
    except Exception as e:
        raise Exception(f"Error sending email: {e}")

def show_dashboard():
    st.subheader("DASHBOARD INFORMATION")
    st.markdown("""
        <p style="font-size: 18px;">
        This dashboard contains visualizations related to Indian Air Quality. It helps you understand various air quality metrics like PM2.5, PM10, NO2, CO, and others, providing insights into air pollution levels.
        </p>
    """, unsafe_allow_html=True)

    st.subheader("How to Use the Dashboard:")
    st.markdown("""
        
        <p style="font-size: 18px;">
        
        - You can filter the data using slicers available on the dashboard.<br>
        - To <strong>Clear all slicers</strong>, <strong>CTRL +</strong> click on <strong>Clear All Slicers</strong> button.<br>
        - To <strong>Apply all slicers</strong>, select the filters and do <strong>CTRL +</strong> click on <strong>Apply All Slicers</strong> to select multiple values within a slicer.<br>
        - You can explore different air quality indices and their associated data based on your selected filters.
        </p>
    """, unsafe_allow_html=True)

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiYzQ2MDRhOWUtNjM2ZS00YjY5LWExZjUtODVhMGQzMDgxNDIxIiwidCI6ImI2MDBlZTNmLWM5ODAtNDU4OS04MDNiLTRlOWM5OTAxOTI1MSJ9"
    st.markdown(
        f"""
        <style>
        .iframe-container {{
            width: 80vw;
            height: 100vh;
        }}
        </style>
        <div class="iframe-container">
            <iframe title="Power BI Dashboard" width="100%" height="100%" 
            src="{powerbi_url}" frameborder="0" allowFullScreen="true"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )  
def show_home_page():
    st.subheader("UNDERSTANDING AIR POLLUTION:")
    st.markdown("""
        <p style="font-size: 18px;">
        Air pollution refers to the presence of harmful substances in the air that can pose a risk to human health, ecosystems, and the environment. 
        The Air Quality Index (AQI) is a measurement of air pollutant concentrations in ambient air pollution and their associated health risks.
        </p>
        """, unsafe_allow_html=True)

    st.write("""
        ### AIR POLLUTANTS MEASURED IN AQI:
        <ul style="font-size: 18px;">
            <li><strong>PM2.5</strong></li>
            <li><strong>PM10</strong></li>
            <li><strong>CARBON MONOXIDE - CO</strong></li>
            <li><strong>SULFUR DIOXIDE - SO2</strong></li>
            <li><strong>NITROGEN DIOXIDE - NO2</strong></li>
            <li><strong>GROUND-LEVEL OZONE - O3</strong></li>
        </ul>
        """, unsafe_allow_html=True)
    
    st.image("https://www.ourair.org/wp-content/uploads/AQItable.gif", caption="AQI Level", width=700)

    st.markdown("""
        <p style="font-size: 18px;">
        The air quality index ranges from 0 to 500, though air quality can be indexed beyond 500 when there are higher levels of hazardous air pollution. 
        Good air quality ranges from 0 to 50, while measurements over 300 are considered hazardous.
        </p>
        """, unsafe_allow_html=True)

    st.write("""
        ### WHAT CAN YOU DO TO PROTECT YOURSELF:
        <ul style="font-size: 18px;">
            <li><strong>Limit outdoor activities:</strong> Reduce time spent outdoors, especially during high pollution periods.</li>
            <li><strong>Avoid exercise in high pollution areas:</strong> If you exercise outdoors, do it when air quality is better.</li>
            <li><strong>Stay indoors:</strong> Keep windows and doors closed during times of high pollution.</li>
            <li><strong>Use air purifiers:</strong> Ensure good air quality inside your home, especially if you have respiratory issues.</li>
            <li><strong>Wear a mask:</strong> Consider wearing a mask designed for air pollution (such as N95) when air quality is poor.</li>
        </ul>
        """, unsafe_allow_html=True)
def login_page():
    
    st.subheader("Login to Access Dashboard")
    if "clear_inputs" in st.session_state and st.session_state.clear_inputs:
        st.session_state.username = ""
        st.session_state.password = ""
        st.session_state.clear_inputs = False
    username = st.text_input("Username", value=st.session_state.get("username", ""), key="username")
    password = st.text_input("Password", type="password", value=st.session_state.get("password", ""), key="password")
    
    if st.button("Login"):
        if username in st.session_state["users"]:
            hashed_password = st.session_state["users"][username]
            if check_password(hashed_password, password):
                st.session_state["logged_in"] = True
                st.session_state["page"] = "Home"
                st.success("Logged in successfully!")
                clear_all_inputs()
            else:
                st.error("Incorrect password.")
        else:
            st.error("Username not found.")

    st.markdown("Don't have an account? Create one below:")
    if st.button("Sign up"):
        st.session_state["page"] = "Sign Up"

def signup_page():
    st.subheader("Create an Account")
    if "clear_inputs" in st.session_state and st.session_state.clear_inputs:
        st.session_state.new_username = ""
        st.session_state.new_password = ""
        st.session_state.clear_inputs = False

    new_username = st.text_input("New Username", value=st.session_state.get("new_username", ""), key="new_username")
    new_password = st.text_input("New Password", type="password", value=st.session_state.get("new_password", ""), key="new_password")
    
    if st.button("Sign Up"):
        if new_username in st.session_state["users"]:
            st.warning("Username already exists. Please choose another one.")
        else:
            hashed_pw = hash_password(new_password)
            st.session_state["users"][new_username] = hashed_pw
            st.success("Account created successfully! You can now log in.")
            clear_all_inputs()
            st.session_state["page"] = "Login"
    st.markdown("Already have an account?")
    if st.button("Back to Login"):
        st.session_state["page"] = "Login"

if st.session_state["logged_in"]:
    st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 20px; font-weight: bold;">
        MENU
    </div>
    """,
    unsafe_allow_html=True
    )
    home_button = st.sidebar.button(" 🏡 Home", key="home_button")
    dashboard_button = st.sidebar.button(" 📊 Dashboard", key="dashboard_button")
    feedback_button = st.sidebar.button(" 📝 Feedback and Reports", key="feedback_button")
    logout_button = st.sidebar.button(" ⬅️ Logout", key="logout_button")

    if home_button:
        st.session_state["page"] = "Home"
    elif dashboard_button:
        st.session_state["page"] = "Dashboard"
    elif feedback_button:
        st.session_state["page"] = "Feedback and Reports"
    elif logout_button:
        st.session_state.update({"logged_in": False, "page": "Login"})
        st.success("You have successfully logged out.")
        time.sleep(1)
        st.rerun()
    
    if st.session_state["page"] == "Home":
        show_home_page()
    elif st.session_state["page"] == "Dashboard":
        show_dashboard()
    elif st.session_state["page"] == "Feedback and Reports":
        feedback_page()

else:
    if st.session_state["page"] == "Login":
        login_page()
    elif st.session_state["page"] == "Sign Up":
        signup_page()