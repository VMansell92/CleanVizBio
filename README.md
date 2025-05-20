# 🧬 CleanVizBio

**CleanVizBio** is a lightweight Streamlit web app for scientific data cleaning and visualization. Built for researchers, students, and small labs, it allows users to upload `.csv` or `.tsv` files, clean data, visualize it interactively, and download results — all without writing code.

---

## 🚀 Features

- 📂 Upload `.csv` or `.tsv` files
- 🧹 Drop empty rows/columns
- ✍️ Rename columns
- 📊 Generate basic stats (mean, std, etc.)
- 📈 Visualizations:
  - Histogram
  - Box Plot
  - Scatter Plot
  - Heatmap (correlation)
- 💾 Download cleaned data

---

## 📦 Tech Stack

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [Matplotlib](https://matplotlib.org/)

---

## 🧪 Getting Started (Local)

```bash
git clone https://github.com/VMansell92/CleanVizBio.git
cd CleanVizBio
python -m venv venv
venv\Scripts\activate      # (or source venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
streamlit run app.py
