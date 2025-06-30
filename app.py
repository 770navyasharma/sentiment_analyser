import streamlit as st
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
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

    
    # ------------------------
    # Row 1: Overall Bar + Pie
    # ------------------------
    st.markdown("---")
    st.subheader("📊 Sentiment Overview")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(5,3))
        sns.barplot(x=["Positive", "Negative", "Neutral"],
                    y=[total_positive, total_negative, total_neutral],
                    palette=["#4CAF50", "#F44336", "#FFC107"], ax=ax)
        ax.set_ylabel("Number of Comments")
        ax.set_title("Overall Sentiment Counts")
        sns.despine()
        fig.tight_layout()
        st.pyplot(fig)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(5,3))
        ax2.pie([total_positive, total_negative, total_neutral],
                labels=["Positive", "Negative", "Neutral"],
                autopct='%1.1f%%',
                startangle=140,
                colors=["#4CAF50", "#F44336", "#FFC107"],
                wedgeprops={'edgecolor':'white', 'linewidth':2})
        centre_circle = plt.Circle((0,0),0.70,fc='#f7f9fc')
        fig2.gca().add_artist(centre_circle)
        ax2.axis('equal')
        fig2.tight_layout()
        st.pyplot(fig2)

    # -------------------------------
    # Row 2: Top / Worst Posts
    # -------------------------------
    st.markdown("---")
    st.subheader("📈 Top & Worst Performing Posts")

    col3, col4 = st.columns(2)

    with col3:
        top5_positive = summary.sort_values(by='Positive', ascending=False).head(5)
        fig3, ax3 = plt.subplots(figsize=(5,3))
        sns.barplot(data=top5_positive, x='Positive', y='Link', palette="Greens_d", ax=ax3)
        ax3.set_title("Top 5 Posts by Positive Comments")
        fig3.tight_layout()
        st.pyplot(fig3)

    with col4:
        worst5_positive = summary.sort_values(by='Positive', ascending=True).head(5)
        fig4, ax4 = plt.subplots(figsize=(5,3))
        sns.barplot(data=worst5_positive, x='Positive', y='Link', palette="Reds_d", ax=ax4)
        ax4.set_title("Top 5 Worst Posts by Positive Comments")
        fig4.tight_layout()
        st.pyplot(fig4)

    # ------------------------------
    # Row 3: Top posts by negatives
    # ------------------------------
    st.markdown("---")
    st.subheader("🚨 Posts with Highest Negative Comments")

    col5, col6 = st.columns(2)

    with col5:
        top5_negative = summary.sort_values(by='Negative', ascending=False).head(5)
        fig5, ax5 = plt.subplots(figsize=(5,3))
        sns.barplot(data=top5_negative, x='Negative', y='Link', palette="Oranges_d", ax=ax5)
        ax5.set_title("Top 5 Posts by Negative Comments")
        fig5.tight_layout()
        st.pyplot(fig5)

    with col6:
        # your creative choice: maybe neutral concentration?
        top5_neutral = summary.sort_values(by='Neutral', ascending=False).head(5)
        fig6, ax6 = plt.subplots(figsize=(5,3))
        sns.barplot(data=top5_neutral, x='Neutral', y='Link', palette="Purples_d", ax=ax6)
        ax6.set_title("Top 5 Posts by Neutral Comments")
        fig6.tight_layout()
        st.pyplot(fig6)
    
    
    # Download
    st.download_button("📥 Download Summary as CSV", summary.to_csv(index=False), "summary.csv", "text/csv")

    # Detailed comments
    st.markdown("---")
    st.subheader("📝 Detailed Comments with Sentiment")
    st.dataframe(df)