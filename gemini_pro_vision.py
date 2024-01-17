import streamlit as st
import os
import image_to_code

import google.generativeai as genai
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
prompt = """Generate code (HTML FULL CODE, CSS FULL CODE) 
for a website that looks EXACTLY like the one in the image provided, 
, make sure the stylesheet is called 
styles.css, Make HTML, CSS code, and make sure to put the code inside 
```html and ```css tags MAKE SURE CSS INCLUDES HOVER EFFECTS, LEAVE IMAGES' SRC ATTRIBUTES (if there are any images) AS PLACEHOLDERS, DON'T LEAVE ANY OTHER PLACEHOLDERS, INCLUDE ALL THE TEXT AND DON'T LEAVE OUT ANYTHING, MAKE AN EXACT VERSION OF THE WEBSITE IN THE IMAGE PROVIDED. MAKE SURE NONE OF THE  CODES (HTML OR CSS) IS MISSING, MAKE SURE TO PROVIDE CSS CODE, MAKE SURE THERE IS CSS CODE FOR EVERY SINGLE PART AND ELEMENT OF THE WEBSITE, NEVER LEAVE ANY ELEMENT WITHOUT STYLE!!, MAKE SURE THE WEBSITE DESIGN IS PERFECTLY IDENTICAL WITH THE IMAGE PROVIDED, MAKE SURE THE CODE IS FULL,, INCLUDE CSS FOR NAVIGATION BAR ON TOP OF THE WEBSITE IF THERE'S ONE IN THE IMAGE"""


def getGeminiProResponse(image_url, input):
    genai.configure(api_key=GOOGLE_API_KEY)

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": input,
            },  # You can optionally provide text parts
            {
                "type": "image_url",
                "image_url": image_url,
            },
        ]
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro-vision", temperature=0.4, max_output_tokens=4096
    )
    print("Generating response...")
    response = llm.invoke([message])

    text = str(response)
    text = text.split("content='")[1]
    text = text.encode().decode("unicode_escape")

    return text


