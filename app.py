# Import necessary libraries
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up Streamlit app
st.set_page_config(page_title="💿 Data Sweeper", layout='wide')

# Custom CSS for styling
st.markdown("""
    <style>
        /* Title Centering */
        .center-text { text-align: center; font-size: 26px; font-weight: bold; color: #1F618D; }
        
        /* File uploader styling */
        div[data-testid="stFileUploader"] { 
            border: 2px dashed #4A90E2; 
            background-color: #f9f9f9; 
            padding: 15px; 
            border-radius: 10px; 
            text-align: center;
        }
        
        /* Success message */
        .stAlert {
            background-color: #E6F4EA !important;
            color: #1D8348 !important;
            border-left: 5px solid #1D8348;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Title & Description
st.markdown("<h1 class='center-text'> Data Transformer 🚀</h1>", unsafe_allow_html=True)
st.write("🔄 Transform your files between **CSV and Excel** formats with **built-in data cleaning & visualization!**")

# File Upload
uploaded_files = st.file_uploader("📂 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read file
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"⚠️ Error reading file: {e}")
            continue

        # File Information
        st.subheader(f"📜 File Details: {file.name}")
        st.write(f"**File Size:** {round(file.size / 1024, 2)} KB")
        st.write("🔍 **Preview (First 5 Rows):**")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠️ Data Cleaning")
        if st.checkbox(f"🧹 Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove Duplicates - {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed successfully!")

            with col2:
                if st.button(f"🔄 Fill Missing Values - {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values have been filled!")

        # Column Selection
        st.subheader("📌 Select Columns")
        columns = st.multiselect(f"🔎 Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization") 
        if st.checkbox(f"📈 Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion
        st.subheader("🔄 Convert & Download")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        
        if st.button(f"⬇️ Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}", 
                data=buffer, 
                file_name=file_name, 
                mime=mime_type
            )

st.success("✅ All files processed!") 
