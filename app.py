import streamlit as st
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt

# Download VADER if first time
nltk.download('vader_lexicon')

st.set_page_config(
    page_title="Instagram Sentiment Analyzer 📊",
    layout="wide"
)

st.title("📊 Instagram Sentiment Analyzer")
st.write("Upload an Excel file containing your Instagram comments data.")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    # Read data & drop unnamed columns
    df = pd.read_excel(uploaded_file)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    st.success("✅ File uploaded successfully!")

    # Assign unique Post IDs based on 'Link'
    df['Post ID'] = df['Link'].factorize()[0] + 1

    # Initialize VADER
    sid = SentimentIntensityAnalyzer()

    # Function to get sentiment
    def classify_sentiment(text):
        score = sid.polarity_scores(str(text))['compound']
        if score >= 0.05:
            return 'Positive'
        elif score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    # Apply sentiment classification
    df['Sentiment'] = df['Comment'].apply(classify_sentiment)

    # Group by Post to calculate counts
    summary = df.groupby(['Link', 'Post ID'])['Sentiment'].value_counts().unstack(fill_value=0).reset_index()

    # Compute totals & percentages
    summary['Total Comments'] = summary[['Positive', 'Negative', 'Neutral']].sum(axis=1)
    summary['% Positive'] = (summary['Positive'] / summary['Total Comments'] * 100).round(2)
    summary['% Negative'] = (summary['Negative'] / summary['Total Comments'] * 100).round(2)
    summary['% Neutral'] = (summary['Neutral'] / summary['Total Comments'] * 100).round(2)

    # Display everything
    st.subheader("📌 Summary by Post")
    st.dataframe(summary.style.background_gradient(cmap='Blues'))

    st.subheader("📝 All Comments with Sentiment")
    st.dataframe(df)

    # Allow download
    st.download_button("📥 Download Summary as CSV", summary.to_csv(index=False), "summary.csv", "text/csv")