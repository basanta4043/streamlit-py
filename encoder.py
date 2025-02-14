import streamlit as st
import hashlib


def encode(plain_text, salt=None):
    first_hash = hashlib.sha256(plain_text.encode('utf-8')).hexdigest()
    if salt is not None:
        final_hash = hashlib.sha256((first_hash + salt).encode('utf-8')).hexdigest()
    else:
        final_hash = first_hash
    return final_hash


def is_equal_encoding(encoded_password, plain_text, salt=None):
    first_hash = hashlib.sha256(plain_text.encode('utf-8')).hexdigest()
    if salt is not None:
        final_hash = hashlib.sha256((first_hash + salt).encode('utf-8')).hexdigest()
    else:
        final_hash = first_hash
    return encoded_password == final_hash


def password_encoder_ui():
    st.title("🔑 Password Encoder & Verifier")
    plain_text = st.text_input("Enter Plain Text Password", type="password")
    salt = st.text_input("Enter Salt (Optional)")

    if st.button("Encode Password"):
        if plain_text:
            if salt == "": salt = None
            encoded_password = encode(plain_text, salt)
            st.success(f"Encoded Password: `{encoded_password}`")
        else:
            st.warning("Please enter a password.")

    st.subheader("Verify Encoded Password")
    encoded_password_input = st.text_input("Encoded Password", type="password")
    plain_text_verify = st.text_input("Plain Text for Verification", type="password")
    salt_verify = st.text_input("Salt (Optional) for Verification")

    if st.button("Verify Password"):
        if encoded_password_input and plain_text_verify:
            if is_equal_encoding(encoded_password_input, plain_text_verify, salt_verify):
                st.success("Password matches!")
            else:
                st.error("Password does not match.")
        else:
            st.warning("Fill all fields for verification.")
