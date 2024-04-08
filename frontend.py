import logging
import os
import time
from display_cost_and_summary import display_summary_and_cost
import hmac
import streamlit as st

from main import call_recording_main

logging.basicConfig(filename="log.log", filemode="w", level=logging.INFO)
logger = logging.getLogger(__name__)


def file_uploader_placeholder(file_name, file_size):
    st.text(f"{file_name} - {file_size}MB")
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.05)
        my_bar.progress(percent_complete + 1)


def summarizing_audio(file_name):
    st.text(f"Summarizing {file_name}...")
    my_bar = st.progress(0)
    call_recording_main()
    for percent_complete in range(100):
        time.sleep(0.05)
        my_bar.progress(percent_complete + 1)
    st.success(f"Summarizing complete for {file_name}!")


def uploaded_files_in_dir(uploaded_file):
    file_name = uploaded_file.name
    bytes_data = uploaded_file.read()

    st.write("Filename:", file_name)
    file_size = len(bytes_data) / (1024 * 1024)
    file_uploader_placeholder(file_name, round(file_size, 2))
    with open(os.path.join("audio", file_name), "wb") as f:
        f.write(bytes_data)

    st.audio(bytes_data)
    file = f"audio_summary/{file_name}_call_recording_summary_of_.md"
    print("=========file", file)
    print("---------os.path.exists(file)-------", os.path.exists(file))
    if os.path.exists(file):
        print("--------in if")
        display_summary_and_cost(file_name)
    else:
        print("-----------in else")
        summarizing_audio(file_name)

def main():
    st.set_page_config("Call Recording Summarization", page_icon="https://media.licdn.com/dms/image/C4E0BAQErzHJr7lA-uQ/company-logo_200_200/0/1631356294168?e=1714608000&v=beta&t=lbeplkUBiGsPGvObCIUmLk5qRA9X8NvoJGHWBZEC6so", layout="wide")
    st.title("Audio File Uploader")

    uploaded_files = st.file_uploader(
        "Drag and drop or select audio files", type=["mp3", "wav", "ogg", "mp4"]
    )
    if uploaded_files:
        uploaded_files_in_dir(uploaded_files)
        st.button("Re-run")

def check_password():

    def login_form():
        st.set_page_config(page_title="LexoGraph", layout="wide")
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        if st.session_state["username"] in st.secrets["passwords"] and hmac.compare_digest(st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()

main()
