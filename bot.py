import os
import logging
import io
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import google.generativeai as genai
from PIL import Image

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! Send me an image with a text prompt as the caption, and I will generate a new image for you.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "Welcome to the Nano Banana Bot!\n\n"
        "**How to use:**\n"
        "1. Attach an image to a message.\n"
        "2. Add a text prompt in the 'caption' field.\n"
        "3. Send the message.\n\n"
        "The bot will use your image and prompt to generate a new image using the Gemini 1.5 Flash model."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_image_generation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles image and caption to generate a new image."""
    if not update.message.caption:
        await update.message.reply_text("Please send an image with a text prompt in the caption.")
        return

    prompt = update.message.caption
    await update.message.reply_text(f"Generating image for: '{prompt}'. This might take a moment...")

    try:
        photo = update.message.photo[-1]
        photo_file = await photo.get_file()
        
        photo_bytes_io = io.BytesIO()
        await photo_file.download_to_memory(photo_bytes_io)
        photo_bytes_io.seek(0)
        
        img = Image.open(photo_bytes_io)

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, img])

        # Assuming the API returns a PIL.Image object in the response.
        # This part might need adjustment based on the actual API response format.
        # For this library, the response.parts[0] should contain the image data.
        generated_image_bytes = response.parts[0]._raw_content.blob.data
        
        img_buffer = io.BytesIO(generated_image_bytes)
        img_buffer.seek(0)
        
        await update.message.reply_photo(photo=img_buffer)

    except Exception as e:
        logging.error(f"Error generating image: {e}")
        await update.message.reply_text("Sorry, there was an error generating the image. Please check your API key and ensure the model is accessible.")

def main():
    """Start the bot."""
    load_dotenv()

    # Configure the Gemini API
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        logging.error("GEMINI_API_KEY not found in environment variables.")
        return
    genai.configure(api_key=gemini_api_key)

    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_token:
        logging.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
        return

    application = Application.builder().token(telegram_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # This handler now specifically looks for messages that are photos WITH a caption.
    application.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, handle_image_generation))
    # A handler for photos without a caption, to guide the user.
    application.add_handler(MessageHandler(filters.PHOTO & ~filters.CAPTION, lambda u, c: u.message.reply_text("Please include a text prompt in the caption.")))


    application.run_polling()

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    main()
