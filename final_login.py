from PIL import Image
import base64
import bcrypt
import pymongo
import re
import streamlit as st

# MongoDB Connection
MONGO_URI = "mongodb+srv://samir1120k:samirsyra1120@cluster0.sjtkfdj.mongodb.net/"
client = pymongo.MongoClient(MONGO_URI)
db = client["your_database_name"]
collection = db["users"]

# ------------------ EMAIL VALIDATION FUNCTION ------------------ #
def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)

# ------------------ SIGNUP FUNCTION ------------------ #
def signup(email, password):
    if not is_valid_email(email):
        return "Invalid email format. Please enter a valid email."

    if collection.find_one({"email": email}):
        return "Email already exists. Please try logging in."

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    collection.insert_one({"email": email, "password": hashed_password.decode('utf-8')})
    return "success"

# ------------------ LOGIN FUNCTION ------------------ #
def authenticate_user(email, password):
    user = collection.find_one({"email": email})
    if user:
        stored_hashed_password = user["password"]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            return "success"
        else:
            return "Invalid password. Please try again."
    else:
        return "Email not found. Please sign up first."

# ------------------ POPUP FORM PAGE ------------------ #
def main_page():
    st.markdown(
        """
        <style>
            .popup-container {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) translateY(-100%);
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                padding: 30px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                z-index: 1000;
                opacity: 0;
                border-radius: 8px;
                transition: transform 0.5s ease-in-out, opacity 0.5s ease-in-out;
                text-align: center;
                width: 300px;
            }

            .popup-container.show {
                transform: translate(-50%, -50%);
                opacity: 1;
                width: auto;
            }

            .popup-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 999;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.3s ease-in-out;
            }

            .popup-overlay.show {
                opacity: 1;
                pointer-events: auto;
            }

            .popup-close-button {
                position: absolute;
                top: 15px;
                right: 15px;
                cursor: pointer;
                font-size: 18px;
                color: #555;
                border: none;
                background: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
        name = st.text_input("Enter your name")
        height = st.text_input("Enter your height", placeholder="e.g., 175 cm")

        if st.button("Submit"):
            if name and height:
                st.markdown(
                    f"""
                    <div class="popup-overlay show" id="popup-overlay"></div>
                    <div class="popup-container show" id="popup">
                        <button class="popup-close-button" onclick="document.getElementById('popup').classList.remove('show'); document.getElementById('popup-overlay').classList.remove('show');">×</button>
                        <h3>Tada 😉 {name}</h3>
                        <p>Your Height is {height} cm</p>
                    </div>
                    <script>
                        if (document.getElementById('popup')) {{
                            document.getElementById('popup').classList.add('show');
                        }}
                        if (document.getElementById('popup-overlay')) {{
                            document.getElementById('popup-overlay').classList.add('show');
                        }}
                    </script>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.warning("Please fill both name and height.")

# ------------------ SIGNUP PAGE ------------------ #
def signup_page():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        image_path = "welcome_image.jpeg"
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            st.markdown(
                f"""
                <style>
                .styled-image {{
                    width: 340px;
                    height: 450px;
                    border-radius: 10px;
                    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);
                    display: block;
                    margin-left: auto;
                }}
                .image-text {{
                    position: absolute;
                    top: 15%;
                    left: 100%;
                    transform: translate(-100%, -50%);
                    color: #36c2ad;
                    font-size: 33px;
                    font-weight: bold;
                    text-align: center;
                    width: 100%;
                    white-space: nowrap;
                }}
                </style>
                <div class="image-container">
                    <img class="styled-image" src="data:image/jpeg;base64,{encoded_string}" alt="My Styled Image">
                    <div class="image-text">Welcome😊</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except FileNotFoundError:
            st.error(f"Image file '{image_path}' not found.")

    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>Sign up</h1>", unsafe_allow_html=True)
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        signup_message = ""

        if st.button("Register"):
            signup_message = signup(email, password)
            if signup_message == "success":
                st.session_state.page = "main"
                st.rerun()
            else:
                st.markdown(f"<p style='text-align: center; color: red;'>{signup_message}</p>", unsafe_allow_html=True)

        if st.button("Already have an account? Log In"):
            st.session_state.page = "login"
            st.rerun()

# ------------------ LOGIN PAGE ------------------ #
def login_page():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        image_path = "welcome_image.jpeg"
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            st.markdown(
                f"""
                <style>
                .styled-image {{
                    width: 340px;
                    height: 450px;
                    border-radius: 10px;
                    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);
                    display: block;
                    margin-left: auto;
                }}
                .image-text {{
                    position: absolute;
                    top: 15%;
                    left: 100%;
                    transform: translate(-100%, -50%);
                    color: #36c2ad;
                    font-size: 33px;
                    font-weight: bold;
                    text-align: center;
                    width: 100%;
                    white-space: nowrap;
                }}
                </style>
                <div class="image-container">
                    <img class="styled-image" src="data:image/jpeg;base64,{encoded_string}" alt="My Styled Image">
                    <div class="image-text">Welcome Back😊</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except FileNotFoundError:
            st.error(f"Image file '{image_path}' not found.")

    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_message = ""

        if st.button("Enter"):
            login_message = authenticate_user(email, password)
            if login_message == "success":
                st.session_state.page = "main"
                st.rerun()
            else:
                color = "green" if "successful" in login_message.lower() else "red"
                st.markdown(f"<p style='text-align: center; color: {color};'>{login_message}</p>", unsafe_allow_html=True)

        if st.button("Don't have an account? Sign Up"):
            st.session_state.page = "signup"
            st.rerun()

# ------------------ MAIN APP ------------------ #
def main():
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "main":
        main_page()

if __name__ == "__main__":
    main()
