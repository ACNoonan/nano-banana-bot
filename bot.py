import os
import logging
import io
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import google.generativeai as genai
from google.api_core import exceptions
import httpx
from PIL import Image

# --- Bot Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message."""
    await update.message.reply_text('Hello! Send me a text prompt to generate an image, or an image with a caption to modify it.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message."""
    help_text = (
        "**Welcome to the Nano Banana Bot!**\n\n"
        "This bot can generate images in two ways:\n\n"
        "1.  **Text-to-Image:**\n"
        "    - Just send a text message describing the image you want.\n"
        "    - *Example:* `a futuristic city with flying cars`\n\n"
        "2.  **Image-and-Text-to-Image:**\n"
        "    - Send a photo and add a text prompt in the caption.\n"
        "    - *Example:* Attach a photo of your cat and add the caption `make my cat a pirate`."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

# --- Quota and Image Generation Logic ---

async def get_quota_info(project_id: str, model_name: str) -> str:
    """Fetches and formats quota information from the Google Cloud Quotas API."""
    api_key = os.getenv("GEMINI_API_KEY")
    service_name = "generativelanguage.googleapis.com"
    url = f"https://cloudquotas.googleapis.com/v1/projects/{project_id}/locations/global/services/{service_name}/quotaInfos?key={api_key}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            formatted_quotas = [f"Quota details for model `{model_name}`:"]
            quota_found = False
            if 'quotaInfos' in data:
                for info in data['quotaInfos']:
                    dimensions = info.get('dimensions', {})
                    if dimensions.get('model') == model_name:
                        quota_found = True
                        name = info.get('displayName', 'Unknown Quota')
                        usage = int(info.get('quotaUsage', {}).get('currentValue', 0))
                        limit = int(info.get('quotaIncreaseEligibility', {}).get('limitValue', 0))
                        formatted_quotas.append(f"- *{name}*: Used {usage} / {limit}")
            
            if quota_found:
                return "\n".join(formatted_quotas)
            else:
                return "Could not retrieve specific quota details for the model."

    except httpx.HTTPStatusError as e:
        logging.error(f"Error fetching quota info: {e.response.status_code} - {e.response.text}")
        if e.response.status_code == 403:
            return "Could not fetch quota details. Please ensure the 'Cloud Quotas API' is enabled in your Google Cloud project."
        return "Could not fetch quota details due to a server error."
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching quota info: {e}")
        return "An error occurred while trying to fetch your quota details."


async def handle_text_to_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates an image from a text prompt."""
    prompt = update.message.text
    await update.message.reply_text(f"🎨 Generating image for: '{prompt}'...")

    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash") # Or another suitable text-to-image model
        response = model.generate_content(prompt, generation_config={"response_mime_type": "image/png"})
        
        if response.parts and response.parts[0].inline_data and response.parts[0].inline_data.data:
            image_bytes = response.parts[0].inline_data.data
            img_buffer = io.BytesIO(image_bytes)
            img_buffer.seek(0)
            await update.message.reply_photo(photo=img_buffer)
        else:
            logging.error(f"API did not return image data for text prompt. Response: {response}")
            await update.message.reply_text("Sorry, I could not generate an image from that text. The model may have refused the prompt.")

    except exceptions.ResourceExhausted as e:
        logging.warning(f"Quota exceeded for text-to-image: {e}")
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        quota_details = await get_quota_info(project_id, "gemini-1.5-flash")
        await update.message.reply_text(f"⚠️ You've hit the API quota.\n\n{quota_details}", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in text-to-image generation: {e}")
        await update.message.reply_text("Sorry, there was an error generating your image.")


async def handle_image_and_text_to_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates a new image from an existing image and a text prompt."""
    prompt = update.message.caption
    await update.message.reply_text(f"🎨 Modifying image with prompt: '{prompt}'...")

    try:
        photo = update.message.photo[-1]
        photo_file = await photo.get_file()
        
        photo_bytes_io = io.BytesIO()
        await photo_file.download_to_memory(photo_bytes_io)
        photo_bytes_io.seek(0)
        
        input_image = Image.open(photo_bytes_io)

        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        response = model.generate_content([prompt, input_image])
        
        if response.parts and response.parts[0].inline_data and response.parts[0].inline_data.data:
            image_bytes = response.parts[0].inline_data.data
            img_buffer = io.BytesIO(image_bytes)
            img_buffer.seek(0)
            await update.message.reply_photo(photo=img_buffer)
        else:
            logging.error(f"API did not return image data for image prompt. Response: {response}")
            await update.message.reply_text("Sorry, I could not generate an image. The model may have refused the prompt.")

    except exceptions.ResourceExhausted as e:
        logging.warning(f"Quota exceeded for image-and-text-to-image: {e}")
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        quota_details = await get_quota_info(project_id, "gemini-1.5-pro")
        await update.message.reply_text(f"⚠️ You've hit the API quota.\n\n{quota_details}", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in image-and-text-to-image generation: {e}")
        await update.message.reply_text("Sorry, there was an error generating your image.")


# --- Main Bot Setup ---

def main():
    """Start the bot."""
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        logging.warning("GOOGLE_CLOUD_PROJECT not set in .env file. Quota details will not be available.")

    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_to_image))
    application.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, handle_image_and_text_to_image))

    application.run_polling()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    main()
