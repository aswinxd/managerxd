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
    
    # Register the same handlers to the new bot instance
    clone_bot.add_message_handler(start)
    clone_bot.add_message_handler(kick_user)
    clone_bot.add_message_handler(ban_user)
    
    bot.reply_to(message, "Bot cloned successfully!")

# Start the bot
bot.polling()
