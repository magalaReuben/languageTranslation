import streamlit as st
from tornado.web import RequestHandler
from injectApi import CustomRule, init_global_tornado_hook, uninitialize_global_tornado_hook
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, MBart50Tokenizer, MBartForConditionalGeneration
import datetime
import sentencepiece
import torch
import json
import os
import yaml
import logging


first_run = True


language_to_code = {
    "Acholi": ">>ach<<",
    "Ateso": ">>teo<<",
    "Luganda": ">>lug<<",
    "Lugbara": ">>lgg<<",
    "Runyankole": ">>nyn<<"
    }


language_iso_codes = {
        "Acholi": "ach",
        "Ateso": "teo",
        "Luganda": "lug",
        "Lugbara": "lgg",
        "Runyankole": "nyn",
    }



def multiple_to_english(text, language):
    mul_en_tokenizer.src_lang = language_iso_codes[language]
    inputs = mul_en_tokenizer(text, return_tensors="pt")
    tokens = mul_en_model.generate(**inputs)
    result = mul_en_tokenizer.decode(tokens.squeeze(), skip_special_tokens=True)
    return result


def english_to_multiple(text, target_language):
    lang_code = language_to_code[target_language]
    inputs = en_mul_tokenizer(f"{lang_code}{text}", return_tensors="pt")
    tokens = en_mul_model.generate(**inputs)
    result = en_mul_tokenizer.decode(tokens.squeeze(), skip_special_tokens=True)
    return result

def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    global mul_en_tokenizer, mul_en_model, en_mul_tokenizer, en_mul_model
    mul_en_tokenizer = MBart50Tokenizer.from_pretrained('Sunbird/mbart-mul-en')
    mul_en_model = MBartForConditionalGeneration.from_pretrained('Sunbird/mbart-mul-en')

    en_mul_tokenizer = AutoTokenizer.from_pretrained('Sunbird/sunbird-en-mul')
    en_mul_model = AutoModelForSeq2SeqLM.from_pretrained('Sunbird/sunbird-en-mul')

    logging.info("Init complete")
    
if first_run:
    init()
    first_run = False

class TranslationHandler(RequestHandler):
    def get(self):
        self.write({
            "text": "Hello World"
        })
        
    def post(self):
        self.set_status(200)
        body = self.request.body.decode('utf-8')  # Decode the body from bytes to string
        # Process the body of the request here
        self.write({
            "text": body
        })
        
    def check_xsrf_cookie(self) -> None:
        return None

init_global_tornado_hook([CustomRule("/translate", TranslationHandler)])

if not hasattr(st, 'already_started_server'):
    # Hack the fact that Python modules (like st) only load once to
    # keep track of whether this file already ran.
    st.already_started_server = True

    st.write('''
        The first time this script executes it will run forever because it's
        running a Flask server.

        Just close this browser tab and open a new one to see your Streamlit
        app.
    ''')


# We'll never reach this part of the code the first time this file executes!

# Your normal Streamlit app goes here:
x = st.slider('Pick a number')
st.write('You picked:', x)