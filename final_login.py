import streamlit as st
from PIL import Image
import base64
import bcrypt
import pymongo

# MongoDB Connection
MONGO_URI = "mongodb+srv://samir1120k:samirsyra1120@cluster0.sjtkfdj.mongodb.net/"
client = pymongo.MongoClient(MONGO_URI)
db = client["your_database_name"]
collection = db["users"]

# ------------------ SIGNUP FUNCTION ------------------ #
def signup(username, password):
    if collection.find_one({"username": username}):
        return "Username already exists. Please try another one."

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    collection.insert_one({"username": username, "password": hashed_password.decode('utf-8')})
    return "Signup successful! You can now log in."

# ------------------ LOGIN FUNCTION ------------------ #
def authenticate_user(username, password):
    user = collection.find_one({"username": username})
    if user:
        stored_hashed_password = user["password"]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            return "Login successful!"
        else:
            return "Invalid password. Please try again."
    else:
        return "Invalid username. Please check your details."

# ------------------ USER INTERFACE ------------------ #
def login_page():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        image_path = "welcome_image.jpeg"
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

    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>Sign up</h1>", unsafe_allow_html=True)
        username = st.text_input("User Name")
        password = st.text_input("Password", type="password")
        login_message = ""

        if st.button("Login"):
            login_message = signup(username, password)

        if login_message:
            st.markdown(f"<p style='text-align: center; color: green;'>{login_message}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    login_page()
