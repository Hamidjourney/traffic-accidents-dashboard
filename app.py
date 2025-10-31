import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.title("🚦 Traffic Accidents Demo Dashboard")

# connect to Google Sheet
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
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
