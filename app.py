import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import io
import numpy as np




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
            plot_type = st.selectbox("Select plot type", ["Histogram", "Box Plot", "Scatter Plot", "Heatmap", "PCA", "Volcano Plot"])

            if plot_type == "Histogram":
                col = st.selectbox("Column for histogram", numeric_cols)
                fig, ax = plt.subplots()
                sns.histplot(df[col], kde=True, ax=ax)
                st.pyplot(fig)

                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                st.download_button(
                    label="📥 Download Histogram",
                    data=buf.getvalue(),
                    file_name="histogram.png",
                    mime="image/png"
                )


            elif plot_type == "Box Plot":
                col = st.selectbox("Column for box plot", numeric_cols)
                fig, ax = plt.subplots()
                sns.boxplot(y=df[col], ax=ax)
                st.pyplot(fig)

                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                st.download_button(
                    label="📥 Download Box Plot",
                    data=buf.getvalue(),
                    file_name="box_plot.png",
                    mime="image/png"
                ) 


            elif plot_type == "Scatter Plot":
                x = st.selectbox("X-axis", numeric_cols)
                y = st.selectbox("Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
                fig, ax = plt.subplots()
                sns.scatterplot(x=df[x], y=df[y], ax=ax)
                st.pyplot(fig)

                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                st.download_button(
                    label="📥 Download Scatter Plot",
                    data=buf.getvalue(),
                    file_name="scatter_plot.png",
                    mime="image/png"
                )


            elif plot_type == "Heatmap":
                fig, ax = plt.subplots()
                sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
                st.pyplot(fig)

                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                st.download_button(
                    label="📥 Download Heatmap",
                    data=buf.getvalue(),
                    file_name="heatmap.png",
                    mime="image/png"
                )


            elif plot_type == "PCA":
                st.write("🔬 PCA - Principal Component Analysis")

                df_clean = df[numeric_cols].dropna()
    
                if df_clean.shape[0] < 2 or df_clean.shape[1] < 2:
                     st.warning("❗ PCA requires at least 2 samples and 2 numeric columns.")
                else:
                    scaled = StandardScaler().fit_transform(df_clean)
                    pca = PCA(n_components=2)
                    components = pca.fit_transform(scaled)

                    explained_var = pca.explained_variance_ratio_ * 100
                    st.write(f"🧠 PC1 explains {explained_var[0]:.2f}% of variance, PC2 explains {explained_var[1]:.2f}%")

                    pca_df = pd.DataFrame(data=components, columns=["PC1", "PC2"])
                    fig, ax = plt.subplots()
                    sns.scatterplot(x="PC1", y="PC2", data=pca_df, ax=ax)
                    ax.set_title("PCA: PC1 vs. PC2")
                    st.pyplot(fig)

                    buf = io.BytesIO()
                    fig.savefig(buf, format="png")
                    st.download_button(
                        label="📥 Download PCA Plot",
                        data=buf.getvalue(),
                        file_name="pca_plot.png",
                        mime="image/png"
                    )

            elif plot_type == "Volcano Plot":
                st.write("🌋 Volcano Plot - log2FoldChange vs. p-value")

                if "log2FoldChange" not in df.columns or "p-value" not in df.columns:
                    st.error("This dataset must contain 'log2FoldChange' and 'p-value' columns.")
                else:
                    df_v = df.dropna(subset=["log2FoldChange", "p-value"]).copy()
                    df_v["-log10(p-value)"] = -np.log10(df_v["p-value"])
                    df_v["Significant"] = (abs(df_v["log2FoldChange"]) > 1) & (df_v["p-value"] < 0.05)

                    fig, ax = plt.subplots()
                    sns.scatterplot(
                        data=df_v,
                        x="log2FoldChange",
                        y="-log10(p-value)",
                        hue="Significant",
                        palette={True: "red", False: "gray"},
                        legend=False,
                        ax=ax
                    )
                    ax.set_title("Volcano Plot")
                    st.pyplot(fig)

                    buf = io.BytesIO()
                    fig.savefig(buf, format="png")
                    st.download_button(
                        label="📥 Download Volcano Plot",
                        data=buf.getvalue(),
                        file_name="volcano_plot.png",
                        mime="image/png"
                    )



        st.subheader("Download Cleaned Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download cleaned CSV", data=csv, file_name="cleaned_data.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Upload a .csv or .tsv file to get started.")


if st.button("📄 Generate Analysis Report (Markdown)"):
    report_lines = []

    report_lines.append("# 🔬 CleanVizBio Summary Report")
    report_lines.append("Generated with CleanVizBio – Scientific Data Visualization App\n")

    # Dataset info
    report_lines.append("## 📂 Dataset Info")
    report_lines.append(f"- Number of rows: {df.shape[0]}")
    report_lines.append(f"- Number of columns: {df.shape[1]}")
    report_lines.append(f"- Numeric columns: {', '.join(numeric_cols)}\n")

    # Basic Stats
    report_lines.append("## 📊 Basic Statistics\n")
    report_lines.append(df[numeric_cols].describe().to_markdown())

    # PCA variance (if available)
    try:
        explained_var = pca.explained_variance_ratio_ * 100
        report_lines.append("\n## 🔎 PCA Summary")
        report_lines.append(f"- PC1 explains **{explained_var[0]:.2f}%**, PC2 explains **{explained_var[1]:.2f}%** of variance")
    except:
        report_lines.append("\n## 🔎 PCA Summary")
        report_lines.append("- PCA not run or data insufficient.")

    report_md = "\n".join(report_lines)

    st.download_button(
        label=⬇️ Download Markdown Report",
        data=report_md,
        file_name="cleanvizbio_report.md",
        mime="text/markdown"
    )

