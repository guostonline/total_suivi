import pandas as pd
import streamlit as st
from core.excel import *

# import data from excel file
st.set_page_config(page_title="Rapport FDV",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )
st.sidebar.header("Options")
upload_file = st.sidebar.file_uploader("Choose Excel file", type="xlsx")
day_work = 0
total_day = 0
if upload_file is not None:
    excel_file = Excel(upload_file)
    excel_file.fix_sheets()
    total_day, day_work = excel_file.get_day_work()
    st.title("File converted")
df = pd.read_excel(
    io="excel/finale.xlsx",
    engine="openpyxl",
    sheet_name=["AGADIR", "QUALI NV"],
)

col1, col2, col3 = st.sidebar.columns(3)
with col1:
    total_days = int(st.text_input("Total days", value=total_day))

with col2:
    total_days_work = int(st.text_input("Days work", value=day_work))
with col3:
    total_days_rest = int(st.text_input("Days Rest", value=str(total_days - day_work)))
df = df.get("AGADIR")
df = df.fillna(0)
list_of_string_H: list = df[df['H'].apply(lambda x: isinstance(x, str))]
list_of_string_Percent: list = df[df['Percent'].apply(lambda x: isinstance(x, str))]

for i in list_of_string_H.index:
    df.loc[i, "H"] = 0
for i in list_of_string_Percent.index:
    df.loc[i, "Percent"] = 0

df = df.astype({
    "REAL": "int",
    "OBJ": "int",
    "Real 2023": "int",
    "Historique 2022": "int",
    # "H": "int",
    # "Percent": "int",

})
df.loc[:, "Percent"] = df["Percent"].map("{:.1%}".format)

df.loc[:, "H"] = df["H"].map('{:.1%}'.format)

st.dataframe(df)
