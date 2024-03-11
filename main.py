from telegram.ext import Updater, CommandHandler
import configparser

# Read bot token from config
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config['Telegram']['token']

# Define the /start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Bot! You can start using it now.")

# Define the /clone command handler
def clone(update, context):
    if len(context.args) != 1:
        update.message.reply_text("Usage: /clone <token>")
        return
    clone_token = context.args[0]
    try:
        # Stop the polling of the original bot
        context.bot.stop_polling()

        clone_updater = Updater(token=clone_token, use_context=True)
        clone_dispatcher = clone_updater.dispatcher
        # Add handlers for any other commands or functionalities you want to clone
        clone_dispatcher.add_handler(CommandHandler('start', start))
        clone_dispatcher.add_handler(CommandHandler('ban', ban))
        clone_updater.start_polling()
        update.message.reply_text("Bot successfully cloned!")
    except Exception as e:
        update.message.reply_text(f"Error cloning bot: {e}")

# Define the /ban command handler
def ban(update, context):
    if update.message.reply_to_message:
        banned_user_id = update.message.reply_to_message.from_user.id
        context.bot.kick_chat_member(chat_id=update.effective_chat.id, user_id=banned_user_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text="User banned!")
    else:
        update.message.reply_text("Reply to a user's message to ban them.")

def main():
    # Initialize the Updater with the bot token
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('clone', clone))
    dispatcher.add_handler(CommandHandler('ban', ban))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
