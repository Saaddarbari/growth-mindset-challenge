#  import
import streamlit as st
import pandas as pd
import os
from io import BytesIO


# Set up our App
st.set_page_config(page_title="Data Sweeper App", layout="wide")
st.sidebar.success("🌟Be Silent And let your success shout")
st.markdown(
    """
    <style>
        .responsive-title {
            text-align: center;
            font-size:70px !important;
        }
        @media (max-width: 600px) {
            .responsive-title {
            text-align: center;
            font-size:30px !important;
            }
        }
    </style>
    <h1 class="responsive-title">🚀Data Sweeper</h1>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        .responsive-titles {
            text-align: center;
            font-size:30px !important;
        }
        @media (max-width: 600px) {
            .responsive-titles {
            text-align: center;
            font-size:20px !important;
            }
        }
    </style>
    <h1 class="responsive-titles">Prepared by Saad Darbari</h1>
    """
    , unsafe_allow_html=True)
st.write("🌟Transform your file between CSV to Excel formats with built-in data and Visulization!")


uploaded_files = st.file_uploader("Upload Files to CSV or Excel :" ,type=["csv","xlsx"], accept_multiple_files=True)
if uploaded_files :
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv" :
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
           df = pd.read_excel(file)
        else:
            st.error(f"This File types Does not support : {file_ext}")
            continue

        # Display info About the file 
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")


        #Show 5 row of our df
        st.write("Preview the Head of the DataFrame")
        st.dataframe(df.head())


        # Options of Data Cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1 , col2 = st.columns(2)

            with col1 :
                if st.button(f"Remove Duplicate file {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✔️Duplicates Remove!")
            with col2 :
                if st.button(f"Fill missing Value {file.name} ") :
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✔️missing value Have been filled")
            

            # Choose Specific Coloumn to keep or convert
            st.subheader("Select Coulumn to convert")
            columns = st.multiselect(f"Choose column to {file.name}",df.columns,default=df.columns)
            df= df[columns]

            #Create some visulization
            st.subheader(f"Data visualization")
            if st.checkbox(f"Show visualization for {file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])


            #convert the csv to Excel
            st.subheader("Conversion Options")
            conversion_types = st.radio(f"Convert {file.name} to:",["CSV","Excel"],key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_types == "CSV":
                    df.to_csv(buffer,index=False)
                    file_name = file.name.replace(file_ext,".csv")
                    mime_type = "text/csv"

                elif conversion_types == "Excel":
                    df.to_excel(buffer,index=False)
                    file_name = file.name.replace(file_ext,".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)


                #Download button
                st.download_button(
                    label=f"Download {file.name} to {conversion_types}",
                    data =buffer,
                    file_name = file.name,
                    mime = mime_type
                )
st.success("All files Proceed! 🎉")