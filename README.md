# Nano Banana Bot

A Telegram bot that generates images using Google's Gemini models. It can create new images from a text prompt, or modify an existing image based on a prompt.

## Features

-   **Text-to-Image Generation:** Creates an image from a descriptive text prompt using the `gemini-1.5-flash` model.
-   **Image-and-Text-to-Image Generation:** Modifies an existing image based on a text prompt using the multimodal `gemini-1.5-pro` model.
-   Secure handling of API keys using a local `.env` file.
-   Simple, user-friendly commands: `/start` and `/help`.

## How it Works

The bot has two modes:
1.  **Send a plain text message:** The bot will interpret this as a text-to-image request.
2.  **Send a message with an image and a caption:** The bot will use both the image and the text prompt (in the caption) to generate a new, modified image.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ACNoonan/nano-banana-bot.git
    cd nano-banana-bot
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Get your API Keys:**
    -   **Telegram:** Open Telegram, find `@BotFather`, and use the `/newbot` command to create a bot. BotFather will give you a token.
    -   **Google Gemini:** Go to the [Google Cloud Console](https://console.cloud.google.com/), create a new project, and enable the **"Generative Language API"** and the **"Cloud Quotas API"**. Then, go to **APIs & Services -> Credentials -> Create credentials -> API key** to get your key.

5.  **Set up your `.env` file:**
    -   Create a file named `.env` in the root directory.
    -   You will need your Telegram Token, your Gemini API Key, and your Google Cloud Project ID (which you can find on your Google Cloud Console dashboard).
    -   Add your keys and project ID to it like this:
        ```ini
        # Telegram Bot Token from BotFather
        TELEGRAM_BOT_TOKEN="your_telegram_bot_token"

        # Your Google Gemini API Key
        GEMINI_API_KEY="your_gemini_api_key"

        # Your Google Cloud Project ID
        GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
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
