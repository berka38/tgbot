from telegram import *
from telegram.ext import *
from commands import *


# Bot tokeninizi buraya ekleyin
TOKEN = "6425561350:AAGr6caRiZyWA9QYlqxnqKspirvEArmmfmQ"


# def echo(update: Update, context: CallbackContext) -> None:
    # update.message.reply_text(update.message.text)

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    dispatcher.add_handler(CommandHandler("sikayetkapat", sikayetkapat))
    dispatcher.add_handler(CommandHandler("sikayetal", sikayetal))
    dispatcher.add_handler(CommandHandler("sikayet", sikayet))
    dispatcher.add_handler(CommandHandler("adminekle", adminekle))
    dispatcher.add_handler(CommandHandler("adminsil", adminsil))
    dispatcher.add_handler(CommandHandler("talep", talep))
    dispatcher.add_handler(CommandHandler("yardim", yardim))
    job_queue.run_repeating(check_sikayetler, interval=30, first=0)    
    job_queue.run_repeating(tekrar_mesaj, interval=3600, first=0)    
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()