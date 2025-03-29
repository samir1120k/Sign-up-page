import streamlit as st
from PIL import Image
import base64

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
            .image-container {{
                position: relative;
                display: inline-block;
                text-align: right;
                width: 100%;
            }}
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
        st.markdown('<div class="form-container">', unsafe_allow_html=True) # Added div with class form-container
        st.markdown(
            """
            <style>
            .centered-message-container {
                margin-top: 30px;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 50px;
            }
            </style>
            <div class="centered-message-container">
                <h1>Login</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
        username = st.text_input("User Name")
        password = st.text_input("Password", type="password")

        remember_col, forgot_col = st.columns(2)
        with remember_col:
            remember_me = st.checkbox("Remember Me")

        with forgot_col:
            st.markdown(
                """
                <style>
                .forgot-password {
                    margin-left: 30px;
                }
                </style>
                <span class="forgot-password">[Forgot Password?](#)</span>
                """,
                unsafe_allow_html=True,
            )
        if st.button("Login"):
            st.markdown(
                """
                <style>
                .centered-message-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 50px;
                }
                </style>
                <div class="centered-message-container">
                    Login button clicked!
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True) # Close the form-container div

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    login_page()
