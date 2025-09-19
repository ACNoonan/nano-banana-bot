# Nano Banana Bot

A Telegram bot that generates images using Google's Gemini models. It can create new images from a text prompt, or modify an existing image based on a prompt.

## Features

-   **Text-to-Image Generation:** Creates an image from a descriptive text prompt using the `gemini-1.5-flash` model.
-   **Image-and-Text-to-Image Generation:** Modifies an existing image with a text prompt.
-   **Quota Awareness:** Checks for API quota limits and informs the user.
-   **Automatic Retries:** Automatically retries API requests when hitting rate limits.
-   **Secure Authentication:** Uses API keys for Gemini and OAuth2 (via ADC) for Google Cloud Quotas.

## How it Works

The bot uses the `google-generativeai` library to interact with the Gemini API.

-   **Text-to-Image:** `gemini-1.5-flash` is used for its speed in generating images from text prompts.
-   **Image-and-Text-to-Image:** The more powerful `gemini-1.5-pro` model is used for multimodal inputs (image + text).
-   **Quota Management:** The bot calls the **Cloud Quotas API** to fetch details about your usage when you hit a rate limit. This requires separate authentication.

When the bot experiences a temporary `ResourceExhausted` error (a common rate-limiting issue), it will automatically retry the request up to 3 times with exponential backoff.

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
1.  **Project Setup:** Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project (or select an existing one).
2.  **Enable APIs:** Enable the following APIs for your project:
    -   **AI Platform API** (also listed as "Vertex AI API")
    -   **Cloud Quotas API**
3.  **Get Gemini API Key:** Go to **APIs & Services -> Credentials -> Create credentials -> API key**. Copy this key.

### 5. Set Up Authentication

The bot uses two authentication methods:
-   An **API Key** for the Gemini API (image generation).
-   A **Service Account** for the Cloud Quotas API (checking usage). This is the standard, most secure method for authenticating applications.

#### Setting up a Service Account
You need to create a dedicated account for the bot and download its private key.

1.  **Go to the Service Accounts page** in the Google Cloud Console. This link will take you directly to the correct project:
    -   [https://console.cloud.google.com/iam-admin/serviceaccounts?project=nanabonanatgbot](https://console.cloud.google.com/iam-admin/serviceaccounts?project=nanabonanatgbot)

2.  Click **"+ CREATE SERVICE ACCOUNT"**.
    -   **Service account name:** `nano-banana-bot-sa`
    -   Click **"CREATE AND CONTINUE"**.

3.  **Grant it the `Cloud Quotas Viewer` role.**
    -   In the "Select a role" dropdown, type `Cloud Quotas Viewer` and select it. This allows the bot to read usage information.
    -   Click **"CONTINUE"**, then **"DONE"**.

4.  **Create a JSON Key.**
    -   Back on the Service Accounts list, click the email of the account you just created.
    -   Go to the **"KEYS"** tab.
    -   Click **"ADD KEY"** -> **"Create new key"**.
    -   Ensure **JSON** is selected and click **"CREATE"**. A JSON file will be downloaded.

### 6. Create `.env` file
1.  Move the downloaded JSON key file into the root of the `nano-banana-bot` project directory.
2.  Create a file named `.env`. You will need your Telegram Token, your Gemini API Key, your Google Cloud Project ID, and the name of the JSON key file.

```ini
# Telegram Bot Token from BotFather
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"

# Your Google Gemini API Key (must be from the same project)
GEMINI_API_KEY="your_gemini_api_key"

# Your Google Cloud Project ID
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

# The filename of your downloaded service account key
GOOGLE_APPLICATION_CREDENTIALS="your-service-account-file-name.json"
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

## Quota Management
The Gemini API has a free tier with usage limits. If you use the bot frequently, you may encounter `ResourceExhausted` errors.

-   **Check Your Quotas:** You can view your current quotas in the [Google Cloud Console](https://console.cloud.google.com/iam-admin/quotas).
-   **Enable Billing:** To increase your API limits, you must [enable billing](https://cloud.google.com/billing/docs/how-to/modify-project) for your Google Cloud project.
