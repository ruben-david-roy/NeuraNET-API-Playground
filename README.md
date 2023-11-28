# NeuraNET API Playground

![NeuraNET API Playground](playground.png)

## Overview
This Streamlit application is the official [NeuraNET API Playground](https://playground.neuranet-ai.com) and provides an interactive interface to the NeuraNET API, allowing users to access and utilize AI models for chat and image generation.

### Features
- **API Authentication**: Secure API key input for accessing NeuraNET services.
- **Model Selection**: Users can choose between chat and image generation models.
- **Dynamic Inputs**: Input fields adapt based on the model selected.
- **Error Handling**: The app includes checks for missing API keys and empty inputs, along with error messages for user guidance.

## Installation
1. Install requirements with `pip install -r requirements.txt`

## Usage
Run the app with the command: `streamlit run main.py`

### Navigation
- **Sidebar**: Use the sidebar to select AI model types, input API key, and provide additional inputs based on the model type.
- **Main Area**: View the NeuraNET logo, title, and interact with the model-specific functionalities.

### Image Model
- **Model Choice**: Select between 'Vinci Mini' and 'Vinci Max'.
- **Prompt Input**: Enter a prompt for image generation.
- **Generate Image**: Click to generate images based on the provided prompt.

### Chat Model
- **Model Choice**: Select between 'NeuraNET Lite' and 'NeuraNET Pro'.
- **Instruct Prompt**: Optional field for additional instructions.
- **User Input**: Type your message for the chat model.
- **Send Message**: Click to interact with the chat model.

## API Endpoints
- Image Generation: `POST https://neuranet-ai.com/api/v1/image`
- Chat: `POST https://neuranet-ai.com/api/v1/chat`

## Error Handling
- Checks for valid API key and non-empty inputs.
- Provides user feedback on missing data or API access issues.

## License
MIT LICENSE, see details [here](LICENSE)

Developed by the NeuraNET Team
