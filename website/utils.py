from pytrends.request import TrendReq
import pandas
from .models import Blog
from . import mail_sender, db
from flask_mail import Message
from os import getenv
from aitextgen import aitextgen



def get_trending_title():
    # init
    pytrends = TrendReq(hl='en-US', tz=360)
    # getting treanding search

    # Us = pytrends.realtime_trending_searches(pn='US') # realtime search trends for United States
    India =  pytrends.realtime_trending_searches(pn='IN') # realtime search trends for India
    india_df = pandas.DataFrame(India)
    india_df_split = india_df.loc[0].title
    india_df_splited = india_df_split.split(",")
    return india_df_splited[0]


def ai_text(title, max_length=1500):
    # if we want large accurasy use (EleutherAI/gpt-neo-1.3B) this model
    ai_text_init = aitextgen(model="EleutherAI/gpt-neo-125M", to_gpu=False)
    generate_text = ai_text_init.generate_one(max_length = max_length, prompt = title, no_repeat_ngram_size = 3)
    return generate_text


def send_email(Body, Subject):
    msg = Message(f"{Subject}", 
    sender=getenv("EMAIL_USER"), 
    recipients=['nitheshwar040@gmail.com'],
    body=f'{Body}',)
    mail_sender.send(msg)