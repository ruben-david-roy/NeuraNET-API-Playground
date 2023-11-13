import streamlit as st
import requests
import json

st.set_page_config(page_title="NeuraNET API Demo", page_icon="https://neuranet-ai.com/static/img/cover.png")

st.sidebar.markdown("<h1 style='text-align: center;'>Settings</h1>", unsafe_allow_html=True)

model_type = st.sidebar.selectbox('Which Type of AI Model?', ('Chat', 'Image'))

st.markdown("<p style='text-align: center;'><img src='https://neuranet-ai.com/static/img/cover.png' style='width: 20%; height: auto;'></p>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>NeuraNET API Playground</h1>", unsafe_allow_html=True)

apikey = st.sidebar.text_input('Enter your NeuraNET API Key', type='password')
if not apikey:
    st.error('Please enter your NeuraNET API Key.')
    st.stop()

headers = {
    'Authorization': f'Bearer {apikey}',
    'Content-Type': 'application/json'
}

if model_type == 'Image':
    st.markdown("<p style='text-align: center;'>NeuraNET Diffusion (Image Generation) Models</p>", unsafe_allow_html=True)

    model_alias = st.sidebar.selectbox('Choose a model', ('Vinci Mini', 'Vinci Max'))
    model = 'vinci-mini' if model_alias == 'Vinci Mini' else 'vinci-max'

    user_input = st.text_input("Type your prompt here")

    if st.button('Generate Image'):
        if not user_input:
            st.error("Prompt is empty. Please type your message.")
            st.stop()

        data = {
            'content': {
                'model': model,
                'prompt': user_input
            }
        }

        response = requests.post('https://neuranet-ai.com/api/v1/image', headers=headers, data=json.dumps(data))

        try:
            response_data = response.json()

            if 'result' in response_data and len(response_data['result']) > 0:
                image_url = response_data['result'][0]['result-url']
                st.image(image_url, caption='Generated Image', use_column_width=True)
            else:
                st.error('Invalid API Key or you are trying to use a model that you do not have access to.')
                st.stop()

        except ValueError:
            st.error('Decoding JSON has failed')
            st.stop()

elif model_type == 'Chat':
    st.markdown("<p style='text-align: center;'>NeuraNET Text Generation (Chat) Models</p>", unsafe_allow_html=True)

    model_alias = st.sidebar.selectbox('Choose a model', ('NeuraNET Lite', 'NeuraNET Pro'))
    model = 'nlite' if model_alias == 'NeuraNET Lite' else 'npro'

    instruct_input = st.sidebar.text_area("Instruct Prompt (Optional)", height=300)

    conversation = {}
    if instruct_input:
        conversation['Instruct'] = instruct_input

    user_input = st.text_input("Type your message")

    if st.button('Send Message'):
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

        response = requests.post('https://neuranet-ai.com/api/v1/chat', headers=headers, data=json.dumps(data))

        try:
            response_data = response.json()
            ai_response = response_data['choices'][0]['text']
            if 'AI' not in conversation:
                conversation['AI'] = ai_response
            else:
                conversation['AI'] = conversation['AI'] + "\n" + ai_response

            st.write(ai_response)
        except KeyError:
            st.error('Invalid API Key or you are trying to use a model that you do not have access to.')
            st.stop()
