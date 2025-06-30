# 📊 Instagram Sentiment Analyzer

This project is a **Streamlit-based web application** that allows you to upload an Excel file of Instagram comments and analyze them for sentiment insights using NLTK's VADER sentiment analyzer.

It auto-categorizes comments into **Positive, Negative, Neutral**, builds summaries, and shows interactive graphs to help visualize comment sentiment across posts.

---

## 🚀 Features

✅ Upload Excel files (.xlsx) containing Instagram comments and post links.
✅ Automatic sentiment classification using VADER (Positive, Negative, Neutral).
✅ Generates summary tables by Post ID & Link.
✅ Shows:

* Overall sentiment distribution (bar + pie charts)
* Top 5 posts with highest positive comments
* Top 5 worst posts with least positive comments
* Top 5 posts with highest negative comments
* Top 5 posts with highest neutral comments
  ✅ Download summarized CSV for reporting.
  ✅ Responsive, modern UI with custom CSS styling.

---

## 🏗️ Project Structure

```
📂 instagram-sentiment-analyzer
│
├── app.py               # Main Streamlit application
├── assets/
│   └── styles.css       # Custom CSS for styling the dashboard
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
```

---

## ⚙️ Tech Stack

* **Python 3.12**
* **Streamlit** for building interactive dashboards.
* **Pandas** for data manipulation.
* **NLTK VADER** for sentiment analysis.
* **Matplotlib & Seaborn** for visualizations.

---

## 📥 How to Run Locally

1️⃣ **Clone the repository**

```bash
git clone https://github.com/770navyasharma/sentiment_analyser
cd sentiment_analyzer
```

2️⃣ **Create virtual environment (optional but recommended)**

```bash
python3.12 -m venv venv. # change according to your specification
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3️⃣ **Install dependencies**

```bash
pip install -r requirements.txt
```

4️⃣ **Run Streamlit app**

```bash
streamlit run app.py
```

---

## 📄 Excel File Format

Your Excel file should have at least these columns:

| Link        | Comment          |
| ----------- | ---------------- |
| <post-link> | This is awesome! |
| <post-link> | I hate this...   |

* The `Link` is used to group comments by posts.
* The `Comment` text is analyzed for sentiment.

---

## ✨ Dashboard Highlights

* Custom modern styling via `assets/styles.css`.
* Uses multi-row, multi-column layouts to display:

  * Bar charts, pie charts.
  * Top & worst performing posts.
* Interactive tables with color gradients.

---

## 💡 Future Enhancements

* Allow multi-file batch analysis.
* Add wordclouds for most common positive & negative words.
* Support more file formats (CSV, Google Sheets).
* Add advanced filters (date range, keyword).

---

## 👩‍💻 Made with ❤️ by Navya

---

