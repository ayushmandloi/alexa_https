from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")

def get_headlines():
    user_pass_dict = {'user': 'ayush210',
                      'passwd': 'ayush210',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa : Ayush'})
    sess.post('https://www.reddit.com/api/login', data=user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/gadgets/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '... '.join([i for i in titles])
    return titles

news = get_headlines()
print news

@app.route('/')
def homepage():
    return "hi there, hoe are you"

@ask.launch
def start_skill():
    welcome_message = "hello there woul you like the news?"
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The current world headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text ='I am not sure then why you have asked me to open that app...bye'
    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug=True)





