import streamlit as st
import requests
import json
import base64
import os
import random
import string

st.set_page_config(page_title="NeuraNET API Playground", page_icon="https://neuranet-ai.com/static/img/cover.png")

st.sidebar.markdown("<h1 style='text-align: center;'>Settings</h1>", unsafe_allow_html=True)

model_type = st.sidebar.selectbox('Which Type of AI Model?', ('Chat', 'Image', 'TTS'))

st.markdown("<p style='text-align: center;'><img src='https://neuranet-ai.com/static/img/cover.png' style='width: 20%; height: auto;'></p>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>NeuraNET API Playground</h1>", unsafe_allow_html=True)

def generate_random_string(length=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def save_uploaded_file(uploaded_file):
    try:
        os.makedirs('host', exist_ok=True)

        file_ext = os.path.splitext(uploaded_file.name)[1]
        file_name = f"host/{generate_random_string()}{file_ext}"
        with open(file_name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_name
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

NEURANET_API_KEY = st.sidebar.text_input('Enter your NeuraNET API Key', type='password', autocomplete='off')
if not NEURANET_API_KEY:
    st.error('Please enter your NeuraNET API Key.')
    st.stop()

headers = {
    'Authorization': f'Bearer {NEURANET_API_KEY}',
    'Content-Type': 'application/json'
}

if model_type == 'Image':
    st.markdown("<p style='text-align: center;'>The NeuraNET Text-To-Image (Diffusion) Models, referred to as Vinci.</p>", unsafe_allow_html=True)

    model_alias = st.sidebar.selectbox('Choose a model', ('Vinci Mini', 'Vinci Max'))
    model = 'vinci-mini' if model_alias == 'Vinci Mini' else 'vinci-max'

    dimensions = st.sidebar.selectbox('Image dimensions', ('square', 'portrait', 'landscape'))

    user_input = st.text_input("Type your prompt here")

    if st.button('Generate Image'):
        if not user_input:
            st.error("Prompt is empty. Please type your message.")
            st.stop()

        data = {
            'content': {
                'model': model,
                'prompt': user_input,
                'size': dimensions
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
    st.markdown("<p style='text-align: center;'>NeuraNET Text Generation (Chat) Models - Chat History is not supported here.</p>", unsafe_allow_html=True)

    model_alias = st.sidebar.selectbox('Choose a model', ('NeuraNET Lite', 'NeuraNET Hyper', 'NeuraNET Hyper Vision', 'NeuraNET Hyper Web'))
    model = 'nlite' if model_alias == 'NeuraNET Lite' else 'neuranet-hyper-vision-5x185b' if model_alias == 'NeuraNET Hyper Vision' else 'neuranet-hyper-5x185b' if model_alias == 'NeuraNET Hyper' else 'neuranet-hyper-web-5x185b'

    image_data = None
    if model == 'neuranet-hyper-vision-5x185b':
        uploaded_image = st.file_uploader("Upload an Image (PNG or JPEG)", type=["png", "jpg", "jpeg"])
        if uploaded_image is not None:
            saved_file_path = save_uploaded_file(uploaded_image)
            if saved_file_path:
                image_url = f'http://neuranet-api-playground.streamlit.app/{saved_file_path}'

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
            user_message["image"] = f"data:image/png;base64,{image_data}"

        if model == 'nweb':
            try:
                search_response = requests.get(f'https://search.neuranet-ai.com/search?query={user_input}&limit=5')
                search_results = search_response.json()

                if search_results:
                    web_instruct_message = "You are a special version of the NeuraNET Hyper model called 'NeuraNET Hyper Web', you have the ability to indirectly search the internet. You will now receive the search results of what the user said. It will be formatted like this: 'Title - Source Link - Snippet'.You will receive user queries and present the corresponding search results in this format. When creating a response to the user, do not give the user the raw search results, tell it to them in a friendly, informative, and casual way. Here's the user's query: \n\n"
                    for result in search_results:
                        web_instruct_message += f"{result['title']} - {result['link']} - {result['snippet']}\n"
                else:
                    web_instruct_message = "Request failed or is empty."

            except Exception as e:
                web_instruct_message = "Request failed or is empty."

            history.append({
                "sender": "instruct",
                "content": web_instruct_message
            })

        history.append(user_message)

        data = {
            'settings': {
                'model': 'neuranet-hyper-5x185b' if model == 'neuranet-hyper-web-5x185b' else model
            },
            'conversation': {
                'history': history
            }
        }

        response = requests.post('https://neuranet-ai.com/api/v1/chat', headers=headers, data=json.dumps(data))

        try:
            response_data = response.json()
            ai_response = response_data['choices'][0]['text']
            st.write(f"{ai_response} Payload: {data}")
        except KeyError:
            st.error('Invalid API Key or you are trying to use a model that you do not have access to.')
            st.stop()

elif model_type == 'TTS':
    st.markdown("<p style='text-align: center;'>The NeuraNET Text-To-Speech (TTS) Model, referred to as NeuraNET Mint.</p>", unsafe_allow_html=True)

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

    types.discard('en-US')
    selected_type = st.sidebar.selectbox('Select Type', ['en-US'] + sorted(types), index=0)
    available_voices = voices_by_type[selected_type] if selected_type in voices_by_type else []
    selected_voice = st.sidebar.selectbox('Select Voice', available_voices, index=available_voices.index('Eric') if 'Eric' in available_voices else 0)

    user_input = st.text_area("Enter the text for TTS")

    if st.button('Generate Speech'):
        if not user_input:
            st.error("Text is empty. Please type your message.")
            st.stop()
        if not selected_type:
            st.error("Please select a type.")
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
