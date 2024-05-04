import streamlit as st
from tornado.web import RequestHandler
from injectApi import CustomRule, init_global_tornado_hook, uninitialize_global_tornado_hook

class HelloWorldHandler(RequestHandler):
    def get(self):
        self.write({
            "text": "Hello World"
        })
        
    def post(self):
        self.set_status(200)
        self.write({
            "text": "Hello World"
        })
        
    def check_xsrf_cookie(self) -> None:
        return None

init_global_tornado_hook([CustomRule("/hello", HelloWorldHandler)])

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