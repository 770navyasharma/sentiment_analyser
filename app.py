import streamlit as st
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER
nltk.download('vader_lexicon')

# Load custom CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page config
st.set_page_config(
    page_title="Instagram Sentiment Analyzer 📊",
    layout="wide"
)

# App title
st.title("📊 Instagram Sentiment Analyzer")
st.markdown("""
<div style='color:#555;font-size:18px;margin-bottom:20px;'>
Upload your Excel file to analyze Instagram comments for sentiment insights.<br>
This tool auto-categorizes comments into Positive, Neutral, Negative & provides beautiful summary dashboards.
</div>
""", unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader("📁 Choose an Excel file", type=["xlsx"])

if uploaded_file:
    # Read & clean
    df = pd.read_excel(uploaded_file)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    st.success("✅ File uploaded and processed successfully!")

    # Assign Post IDs
    df['Post ID'] = df['Link'].factorize()[0] + 1

    # Sentiment analysis
    sid = SentimentIntensityAnalyzer()
    def classify_sentiment(text):
        score = sid.polarity_scores(str(text))['compound']
        if score >= 0.05:
            return 'Positive'
        elif score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    df['Sentiment'] = df['Comment'].apply(classify_sentiment)

    # Summary
    summary = df.groupby(['Link', 'Post ID'])['Sentiment'].value_counts().unstack(fill_value=0).reset_index()
    summary['Total Comments'] = summary[['Positive', 'Negative', 'Neutral']].sum(axis=1)
    summary['% Positive'] = (summary['Positive'] / summary['Total Comments'] * 100).round(2)
    summary['% Negative'] = (summary['Negative'] / summary['Total Comments'] * 100).round(2)
    summary['% Neutral'] = (summary['Neutral'] / summary['Total Comments'] * 100).round(2)

    # Show summary
    st.markdown("---")
    st.subheader("📌 Summary by Post")
    st.dataframe(summary.style.background_gradient(cmap='PuBu'))
    
        # Overall totals
    total_comments = len(df)
    total_posts = df['Post ID'].nunique()
    total_positive = (df['Sentiment'] == 'Positive').sum()
    total_negative = (df['Sentiment'] == 'Negative').sum()
    total_neutral = (df['Sentiment'] == 'Neutral').sum()

    # Display one line summary
    st.markdown(f"""
    <div style='
        background-color:#f05454;
        color:white;
        padding:15px;
        border-radius:10px;
        text-align:center;
        font-size:18px;
        font-weight:bold;
        margin:20px 0;
    '>
    🚀 Analysis Complete: {total_comments} Total Comments | {total_posts} Unique Posts | 
    {total_positive} Positive | {total_negative} Negative | {total_neutral} Neutral
    </div>
    """, unsafe_allow_html=True)

    # Highest counts summary
    max_positive_row = summary.loc[summary['Positive'].idxmax()]
    max_negative_row = summary.loc[summary['Negative'].idxmax()]
    max_neutral_row = summary.loc[summary['Neutral'].idxmax()]

    st.markdown(f"""
    <div style='
        background-color:#30475e;
        color:white;
        padding:15px;
        border-radius:10px;
        text-align:center;
        font-size:16px;
        font-weight:bold;
        margin:20px 0;
    '>
    🏆 Highest Counts:<br>
    ✅ Positive: {int(max_positive_row['Positive'])} in Post <a href="{max_positive_row['Link']}" target="_blank" style="color:#f05454;">{max_positive_row['Link']}</a><br>
    ❌ Negative: {int(max_negative_row['Negative'])} in Post <a href="{max_negative_row['Link']}" target="_blank" style="color:#f05454;">{max_negative_row['Link']}</a><br>
    🤍 Neutral: {int(max_neutral_row['Neutral'])} in Post <a href="{max_neutral_row['Link']}" target="_blank" style="color:#f05454;">{max_neutral_row['Link']}</a>
    </div>
    """, unsafe_allow_html=True)

    # Download
    st.download_button("📥 Download Summary as CSV", summary.to_csv(index=False), "summary.csv", "text/csv")

    # Detailed comments
    st.markdown("---")
    st.subheader("📝 Detailed Comments with Sentiment")
    st.dataframe(df)