from telegram import *
from telegram.ext import *
from commands2 import *


# Bot tokeninizi buraya ekleyin
TOKEN = "6009120642:AAEWVdBwNOs8SIT6hXVLyt1H11d5vsmTVHg"


# def echo(update: Update, context: CallbackContext) -> None:
    # update.message.reply_text(update.message.text)

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    dispatcher.add_handler(CommandHandler("startnew", startnew)) 
    dispatcher.add_handler(CommandHandler("adminekle", adminekle)) 
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()