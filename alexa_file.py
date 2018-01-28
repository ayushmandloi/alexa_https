from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")

def get_headlines(type):
    user_pass_dict = {'user': 'ayush210',
                      'passwd': 'ayush210',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa : Ayush'})
    sess.post('https://www.reddit.com/api/login', data=user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/'+type+'/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '... '.join([i for i in titles])
    return titles



@app.route('/')
def homepage():
    return "hi there, hoe are you"

@ask.launch
def start_skill():
    welcome_message = "hello there, welcome to the reddit news, what type of news you want to hear?"
    return question(welcome_message)

# @ask.intent("YesIntent")
# def share_headlines():
#     headlines = get_headlines('world')
#     headline_msg = 'The current world headlines are {}'.format(headlines)
#     return statement(headline_msg)

@ask.intent("WorldNewsIntent")
def world_news_intent():
    headlines = get_headlines('worldnews')
    headline_msg = 'The current top 10 world headlines are {}'.format(headlines)
    return statement(headline_msg)


@ask.intent("GadgetsNewsIntent")
def world_news_intent():
    headlines = get_headlines('gadgets')
    headline_msg = 'The current top 10 gadget headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("AndroidNewsIntent")
def world_news_intent():
    headlines = get_headlines('android')
    headline_msg = 'The current top 10 Android headlines are {}'.format(headlines)
    return statement(headline_msg)



@ask.intent("NoIntent")
def no_intent():
    bye_text ='I am not sure then why you have asked me to open that app...bye!'
    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug=True)





