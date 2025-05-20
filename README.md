# 🧬 CleanVizBio

**CleanVizBio** is a web-based bioinformatics and data visualization tool built with Python and Streamlit. Designed for researchers, students, and data analysts, it simplifies the process of exploring, visualizing, and reporting scientific data — no coding required.

---

## 🚀 Features

- 📂 Upload `.csv` or `.tsv` data files
- 🧹 Clean datasets by removing empty rows/columns and renaming headers
- 📊 Visualize data with:
  - Histogram
  - Box Plot
  - Scatter Plot
  - Heatmap (correlation)
  - PCA (Principal Component Analysis)
  - Volcano Plot for log2FC and p-values
- 📈 View PCA variance explained
- 💾 Download plots as `.png`
- 📄 Generate a **Markdown analysis report** summarizing stats, PCA, and dataset info

---

## 📎 Report Export (Markdown)

Users can export a `.md` report containing:
- Dataset overview
- Summary statistics
- PCA results (if available)

This report can be:
- Opened in VS Code, Typora, or Dillinger.io
- Converted to PDF using tools like `pandoc` or Markdown editors

---

## 🛠️ Tech Stack

- Python 3
- Streamlit
- Pandas, NumPy, Seaborn, Matplotlib
- Scikit-learn
- Tabulate (for Markdown formatting)

---

## 📦 Run Locally

```bash
git clone https://github.com/VMansell92/CleanVizBio.git
cd CleanVizBio
python -m venv venv
venv\Scripts\activate     # (or source venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
streamlit run app.py




🔗 Live App
👉 https://cleanvizbio.streamlit.app


📄 License
MIT License

👩‍💻 Author
Victoria Mansell
GitHub @VMansell92
