import streamlit as st
import pandas as pd
import requests
from requests.structures import CaseInsensitiveDict
import json
import io

# Mapping of agent names to their respective IDs
agent_dict = {
    "Bot2_DS_Generators_Infobot": "ed63e9f6-e8c7-4737-83cc-3f3be93ce2b4",
    "cd_Card_Case": "f1568d9a-856e-4ad4-90d9-97d28d610a42",
    "Deutsche Bank PWS PK Agent": "cc412014-0536-4b3f-a951-09eb8fc96c4f",
    "Deutsche Bank PWS Assistant": "c2b632d9-a5c8-41e7-8d71-f15d47d3770a",
    "Sabio Postbank": "054c4b18-ba9b-44f5-9f04-32cbf3c1c84b",
    "Sabio Privatbank": "1adb88ca-6617-4330-b088-d26a3debb351",
    "Sabio Privatbank EN": "8fdda3ca-9327-4838-9843-550179cbc567",
    "sabio_postbank_jsonl_v2": "543886c2-bb6b-42b8-b7ed-34367c6907b2",
    "Sabio-Postbank-TF": "2247e4ad-2d07-4a7d-a3da-d421de93abf6"
}

# Function to send message to the API and get response
def get_chatbot_response(user_message, agent_id):
    url = "https://ac-pbconvai-dev-project.web.app/api/submitMessage"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    data = {
        "user_message": user_message,
        "agentId": agent_id,
        "languageCode": "de",
        "sessionId": "874a8f1e-eb47-41ea-aa75-7821b7530d77",
        "useRoentgen": False
    }

    data_json = json.dumps(data)
    resp = requests.post(url, headers=headers, data=data_json)
    response_dict = json.loads(resp.text)
    return response_dict['responseText']

# Streamlit UI
st.title("Asimov Chatbot Testing")

# Agent selection dropdown
agent_name = st.selectbox("Select an Agent", list(agent_dict.keys()))
agent_id = agent_dict[agent_name]

# File upload
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the file into a dataframe
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("Uploaded data:")
    st.write(df)

    # Check if the dataframe has the required column
    if 'user_message' not in df.columns:
        st.error("The file must contain a 'user_message' column.")
    else:
        # Get responses for each message
        df['response_text'] = df['user_message'].apply(lambda msg: get_chatbot_response(msg, agent_id))

        st.write("Data with responses:")
        st.write(df)

        # Download the result
        @st.cache_data
        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        @st.cache_data
        def convert_df_to_excel(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        csv = convert_df_to_csv(df)
        excel = convert_df_to_excel(df)

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='chatbot_responses.csv',
            mime='text/csv',
        )

        st.download_button(
            label="Download Excel",
            data=excel,
            file_name='chatbot_responses.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
