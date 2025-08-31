# Nano Banana Bot

A Telegram bot that generates new images from a prompt and an existing image, using Google's Gemini 1.5 Flash model.

## Features

- Generates a new image based on a user-provided image and a text prompt.
- Powered by the `gemini-1.5-flash` model via the Google Generative AI API.
- Secure handling of API keys using a local `.env` file.
- Simple, user-friendly commands: `/start` and `/help`.

## How it Works

You send a message containing an image and a caption. The bot takes both your image and your text prompt (the caption) and sends them to the Gemini model, which then generates a completely new image based on your inputs.

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
    -   **Google Gemini:** Go to the [Google Cloud Console](https://console.cloud.google.com/), create a new project, and enable the **"Generative Language API"**. Then, go to **APIs & Services -> Credentials -> Create credentials -> API key** to get your key.

5.  **Set up your `.env` file:**
    -   Create a file named `.env` in the root directory.
    -   Add your keys to it like this:
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
    -   Send a message with an image and a caption describing what you want to generate.
    -   Use `/help` for instructions.
