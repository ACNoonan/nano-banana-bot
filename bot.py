import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from google.cloud import vision
import io
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import database


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! I am Nano Banana Bot. Send me a picture to process or text to generate an image. For more information, use the /help command.')


async def set_api_key_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set the user's API key."""
    user_id = update.message.from_user.id
    try:
        api_key = context.args[0]
        database.set_api_key(user_id, api_key)
        await update.message.reply_text("Your API key has been set successfully. I will now delete your message for security.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /set_api_key <your_api_key>")
    
    # Delete the message containing the API key for security
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "Welcome to the Nano Banana Bot!\n\n"
        "You can use this bot to:\n"
        "1. *Generate images from text:* Just send me a text message with a description of the image you want to create.\n"
        "2. *Analyze images:* Send me a photo, and I'll tell you what I see in it.\n\n"
        "Commands:\n"
        "/start - Start the conversation with the bot.\n"
        "/set_api_key - Set your Google Cloud API key.\n"
        "/help - Show this help message."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages for image generation."""
    user_id = update.message.from_user.id
    api_key_path = database.get_api_key(user_id)

    if not api_key_path:
        await update.message.reply_text("Please set your API key first using the /set_api_key command.")
        return

    text = update.message.text
    await update.message.reply_text(f"Generating image for: '{text}'. This might take a moment...")

    try:
        # The GOOGLE_APPLICATION_CREDENTIALS env var will be set temporarily for this call
        # In a real-world scenario, you'd manage this more robustly
        original_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_key_path

        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION")
        vertexai.init(project=project_id, location=location)
        
        model = ImageGenerationModel.from_pretrained("imagegeneration@005")
        response = model.generate_images(
            prompt=text,
            number_of_images=1
        )
        
        if response.images:
            image_bytes = response.images[0]._image_bytes
            await update.message.reply_photo(photo=io.BytesIO(image_bytes))
        else:
            await update.message.reply_text("Sorry, I could not generate an image for that prompt.")
        
        # Restore original credentials if they existed
        if original_creds:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = original_creds
        else:
            del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    except Exception as e:
        logging.error(f"Error generating image: {e}")
        await update.message.reply_text("Sorry, there was an error generating the image.")


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle image messages for processing."""
    user_id = update.message.from_user.id
    api_key_path = database.get_api_key(user_id)

    if not api_key_path:
        await update.message.reply_text("Please set your API key first using the /set_api_key command.")
        return
        
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    
    photo_bytes = io.BytesIO()
    await photo_file.download_to_memory(photo_bytes)
    photo_bytes.seek(0)
    
    original_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_key_path

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=photo_bytes.read())

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if labels:
        label_descriptions = [label.description for label in labels]
        await update.message.reply_text(f"Detected labels: {', '.join(label_descriptions)}")
    else:
        await update.message.reply_text("Could not detect any labels in the image.")

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    if original_creds:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = original_creds
    else:
        del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]


def main():
    """Start the bot."""
    load_dotenv()

    database.initialize_database()

    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_token:
        logging.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
        return

    application = Application.builder().token(telegram_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_api_key", set_api_key_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    application.run_polling()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    main()
