import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


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
st.line_chart(filtered.set_index("Month")["Accidents"])
st.dataframe(filtered)
