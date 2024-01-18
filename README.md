# NeuraNET API Playground

![NeuraNET API Playground](playground.png)

## Overview

This open source Streamlit application is the official [NeuraNET API Playground](https://playground.neuranet-ai.com) and provides an interactive interface to the NeuraNET API, allowing users to access and utilize AI models for chat (and with vision), image generation, and TTS (Text-To-Speech).

## Features
- **API Authentication**: Secure API key input for accessing NeuraNET services.
- **Model Selection**: Users can choose between chat, chat with vision, image generation and text to speech.
- **Dynamic Inputs**: Input fields adapt based on the model selected.
- **Error Handling**: The app includes checks for missing API keys and empty inputs, along with error messages for user guidance.

## Installation

1. Install requirements with:
```
pip install -r requirements.txt
```

## Usage

Run the app with the command:
```
streamlit run main.py
```

## Supported Models
### Chat Models
- **NeuraNET Lite**: A free version of the NeuraNET chat AI, perfect for basic queries and conversations.
- **NeuraNET Hyper**: A premium chat model offering advanced understanding and more detailed responses.
- **NeuraNET Hyper Vision**: Only accessible to paying beta testers, this model combines the capabilities of advanced chat functionalities with vision to interpret and discuss images.

### Image Generation Models
- **Vinci Mini**: A free and fast version for basic image generation tasks.
- **Vinci Max**: A premium image generation model delivering high-quality visual content.

### TTS Model
The NeuraNET Text-to-Speech AI Model, referred to as NeuraNET Mint, has an array of 300 distinct voice options. This model and API can be used for completely free of charge.

## API Endpoints
- Image Generation: `POST https://neuranet-ai.com/api/v1/image`
- Chat: `POST https://neuranet-ai.com/api/v1/chat`
- TTS: `POST https://neuranet-ai.com/api/v1/tts`

## License

The NeuraNET API Playground is open-source and is under the MIT License. See the [LICENSE](LICENSE) for more information.

### === Made with ❤️ by the NeuraNET Team ===
