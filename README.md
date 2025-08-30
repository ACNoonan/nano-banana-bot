# Nano Banana Bot

A Telegram bot for image processing and generation using Google Cloud.

## Features

- Process images sent to the bot using Google Cloud Vision API to detect labels.
- Generate images from text prompts using Google's Imagen on Vertex AI.
- Secure, user-specific handling of API keys.
- User-friendly commands: `/start`, `/help`, and `/set_api_key`.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/nano-banana-bot.git
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

4. **Generate an Encryption Key:**
   - Before running the bot, you need to generate a secret key to encrypt user API keys.
   - You can generate a key by running the following Python command in your terminal:
     ```bash
     python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
     ```
   - Copy the generated key.

5. **Set up environment variables:**
   - Create a `.env` file in the root directory.
   - Add your API keys and project details to the `.env` file. The `ENCRYPTION_KEY` is the one you just generated.
     ```
     # Secret key for encrypting user API keys
     ENCRYPTION_KEY="your_generated_encryption_key"

     # Telegram Bot Token from BotFather
     TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
     
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
- Before you can use the image generation or processing features, you need to set your Google Cloud API key using the `/set_api_key` command.
  ```
  /set_api_key /path/to/your/credentials.json
  ```
  For security, the bot will delete your message containing the API key after it has been set.

## Database
The bot uses a SQLite database (`user_data.db`) to store user API keys. This file will be created in the root directory when the bot is first started.
