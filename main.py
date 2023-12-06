import streamlit as st
import requests
import json
import base64

st.set_page_config(page_title="NeuraNET API Playground", page_icon="https://neuranet-ai.com/static/img/cover.png")

st.sidebar.markdown("<h1 style='text-align: center;'>Settings</h1>", unsafe_allow_html=True)

model_type = st.sidebar.selectbox('Which Type of AI Model?', ('Chat', 'Image', 'TTS'))

st.markdown("<p style='text-align: center;'><img src='https://neuranet-ai.com/static/img/cover.png' style='width: 20%; height: auto;'></p>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>NeuraNET API Playground</h1>", unsafe_allow_html=True)

NEURANET_API_KEY = st.sidebar.text_input('Enter your NeuraNET API Key', type='password')
if not NEURANET_API_KEY:
    st.error('Please enter your NeuraNET API Key.')
    st.stop()

headers = {
    'Authorization': f'Bearer {NEURANET_API_KEY}',
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
    
    model_alias = st.sidebar.selectbox('Choose a model', ('NeuraNET Lite', 'NeuraNET Pro', 'NeuraNET Pro Vision'))
    model = 'nlite' if model_alias == 'NeuraNET Lite' else 'npro-vision' if model_alias == 'NeuraNET Pro Vision' else 'npro'

    image_data = None
    if model == 'npro-vision':
        uploaded_image = st.file_uploader("Upload an Image (PNG or JPEG)", type=["png", "jpg", "jpeg"])
        if uploaded_image is not None:

            image_data = base64.b64encode(uploaded_image.getvalue()).decode()
    
    instruct_input = st.sidebar.text_area("Instruct Prompt (Optional)", height=300)
    
    history = []
    if instruct_input:
        history.append({
            "sender": "instruct",
            "content": instruct_input
        })
    
    user_input = st.text_input("Type your message")
    
    if st.button('Send Message'):
        if not user_input:
            st.error("User input is empty. Please type your message.")
            st.stop()
    
        user_message = {
            "sender": "user",
            "content": user_input
        }
        if image_data:
            user_message["image_url"] = f"data:image/png;base64,{image_data}"
    
        history.append(user_message)
    
        data = {
            'settings': {
                'model': model
            },
            'conversation': {
                'history': history
            }
        }
    
        response = requests.post('https://neuranet-ai.com/api/v1/chat', headers=headers, data=json.dumps(data))
    
        try:
            response_data = response.json()
            ai_response = response_data['choices'][0]['text']
            history.append({
                "sender": "assistant",
                "content": ai_response
            })
    
            st.write(ai_response)
        except KeyError:
            st.error('Invalid API Key or you are trying to use a model that you do not have access to.')
            st.stop()

elif model_type == 'TTS':
    st.markdown("<p style='text-align: center;'>NeuraNET Text-to-Speech</p>", unsafe_allow_html=True)

    voices_response = requests.get('https://neuranet-ai.com/api/v1/tts/voices')
    voices_data = voices_response.json()

    types = set()
    voices_by_type = {}
    for voice_entry in voices_data:
        voice_type = voice_entry['type']
        voice_name = voice_entry['voice']
        types.add(voice_type)
        if voice_type in voices_by_type:
            voices_by_type[voice_type].append(voice_name)
        else:
            voices_by_type[voice_type] = [voice_name]

    selected_type = st.sidebar.selectbox('Select Type', [''] + sorted(types))
    available_voices = voices_by_type[selected_type] if selected_type else [voice['voice'] for voice in voices_data]
    selected_voice = st.sidebar.selectbox('Select Voice', available_voices, index=available_voices.index('Eric') if 'Eric' in available_voices else 0)

    user_input = st.text_area("Enter the text for TTS")

    if st.button('Generate Speech'):
        if not user_input:
            st.error("Text is empty. Please type your message.")
            st.stop()

        data = {
            'settings': {
                'type': selected_type if selected_type else 'en-US',
                'voice': selected_voice
            },
            'say': user_input
        }

        response = requests.post('https://neuranet-ai.com/api/v1/tts', headers=headers, data=json.dumps(data))

        try:
            response_data = response.json()
            audio_url = response_data['result'][0]['result-url']
            st.audio(audio_url, format='audio/mp3', start_time=0)
        except KeyError:
            st.error('Invalid API Key or an error occurred while processing your request.')
            st.stop()
