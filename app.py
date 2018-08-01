from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from siksa import all_list, tagging, get_recipe, get_recipe2
from tts import make_tts
from news import *

#global users_input

app = Flask(__name__)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")

#english_bot.set_trainer(ChatterBotCorpusTrainer)
#english_bot.train("chatterbot.corpus.english")


@app.route("/")
def home():
    return render_template("index.html")

def get_tts(input):
	make_tts(input)

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    #get_tts(userText)

    # print("---------users_input : "+ str(users_input))
    # return str(news_intent(userText))

    if '레시피' in userText:
        return str(get_recipe2(tagging(userText).get('food')))
    #return str(english_bot.get_response(userText))
    else:
        return str(get_recipe(tagging(userText).get('food')))

if __name__ == "__main__":
    app.run()
