import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Instagram Sentiment Analyzer 📊",
    layout="wide"
)

st.title("📊 Instagram Sentiment Analyzer")
st.write("Upload an Excel file containing your Instagram comments data.")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("File uploaded successfully!")
    
    st.subheader("Raw Data Preview")
    st.dataframe(df)