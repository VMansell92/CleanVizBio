import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO

st.set_page_config(page_title="CleanVizBio", layout="wide")
st.title("🧬 CleanVizBio: Scientific Data Cleaning & Visualization")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV or TSV file", type=["csv", "tsv"])

if uploaded_file:
    try:
        # Try to detect delimiter
        content = uploaded_file.read().decode("utf-8")
        delimiter = "\t" if "\t" in content else ","
        df = pd.read_csv(StringIO(content), delimiter=delimiter)

        st.subheader("Data Preview")
        st.dataframe(df.head())

        st.sidebar.header("Data Cleaning")
        if st.sidebar.checkbox("Drop empty rows"):
            df.dropna(how="all", inplace=True)
        if st.sidebar.checkbox("Drop empty columns"):
            df.dropna(axis=1, how="all", inplace=True)

        st.sidebar.header("Column Renaming")
        columns = df.columns.tolist()
        new_names = {}
        for col in columns:
            new = st.sidebar.text_input(f"Rename column '{col}'", value=col)
            new_names[col] = new
        df.rename(columns=new_names, inplace=True)

        st.subheader("Basic Statistics")
        if st.checkbox("Show statistics"):
            st.write(df.describe())

        st.subheader("Visualizations")
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

        if numeric_cols:
            plot_type = st.selectbox("Select plot type", ["Histogram", "Box Plot", "Scatter Plot", "Heatmap"])

            if plot_type == "Histogram":
                col = st.selectbox("Column for histogram", numeric_cols)
                fig, ax = plt.subplots()
                sns.histplot(df[col], kde=True, ax=ax)
                st.pyplot(fig)

            elif plot_type == "Box Plot":
                col = st.selectbox("Column for box plot", numeric_cols)
                fig, ax = plt.subplots()
                sns.boxplot(y=df[col], ax=ax)
                st.pyplot(fig)

            elif plot_type == "Scatter Plot":
                x = st.selectbox("X-axis", numeric_cols)
                y = st.selectbox("Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
                fig, ax = plt.subplots()
                sns.scatterplot(x=df[x], y=df[y], ax=ax)
                st.pyplot(fig)

            elif plot_type == "Heatmap":
                fig, ax = plt.subplots()
                sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
                st.pyplot(fig)

        st.subheader("Download Cleaned Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download cleaned CSV", data=csv, file_name="cleaned_data.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Upload a .csv or .tsv file to get started.")
