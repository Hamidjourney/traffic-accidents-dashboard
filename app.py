import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

hide_toolbar = """
    <style>
    .vega-actions a {display:none !important;}
    </style>
"""
st.markdown(hide_toolbar, unsafe_allow_html=True)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# st.secrets["gcp_service_account"] is a TOML table (like a dict)
creds = Credentials.from_service_account_info(
    dict(st.secrets["gcp_service_account"]), scopes=SCOPES
)




st.title("🚦 Traffic Accidents Demo Dashboard")
st.write("If you can deploy this, the pipeline is visible.")

# connect to Google Sheet
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open("TrafficAccidents_Sample").worksheet("Data")
df = pd.DataFrame(sheet.get_all_records())

# show chart
years = df["Year"].unique()
selected_year = st.selectbox("Select year", years)
filtered = df[df["Year"] == selected_year]
import altair as alt

chart = (
    alt.Chart(filtered)
    .mark_line(point=True)
    .encode(
        x=alt.X("Month:O", title="Month"),
        y=alt.Y("Accidents:Q", title="Number of Accidents"),
        tooltip=["Month", "Accidents"]
    )
    .properties(
        width="container",
        height=400
    )
)

st.altair_chart(chart, use_container_width=True)

st.dataframe(filtered)
