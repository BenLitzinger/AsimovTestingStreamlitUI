import streamlit as st
import pandas as pd
import requests
from requests.structures import CaseInsensitiveDict
import json
import io

# Function to send message to the API and get response
def get_chatbot_response(user_message):
    url = "https://ac-pbconvai-dev-project.web.app/api/submitMessage"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    data = {
        "user_message": user_message,
        "agentId": "ed63e9f6-e8c7-4737-83cc-3f3be93ce2b4",
        "languageCode": "de",
        "sessionId": "874a8f1e-eb47-41ea-aa75-7821b7530d77",
        "useRoentgen": False
    }

    data_json = json.dumps(data)
    resp = requests.post(url, headers=headers, data=data_json)
    response_dict = json.loads(resp.text)
    return response_dict['responseText']

# Streamlit UI
st.title("Chatbot Testing Application")

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
        df['response_text'] = df['user_message'].apply(get_chatbot_response)

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
