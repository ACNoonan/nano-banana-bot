import os
import logging
import io
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import google.generativeai as genai
from google.api_core import exceptions
from PIL import Image

# --- Bot Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message."""
    await update.message.reply_text('Hello! Send me a text prompt to generate an image, or an image with a caption to modify it.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message."""
    help_text = (
        "**Welcome to the Nano Banana Bot!**\n\n"
        "This bot uses the 'Nano Banana' (Gemini 2.5 Flash Image) model to generate images.\n\n"
        "1.  **Text-to-Image:**\n"
        "    - Just send a text message describing the image you want.\n"
        "    - *Example:* `a futuristic city with flying cars`\n\n"
        "2.  **Image-and-Text-to-Image:**\n"
        "    - Send a photo and add a text prompt in the caption.\n"
        "    - *Example:* Attach a photo of your cat and add the caption `make my cat a pirate`."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

# --- Image Generation Logic ---

async def handle_text_to_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates an image from a text prompt using the correct image generation model."""
    prompt = update.message.text
    await update.message.reply_text(f"🎨 Generating image for: '{prompt}'...")

    try:
        # As per the documentation, use the dedicated image generation model
        model = genai.GenerativeModel(model_name="gemini-2.5-flash-image-preview")
        response = await model.generate_content_async(prompt)

        # Parse the response according to the documentation's structure
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_bytes = part.inline_data.data
                    img_buffer = io.BytesIO(image_bytes)
                    img_buffer.seek(0)
                    await update.message.reply_photo(photo=img_buffer)
                    return # Exit after sending the first image found

        # If no image is found in the response
        logging.error(f"API did not return image data for text prompt. Response: {response}")
        await update.message.reply_text("Sorry, I could not generate an image from that text. The model may have refused the prompt.")

    except exceptions.GoogleAPICallError as e:
        logging.error(f"API call error in text-to-image generation: {e}")
        await update.message.reply_text(f"Sorry, there was an API error: {e.message}")
    except Exception as e:
        logging.error(f"Error in text-to-image generation: {e}")
        await update.message.reply_text("Sorry, there was an unexpected error generating your image.")

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

        # Use the correct model for image and text inputs
        model = genai.GenerativeModel(model_name="gemini-2.5-flash-image-preview")
        response = await model.generate_content_async([prompt, input_image])

        # Parse the response according to the documentation's structure
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_bytes = part.inline_data.data
                    img_buffer = io.BytesIO(image_bytes)
                    img_buffer.seek(0)
                    await update.message.reply_photo(photo=img_buffer)
                    return # Exit after sending the first image found

        logging.error(f"API did not return image data for image prompt. Response: {response}")
        await update.message.reply_text("Sorry, I could not generate an image. The model may have refused the prompt.")

    except exceptions.GoogleAPICallError as e:
        logging.error(f"API call error in image-and-text-to-image: {e}")
        await update.message.reply_text(f"Sorry, there was an API error: {e.message}")
    except Exception as e:
        logging.error(f"Error in image-and-text-to-image generation: {e}")
        await update.message.reply_text("Sorry, there was an error generating your image.")


# --- Main Bot Setup ---

def main():
    """Start the bot."""
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logging.critical("GEMINI_API_KEY not set in .env file. Bot cannot start.")
        return
    genai.configure(api_key=api_key)
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logging.critical("TELEGRAM_BOT_TOKEN not set in .env file. Bot cannot start.")
        return
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_to_image))
    application.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, handle_image_and_text_to_image))

    application.run_polling()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    main()
