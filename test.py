import streamlit as st
import openai
import pandas as pd
import jsonlines

# Set OpenAI API Key
openai.api_key = st.text_input("請輸入OpenAI API Key：")

# Check API Key
try:
    models = openai.Model.list()
except Exception as e:
    st.error(f"無法連接OpenAI API，請檢查API Key是否正確：{e}")
    st.stop()


# allow user upload training data（使用excel格式）
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    try:
        # 讀取excel檔案
        df = pd.read_excel(uploaded_file)
        # 轉換成jsonl格式
        jsonl = openai.FineTune.prepare_data(df=df)
        # 顯示檔案轉換已完成
        st.success('File conversion completed!')
        # 下載jsonl檔案
        href = f'<a href="data:application/jsonl;base64,{jsonl}">Download jsonl file</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.download_button(label="Download jsonl", data=jsonl, file_name="training_data.jsonl", mime="application/jsonl")
    except errors.AuthenticationError:
        st.error("Invalid OpenAI API key")
    except Exception as e:
        st.error(f"Error: {e}")
