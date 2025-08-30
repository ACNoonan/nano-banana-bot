# Nano Banana Bot

A Telegram bot for image processing and generation using Google Cloud.

## Features

- Process images sent to the bot using Google Cloud Vision API to detect labels.
- Generate images from text prompts using Google's Imagen on Vertex AI.
- Secure handling of API keys using a local `.env` file.
- User-friendly commands: `/start` and `/help`.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ACNoonan/nano-banana-bot.git
   cd nano-banana-bot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the root directory.
   - Add your API keys and project details to the `.env` file:
     ```
     # Telegram Bot Token from BotFather
     TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
     
     # Path to your Google Cloud service account key file
     GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/google-credentials.json"
     
     # Your Google Cloud project ID
     GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
     
     # The Google Cloud region for your project
     GOOGLE_CLOUD_LOCATION="your-gcp-region"
     ```

## Usage

- Start the bot:
  ```bash
  python bot.py
  ```
- Interact with the bot on Telegram. Use the `/start` command to begin and `/help` for instructions.
