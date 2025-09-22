# Nano Banana Bot

A Telegram bot that generates images using Google's "Nano Banana" (`gemini-2.5-flash-image-preview`) model. It can create new images from a text prompt, or modify an existing image based on a prompt.

## Features

-   **Text-to-Image Generation:** Creates an image from a descriptive text prompt.
-   **Image-and-Text-to-Image Generation:** Modifies an existing image with a text prompt.
-   Simple, user-friendly commands: `/start` and `/help`.

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ACNoonan/nano-banana-bot.git
cd nano-banana-bot
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Google Cloud Project
1.  **Project Setup:** Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project (or select an existing one). Make sure you have **enabled billing** for the project to avoid restrictive free-tier limits.
2.  **Enable API:** Enable the **"Vertex AI API"** for your project.
3.  **Get Gemini API Key:** Go to **APIs & Services -> Credentials -> Create credentials -> API key**. Copy this key and ensure it belongs to the project with billing enabled.

### 5. Create `.env` file
Create a file named `.env` in the root directory. You will need your Telegram Token and your Gemini API Key.

```ini
# Telegram Bot Token from BotFather
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"

# Your Google Gemini API Key
GEMINI_API_KEY="your_gemini_api_key"
```

## Usage

1.  **Start the bot:**
    ```bash
    python bot.py
    ```
2.  **Interact with the bot on Telegram:**
    -   Use the `/start` command to begin.
    -   Send a text message for text-to-image.
    -   Send an image with a caption for image modification.
    -   Use `/help` for detailed instructions.
