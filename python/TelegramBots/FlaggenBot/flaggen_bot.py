from telegram import InlineKeyboardButton, InlineKeyboardMarkup , ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler , CallbackQueryHandler
import logging,random
import csv,random

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send /quiz to start a quiz.")
    
def quiz(update,context):
    #prepare list for quiz
    country = random.choice(countries) + ["True"]
    choices = [country]
    
    counter = 0
    while counter < 3:
        country = random.choice(countries) + ["True"]
        if country not in choices:
            country[2] = "False"
            choices.append(land)
            counter += 1

    random.shuffle(choices)
        
    #creates reply_markup 
    buttons = []
    for key in choices:
        buttons.append(
        [InlineKeyboardButton(text = key[0], callback_data = key[2])]
        )
    keyboard = InlineKeyboardMarkup(buttons)
    
    context.bot.sendPhoto(chat_id=update.effective_chat.id,photo= open('Flaggen/'+country[1]+'.png','rb'),reply_markup = keyboard)


def button(update,context):
    query = update.callback_query
    query.answer()
    
    if f"{query.data}" == "quiz":
        context.bot.deleteMessage(message_id=query.message.message_id,chat_id=update.effective_chat.id)
        quiz(update,context)
        
    elif f"{query.data}" == "True":
        context.bot.deleteMessage(message_id=query.message.message_id,chat_id=update.effective_chat.id)

        markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "new Quiz!", callback_data = "quiz")]])
        context.bot.send_message(chat_id=update.effective_chat.id, text="This is correct.",reply_markup = markup)
        
    elif f"{query.data}" == "False":
        context.bot.deleteMessage(message_id=query.message.message_id,chat_id=update.effective_chat.id)

        markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "new Quiz!", callback_data = "quiz")]])
        context.bot.send_message(chat_id=update.effective_chat.id, text="This is false.",reply_markup = markup)

def getUpdater():
    updater = Updater(TOKEN, use_context=True)
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('quiz', quiz))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    return updater

def getCountries():
    countries = []
    with open('data.csv','r') as file:
        data = csv.reader(file)
        for i in data:
            countries.append([i[0],i[1].lower()])
        return countries[1::]
        
if __name__ == "__main__":
    countries = getCountries()

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    
    updater = getUpdater()
    updater.start_polling()
    updater.idle()
