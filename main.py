import streamlit as st
import requests
import json

url = 'https://neuranet-ai.com/api/v1/chat'

st.set_page_config(page_title="NeuraNET API Demo", page_icon="https://neuranet-ai.com/static/img/cover.png")

st.sidebar.markdown("<h1 style='text-align: center;'>Settings</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center;'><img src='https://neuranet-ai.com/static/img/cover.png' style='width: 20%; height: auto;'></p>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>NeuraNET API Demo</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center;'>NeuraNET API Demo - Created with Streamlit & Python</p>", unsafe_allow_html=True)

apikey = st.sidebar.text_input('Enter your NeuraNET API Key', type='password')

if not apikey:
    st.error('Please enter your NeuraNET API Key.')
    st.stop()

headers = {
    'Authorization': f'Bearer {apikey}',
    'Content-Type': 'application/json'
}

model_alias = st.sidebar.selectbox('Choose a model', ('NeuraNET Lite', 'NeuraNET Pro'))

model = 'nlite' if model_alias == 'NeuraNET Lite' else 'npro'

instruct_input = st.sidebar.text_area("Instruct Prompt (Optional)", height=300)

conversation = {}

if instruct_input:
    conversation['Instruct'] = instruct_input

user_input = st.text_input("Type your message")

if st.button('Send'):
    if not user_input:
        st.error("User input is empty. Please type your message.")
        st.stop()

    if 'User' not in conversation:
        conversation['User'] = user_input
    else:
        conversation['User'] = conversation['User'] + "\n" + user_input

    data = {
        'settings': {
            'model': model
        },
        'conversation': conversation
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        response_data = response.json()
        ai_response = response_data['choices'][0]['text']
    except KeyError:
        st.error('Invalid API Key or you are trying to use a model that you do not have access to.')
        st.stop()

    if 'AI' not in conversation:
        conversation['AI'] = ai_response
    else:
        conversation['AI'] = conversation['AI'] + "\n" + ai_response

    st.write(ai_response)
