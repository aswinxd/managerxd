import telebot
from telebot import types
import configparser

# Read config
config = configparser.ConfigParser()
config.read('config.ini')

# Read bot token from config
TOKEN = config['Telegram']['token']

bot = telebot.TeleBot(TOKEN)

# Command to start the bot
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! I'm your group management bot.")

# Command to kick a user
@bot.message_handler(commands=['kick'])
def kick_user(message):
    if message.reply_to_message:
        kicked_user_id = message.reply_to_message.from_user.id
        bot.kick_chat_member(message.chat.id, kicked_user_id)
        bot.send_message(message.chat.id, "User kicked!")
    else:
        bot.reply_to(message, "Reply to a user's message to kick them.")

# Command to ban a user
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        banned_user_id = message.reply_to_message.from_user.id
        bot.kick_chat_member(message.chat.id, banned_user_id)
        bot.send_message(message.chat.id, "User banned!")
        bot.unban_chat_member(message.chat.id, banned_user_id)
    else:
        bot.reply_to(message, "Reply to a user's message to ban them.")

# Handle /clone command
@bot.message_handler(commands=['clone'])
def clone_bot(message):
    # Check if the user provided a bot token
    if len(message.text.split()) != 2:
        bot.reply_to(message, "Please provide a bot token.")
        return
    
    # Extract the provided bot token
    clone_token = message.text.split()[1]
    
    # Initialize a new bot instance with the provided token
    try:
        clone_bot = telebot.TeleBot(clone_token)
    except Exception as e:
        bot.reply_to(message, f"Error creating bot instance: {e}")
        return
    
    # Define handlers for the cloned bot instance
    @clone_bot.message_handler(commands=['start'])
    def start_cloned(message):
        clone_bot.reply_to(message, "Welcome! I'm your cloned group management bot.")

    @clone_bot.message_handler(commands=['kick'])
    def kick_user_cloned(message):
        if message.reply_to_message:
            kicked_user_id = message.reply_to_message.from_user.id
            clone_bot.kick_chat_member(message.chat.id, kicked_user_id)
            clone_bot.send_message(message.chat.id, "User kicked!")
        else:
            clone_bot.reply_to(message, "Reply to a user's message to kick them.")

    @clone_bot.message_handler(commands=['ban'])
    def ban_user_cloned(message):
        if message.reply_to_message:
            banned_user_id = message.reply_to_message.from_user.id
            clone_bot.kick_chat_member(message.chat.id, banned_user_id)
            clone_bot.send_message(message.chat.id, "User banned!")
            clone_bot.unban_chat_member(message.chat.id, banned_user_id)
        else:
            clone_bot.reply_to(message, "Reply to a user's message to ban them.")
    
    # Start the polling for the cloned bot
    clone_bot.polling(none_stop=True)
    
    bot.reply_to(message, "Bot cloned successfully!")

# Start the bot
bot.polling()
